# System imports
import concurrent.futures
import time
from typing import Generator, List
import threading
from datetime import datetime

# Local imports
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

    # We can run X number of profiles in parallel
    max_parallel_profile_runs = 4
    max_timeout_s = 5

    def __init__(
            self,
            profile_manager: ProfileManager,
            providers_manager: ProvidersManager) -> None:
        """
        Parameters
        --
        - profile_manager - an instance of a profile manager.
        - providers_manager - an instance of a providers manager.
        """

        self._profile_manager = profile_manager
        self._providers_manager = providers_manager

    def _run_one(self, profile_id: str) -> (datetime, ProviderResult, datetime):
        """
        Description
        --
        Runs a single profile.

        Parameters
        --
        - profile_id - the Id of the profile to run.

        Returns
        --
        Tuple - start date, provider result, finish date
        """

        if not profile_id:
            raise ValueError("profile_id is required")

        # Load the profile
        profile = self._profile_manager.get(profile_id)

        # Create an instance of the provider associated with the profile
        provider_instance = self._providers_manager.instantiate(profile.provider_id)

        # Run the provider, by passing the profile parameters
        return (datetime.utcnow(), provider_instance.run(profile.provider_parameters), datetime.utcnow())

    def _run_many_parallel(self, profile_ids: List[str]) -> Generator[ProfileResult, None, None]:
        """
        Description
        --
        Runs multiple profiles, in a parallel mode.

        Parameters
        --
        - profile_ids - a list of the Ids of the profiles to run.

        Yields
        --
        Profile run results.
        """

        if not profile_ids:
            return

        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_parallel_profile_runs) as executor:
            for profile_id, future in [(profile_id, executor.submit(self._run_one, profile_id)) for profile_id in profile_ids]:
                profile_result = ProfileResult(profile_id, datetime.utcnow())
                try:
                    profile_result.result = future.result(timeout=self.max_timeout_s)
                except concurrent.futures.TimeoutError:
                    # Timed out
                    profile_result.result = ProviderResult(ResultStatus.TIMEOUT)
                finally:
                    profile_result.finished_at = datetime.utcnow()
                    yield profile_result
        """

        # TODO: Timeout on single threads
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_parallel_profile_runs) as executor:
            futures = {executor.submit(self._run_one, profile_id): profile_id for profile_id in profile_ids}
            for future in concurrent.futures.as_completed(futures):
                profile_id = futures[future]
                result = future.result()

                profile_result = ProfileResult(profile_id, result[0])
                profile_result.result = result[1]
                profile_result.finished_at = result[2]

                yield profile_result

    def run_many(self, profile_ids: List[str]) -> Generator[ProfileResult, None, None]:
        """
        Description
        --
        Runs many profiles.

        Parameters
        --
        - profile_ids - the list of profiles to run.

        Yields
        --
        Profile run results.
        """

        if not profile_ids:
            return

        yield from self._run_many_parallel(profile_ids)

    def run_all(self) -> Generator[ProfileResult, None, None]:
        """
        Description
        --
        Runs all available profiles.

        Yields
        --
        Profile run results.
        """

        yield from self.run_many(self._profile_manager.get_all_ids())


class CronRunner:
    """
    Description
    --
    Cron runner.
    """

    def __init__(
                self,
                profile_runner: ProfileRunner,
                result_handler: BaseResultHandler) -> None:
        """
        Parameters
        --
        - profile_runner - an instance of profile runner.
        - result_handler - an instance of result handler.
        """

        if profile_runner is None:
            raise ValueError("profile_runner is required!")

        self._profile_runner = profile_runner
        self._result_handler = result_handler

    def _run(self):
        # Run the profile
        for result in self._profile_runner.run_all():
            # And handle the result
            if self._result_handler is not None:
                self._result_handler.handle_result(result)

    def start(self) -> None:
        """
        Description
        --
        Sets up profile execution plans, according to their schedule.
        """

        # TODO: Setup actual cron job (using 3rd party lib) and run it.

        while True:
            # Every second, kick off a new run/handling in a new thread
            threading.Thread(target=self._run).start()

            time.sleep(1)
