# Import project dependencies
from core.profiles.management import ProfileManager
from core.profiles.storage import FileProfileStorage
from core.providers.management import ProvidersManager
from cron.output import ConsoleResultHandler
from cron.running import CronRunner, ProfileRunner


"""
When the script is executed.
"""
if __name__ == '__main__':
    # Resolve dependencies
    providers_manager = ProvidersManager()
    profile_runner = ProfileRunner(
                        ProfileManager(
                            providers_manager,
                            FileProfileStorage()),
                        providers_manager)
    results_handler = ConsoleResultHandler()

    # Run
    runner = CronRunner(profile_runner, results_handler)
    runner.start()
