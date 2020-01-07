# System imports
import concurrent.futures
import time
from typing import Generator, List
import threading
from datetime import datetime

# Thirdparty
import schedule

# Local imports
from core.profiles.base import Profile
from core.profiles.management import ProfileManager
from core.providers.management import ProvidersManager
from core.providers.base import ProviderResult, ResultStatus
from cron.output import BaseResultHandler, ProfileResult


class ProfileRunner:
    """
    Description
    --
    - Runs profiles.
    """

    max_profile_run_timeout_s = 1

    def __init__(
                self,
                profile_manager: ProfileManager,
                providers_manager: ProvidersManager,
                result_handler: BaseResultHandler) -> None:
        """
        Parameters
        --
        - profile_manager - an instance of a profile manager.
        - providers_manager - an instance of a providers manager.
        - result_handler - an instance of result handler.
        """

        if profile_manager is None:
            raise ValueError("profile_manager is required!")

        if providers_manager is None:
            raise ValueError("providers_manager is required!")

        self._profile_manager = profile_manager
        self._providers_manager = providers_manager
        self._result_handler = result_handler

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
        profile_result = ProfileResult(profile.profile_id, datetime.utcnow())
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
                profile_result = future.result(timeout=self.max_profile_run_timeout_s)
            except Exception as err:
                profile_result = ProfileResult(profile.profile_id, now)
                profile_result.finished_at = datetime.utcnow()

                if isinstance(err, concurrent.futures._base.TimeoutError):
                    profile_result.result = ProviderResult(ResultStatus.TIMEOUT)
                else:
                    profile_result.result = ProviderResult(ResultStatus.ERROR)                

            # And handle the result
            if self._result_handler is not None:
                self._result_handler.handle_result(profile_result)

    def start(self) -> None:
        """
        Description
        --
        Sets up profile execution plans, according to their schedule.
        """

        def run_threaded(profile: Profile) -> None:
            threading.Thread(target=self._run_and_handle, args=(profile,)).start()

        print("Scheduling tasks ...")
        # Read the profiles and schedule the tasks
        for profile_id in self._profile_manager.get_all_ids():
            profile = self._profile_manager.get(profile_id)
            # TODO: Use profile.schedule (cron tab to method translation)
            schedule.every().second.do(run_threaded, profile)
        
        print("Starting loop ...")
        while True:
            try:
                # Run the schedule
                schedule.run_pending()
                time.sleep(0.5)
            except KeyboardInterrupt:
                print("Shutting down ...")
                break

        print("Pulse is shut down.")