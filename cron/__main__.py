# Import project dependencies
from core.running import ProfileRunner
from core.profiles import InMemoryProfileStorage, ProfileManager
from core.providers.management import ProvidersManager
from cron.cronrunner import CronRunner, ConsoleResultsHandler

"""
When the script is executed.
"""
if __name__ == '__main__':
    # Resolve dependencies
    profile_runner = ProfileRunner(ProfileManager(ProvidersManager(), InMemoryProfileStorage()), ProvidersManager())
    results_handler = ConsoleResultsHandler()

    # Run
    runner = CronRunner(profile_runner, results_handler)
    runner.start()