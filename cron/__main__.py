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
                            FileProfileStorage("D:\\PythonProjects\\heartbeat\\heartbeat-pulse\\profiles.dat")),
                        providers_manager)
    # Start
    runner = CronRunner(profile_runner, ConsoleResultHandler())
    runner.start()
