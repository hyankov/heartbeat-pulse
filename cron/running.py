# Import standard libraries
import threading
import time
from typing import List, Generator
import concurrent.futures

# Local imports
from core.providers.management import ProvidersManager
from core.profiles.management import ProfileManager
from cron.output import BaseResultHandler, ProfileRun


class ProfileRunner:
    """
    Description
    --
    - Runs profiles.
    """

    def __init__(
            self,
            profile_manager: ProfileManager,
            providers_manager: ProvidersManager) -> None:
        """
        - profile_manager - an instance of a profile manager.
        - providers_manager - an instance of a providers manager.
        """

        self._profile_manager = profile_manager
        self._providers_manager = providers_manager

    def run_one(self, profile_id: str) -> ProfileRun:
        """
        Description
        --
        Runs a single profile.

        Parameters
        --
        - profile_id - the Id of the profile to run.

        Returns
        --
        The profile run result.
        """

        # Load the profile
        profile = self._profile_manager.get(profile_id)

        # Create an instance of the provider associated with the profile
        provider_instance = self._providers_manager.instantiate(profile.provider_id)

        # Run the provider, by passing the profile parameters
        provider_run = provider_instance.run(profile.provider_parameters)

        # And return it
        return ProfileRun(profile.profile_id, profile.name, provider_run)

    def _run_many_serial(self, profile_ids: List[str]) -> Generator[ProfileRun, None, None]:
        """
        Description
        --
        Runs multiple profiles, in a serial mode.

        Parameters
        --
        - profile_ids - a list of the Ids of the profiles to run.

        Returns
        --
        A list of all profile run results.
        """

        # with every profile Id in the list ...
        for profile_id in profile_ids:
            # run it
            yield self.run_one(profile_id)

    def _run_many_parallel(self, profile_ids: List[str]) -> Generator[ProfileRun, None, None]:
        """
        Description
        --
        Runs multiple profiles, in a parallel mode.

        Parameters
        --
        - profile_ids - a list of the Ids of the profiles to run.

        Returns
        --
        A list of all profile run results.
        """

        # with every profile Id in the list ...
        for profile_id in profile_ids:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(self.run_one, profile_id)

                # add it to the list of results
                yield future.result()

    def run_many(self, profile_ids: List[str], serial: bool) -> Generator[ProfileRun, None, None]:
        if serial:
            yield from self._run_many_serial(profile_ids)
        else:
            yield from self._run_many_parallel(profile_ids)

    def run_all(self, serial: bool = True) -> Generator[ProfileRun, None, None]:
        """
        Description
        --
        Runs all available profiles.

        Parameters
        --
        - serial - true to run in serial mode, false to run in parallel.

        Returns
        --
        A list of all profile run results.
        """

        yield from self.run_many(self._profile_manager.get_all_ids(), serial)


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
        - profile_runner - an instance of profile runner.
        - results_handler - an instance of result handler.
        """

        self._profile_runner = profile_runner
        self._result_handler = result_handler

    def _run(self):
        # Run
        for result in self._profile_runner.run_all(False):
            # And handle the result
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
            runner_thread = threading.Thread(target=self._run, args=())
            runner_thread.daemon = True
            runner_thread.start()

            time.sleep(1)
