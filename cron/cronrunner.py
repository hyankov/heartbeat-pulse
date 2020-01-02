# Import standard libraries
import threading
import time

class CronRunner:
    _profile_runner = None
    _results_handler = None

    def __init__(self, profile_runner, results_handler):
        self._profile_runner = profile_runner
        self._results_handler = results_handler

    def _run(self):
        # Run
        results = self._profile_runner.run_all_serial()
        
        # And handle the results
        self._results_handler.handle_results(results)

    def start(self):
        # TODO: Setup actual cron job (using 3rd party lib) and run it.

        def start_run_thread():
            runner_thread = threading.Thread(target=self._run, args=())
            runner_thread.daemon = True
            runner_thread.start()

        while True:
            # Every second, kick off a new run/handling in a new thread
            start_run_thread()

            time.sleep(1)

class ConsoleResultsHandler:
    def handle_result(self, result):
        print(result)

    def handle_results(self, results):
        for result in results:
            self.handle_result(result)
