# System imports
import concurrent.futures
import time
import threading
from datetime import datetime

# Thirdparty
import schedule

# Local imports
from ..config import Config
from ..logging import get_module_logger
from ..profiles import Profile
from ..profiles.storage import BaseProfileStorage
from ..providers import ProviderResult, ResultStatus, ProvidersManager
from .output import LogResultHandler, ProfileResult


class ProfileRunner:
    """
    Description
    --
    Runs the profiles.
    """

    def __init__(
                self,
                profile_storage: BaseProfileStorage,
                providers_manager: ProvidersManager,
                result_handler: LogResultHandler) -> None:
        """
        Parameters
        --
        - profile_storage - an instance of a profile storage.
        - providers_manager - an instance of a providers manager.
        - result_handler - an instance of result handler.
        """

        if profile_storage is None:
            raise ValueError("profile_storage is required!")

        if providers_manager is None:
            raise ValueError("providers_manager is required!")

        if result_handler is None:
            raise ValueError("result_handler is required!")

        self._profile_storage = profile_storage
        self._providers_manager = providers_manager
        self._logger = get_module_logger(__name__)
        self._result_handler = result_handler

        try:
            self._max_run_timeout_s = int(Config.load('profile_runner', 'max_run_timeout_s'))
        except Exception:
            self._logger.warn(
                "Could not parse integer setting '%s' from config section '%s", 'max_run_timeout_s', 'profile_runner')
            self._max_run_timeout_s = 1

    def _run_profile(self, profile: Profile) -> ProfileResult:
        """
        Description
        --
        Runs a single profile.

        Parameters
        --
        - profile - the profile to run.

        Returns
        --
        The profile result.
        """

        if profile is None:
            raise ValueError("profile is required")

        # Create an instance of the provider associated with the profile
        provider_instance = self._providers_manager.instantiate(profile.provider_id)

        # Run the provider, by passing the profile parameters
        profile_result = ProfileResult(profile, datetime.utcnow())
        profile_result.result = provider_instance.run(profile.provider_parameters)
        profile_result.finished_at = datetime.utcnow()

        if (profile_result.result is None):
            self._logger.error("Profile '%s' did not return any result!", profile.id)
            profile_result.result = ProviderResult(ResultStatus.ERROR)

        return profile_result

    def _run_and_handle(self, profile: Profile) -> None:
        if profile is None:
            raise ValueError("profile is required")

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            # Run
            future = executor.submit(self._run_profile, profile)
            profile_result = None   # type: ProfileResult
            now = datetime.utcnow()

            try:
                # Normal profile result
                profile_result = future.result(timeout=self._max_run_timeout_s)
            except Exception as err:
                # Profile result errored out
                profile_result = ProfileResult(profile, now)
                profile_result.finished_at = datetime.utcnow()

                # What is the reason?
                if isinstance(err, concurrent.futures._base.TimeoutError):
                    # The thread timed out
                    profile_result.result = ProviderResult(ResultStatus.TIMEOUT)
                else:
                    # The thread errored
                    # Log it
                    self._logger.error("Profile Id '%s' encountered error: %s", profile.id, err)

                    # Return generic error result
                    profile_result.result = ProviderResult(ResultStatus.ERROR)

            # Now handle the result.
            if profile_result.result.status in [ResultStatus.GREEN, ResultStatus.YELLOW, ResultStatus.RED, ResultStatus.TIMEOUT]:
                self._result_handler.handle_result(profile_result)

    def start(self) -> None:
        """
        Description
        --
        Sets up profile execution plans, according to their schedule.
        """

        def run_threaded(profile: Profile) -> None:
            threading.Thread(target=self._run_and_handle, args=(profile,)).start()

        self._logger.info("Loading profiles ...")
        # Read the profiles and schedule the tasks
        for profile_id in self._profile_storage.get_all_ids():
            profile = self._profile_storage.get(profile_id)

            try:
                # Validate profile
                profile.self_validate()
                provider_instance = self._providers_manager.instantiate(profile.provider_id)
                provider_instance.validate(profile.provider_parameters)
            except Exception as ex:
                self._logger.error("Error loading profile '%s': %s", profile.id, ex)
            else:
                schedule.every(profile.run_every_x_seconds).seconds.do(run_threaded, profile)

        if not schedule.jobs:
            self._logger.critical("No valid profiles loaded, exiting!")
            return
        else:
            self._logger.info("%s profile(s) loaded.", len(schedule.jobs))

        self._logger.info("Starting loop ...")

        # run all jobs
        schedule.run_all()
        time.sleep(1)

        while True:
            try:
                # Run the schedule
                schedule.run_pending()
                time.sleep(1)
            except KeyboardInterrupt:
                self._logger.info("Shutting down ...")
                break
