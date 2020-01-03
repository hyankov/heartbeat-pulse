# Import standard libraries
import threading
import time

# Local imports
from cron.output import BaseResultsHandler
from core.profiles.management import ProfileManager
from core.running import ProfileRunner


class CronRunner:
    """
    Description
    --
    Cron runner.
    """

    _profile_manager = None     # type: ProfileManager
    _profile_runner = None      # type: ProfileRunner
    _results_handler = None     # type: BaseResultsHandler

    def __init__(
                self,
                profile_manager: ProfileManager,
                profile_runner: ProfileRunner,
                results_handler: BaseResultsHandler) -> None:
        """
        Initializes the instance.

        Parameters
        --
        - profile_manager - an instance of profile manager.
        - profile_runner - an instance of profile runner.
        - results_handler - an instance of results handler.
        """

        if profile_manager is None:
            raise ValueError("profile_manager is required!")

        if profile_runner is None:
            raise ValueError("profile_runner is required!")

        if results_handler is None:
            raise ValueError("results_handler is required!")

        self._profile_manager = profile_manager
        self._profile_runner = profile_runner
        self._results_handler = results_handler

    def _run(self):
        # Run
        results = self._profile_runner.run_all_serial()

        # And handle the results
        self._results_handler.handle_results(results)

    def start(self):
        """
        Description
        --
        Sets up profile execution plans, according to their schedule.
        """

        # TODO: Setup actual cron job (using 3rd party lib) and run it.

        def start_run_thread():
            runner_thread = threading.Thread(target=self._run, args=())
            runner_thread.daemon = True
            runner_thread.start()

        while True:
            # Every second, kick off a new run/handling in a new thread
            start_run_thread()

            time.sleep(1)
