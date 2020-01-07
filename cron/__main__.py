# Import project dependencies
from core.profiles.management import ProfileManager
from core.profiles.storage import FileProfileStorage
from core.providers.management import ProvidersManager
from cron.output import ConsoleResultHandler
from cron.running import ProfileRunner


"""
When the script is executed.
"""
if __name__ == '__main__':
    print("Wiring dependencies ...")
    
    # Resolve dependencies
    providers_manager = ProvidersManager()
    runner = ProfileRunner(
                            ProfileManager(
                                providers_manager,
                                FileProfileStorage("D:\\PythonProjects\\heartbeat\\heartbeat-pulse\\profiles.dat")),
                            providers_manager,
                            ConsoleResultHandler())

    # Start
    runner.start()
