# System imports
import concurrent.futures
import time
import threading
from datetime import datetime

# Thirdparty
import schedule

# Local imports
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

    max_profile_run_timeout_s = 1

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

        self._profile_storage = profile_storage
        self._providers_manager = providers_manager
        self._result_handler = result_handler
        self._logger = get_module_logger(__name__)

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
        profile_result = ProfileResult(profile.profile_id, profile.name, datetime.utcnow())
        profile_result.result = provider_instance.run(profile.provider_parameters)
        profile_result.finished_at = datetime.utcnow()

        return profile_result

    def _run_and_handle(self, profile: Profile) -> None:
        if profile is None:
            raise ValueError("profile is required")

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(self._run_profile, profile)
            profile_result = None   # type: ProfileResult
            now = datetime.utcnow()

            try:
                # Normal profile result
                profile_result = future.result(timeout=self.max_profile_run_timeout_s)
            except Exception as err:
                # Profile result errored out
                profile_result = ProfileResult(profile.profile_id, profile.name, now)
                profile_result.finished_at = datetime.utcnow()

                # What is the reason?
                if isinstance(err, concurrent.futures._base.TimeoutError):
                    # The thread timed out
                    profile_result.result = ProviderResult(ResultStatus.TIMEOUT)
                else:
                    # The thread errored
                    # Log it
                    self._logger.error("Profile Id '{}' encountered error: {}".format(profile.profile_id, err))

                    # Return generic error result
                    profile_result.result = ProviderResult(ResultStatus.ERROR)
            else:
                # Did the normal profile result actually came back with a provider result?
                if profile_result.result is None:
                    # Nothing was returned as a result from the provider, so create a dummy Unknown
                    # provider result.
                    profile_result.result = ProviderResult(ResultStatus.UNKNOWN)

            # Only allow GREEN, YELLOW, RED and TIMEOUT results to go to the results handler
            if self._result_handler is not None and profile_result.result.status not in [ResultStatus.ERROR, ResultStatus.UNKNOWN]:
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
                self._logger.error("Error loading profile '{}': {}".format(profile.profile_id, ex))
            else:
                schedule.every(profile.run_every_x_seconds).seconds.do(run_threaded, profile)

        if not schedule.jobs:
            self._logger.critical("No valid profiles loaded, exiting!")
            return
        else:
            self._logger.info("{} profile(s) loaded.".format(len(schedule.jobs)))

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
