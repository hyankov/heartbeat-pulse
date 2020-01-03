# Import project dependencies
from core.profiles.management import ProfileManager
from core.profiles.storage import InMemoryProfileStorage
from core.providers.management import ProvidersManager
from core.running import ProfileRunner
from cron.output import ConsoleResultsHandler
from cron.running import CronRunner

"""
When the script is executed.
"""
if __name__ == '__main__':
    # Resolve dependencies
    providers_manager = ProvidersManager()
    profile_storage = InMemoryProfileStorage()
    profile_manager = ProfileManager(providers_manager, profile_storage)
    profile_runner = ProfileRunner(profile_manager, providers_manager)
    results_handler = ConsoleResultsHandler()

    # Run
    runner = CronRunner(profile_manager, profile_runner, results_handler)
    runner.start()
