# Local imports
from core.providers.management import ProvidersManager
from core.profiles.management import ProfileManager
from core.profiles.base import Profile


class ConsoleUI:
    def __init__(self, profile_manager: ProfileManager, providers_manager: ProvidersManager):
        """
        Parameters
        --
        - profile_manager - an inst
        """

        if profile_manager is None:
            raise ValueError("profile_manager is required!")

        if providers_manager is None:
            raise ValueError("providers_manager is required!")

        self.profile_manager = profile_manager
        self.providers_manager = providers_manager

    def start(self, config_name) -> None:
        """
        When the script is executed.
        """

        def main_menu():
            print("\n\nProfile management:")
            print("1. List")
            print("2. Add")
            print("x. exit")
            return input("> ")

        def list_menu():
            print("\n\nList:")
            i = 1
            for id in self.profile_manager.get_all_ids():
                print("{i} {id}".format(i=i, id=id))
                i += 1

            print("x. exit")

        def add_menu():
            print("\n\nAdd profile:")
            print("\tChoose provider:")
            i = 1
            for pid in self.providers_manager.get_all_ids():
                print("\t\t{i}. {pid}".format(i=i, pid=pid))
                i += 1

            provider_id = self.providers_manager.get_all_ids()[int(input("> ")) - 1]

            name = input("\tProfile name:")
            schedule = int(input("\tSchedule:"))
            provider_parameters = {}
            params = self.providers_manager.discover_parameters(provider_id)
            for param_key in params:
                param = params[param_key]
                print("\t\t\tName: " + param_key)
                print("\t\t\tDescription: " + param.description)
                print("\t\t\tRequired: " + str(param.required))
                provider_parameters[param_key] = input("\t\t\tValue: ")
                print()

            profile = Profile(name, provider_id, schedule)
            profile.provider_parameters = provider_parameters
            self.profile_manager.add(profile)

        # Create the menu
        while True:
            result = main_menu()
            if result == "1":
                list_menu()
            elif result == "2":
                add_menu()
            elif result == "x":
                break
