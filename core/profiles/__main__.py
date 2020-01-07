# System imports

# Local imports
from core.providers.management import ProvidersManager
from core.profiles.storage import FileProfileStorage
from core.profiles.management import ProfileManager
from core.profiles.base import Profile


"""
When the script is executed.
"""
if __name__ == '__main__':
    # Resolve dependencies
    providers_manager = ProvidersManager()
    profile_storage = FileProfileStorage("D:\\PythonProjects\\heartbeat\\heartbeat-pulse\\profiles.dat")
    profile_manager = ProfileManager(providers_manager, profile_storage)

    def main_menu():
        print("\n\nProfile management:")
        print("1. List")
        print("2. Add")
        print("x. exit")
        return input("> ")

    def list_menu():
        print("\n\nList:")
        i = 1
        for id in profile_manager.get_all_ids():
            print("{i} {id}".format(i=i, id=id))
            i += 1

        print("x. exit")

    def add_menu():
        print("\n\nAdd profile:")
        print("\tChoose provider:")
        i = 1
        for pid in providers_manager.get_all_ids():
            print("\t\t{i}. {pid}".format(i=i, pid=pid))
            i += 1

        provider_id = providers_manager.get_all_ids()[int(input("> ")) - 1]

        name = input("\tProfile name:")
        provider_parameters = {}
        params = providers_manager.discover_parameters(provider_id)
        for param_key in params:
            param = params[param_key]
            print("\t\t\tName: " + param_key)
            print("\t\t\tDescription: " + param.description)
            print("\t\t\tRequired: " + str(param.required))
            provider_parameters[param_key] = input("\t\t\tValue: ")
            print()

        profile = Profile(name, provider_id, "1")
        profile.provider_parameters = provider_parameters
        profile_manager.add(profile)

    # Create the menu
    while True:
        result = main_menu()
        if result == "1":
            list_menu()
        elif result == "2":
            add_menu()
        elif result == "x":
            break
