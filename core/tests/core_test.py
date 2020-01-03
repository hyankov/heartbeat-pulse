# System imports
import unittest
import matplotlib.pyplot as plt

# Local application imports
from core.profiles.base import Profile
from core.profiles.management import ProfileManager
from core.profiles.storage import InMemoryProfileStorage
from core.providers.management import ProvidersManager
from core.running import ProfileRunner


class TestCore(unittest.TestCase):
    def test_end_to_end(self):
        providers_manager = ProvidersManager()
        profile_storage = InMemoryProfileStorage()
        profile_runner = ProfileManager(providers_manager, profile_storage)

        provider_ids = providers_manager.get_all_ids()

        # List all available providers and their properties
        for provider_id in provider_ids:
            print("\tProvider: " + provider_id)
            params = providers_manager.discover_parameters(provider_id)
            for param_key in params:
                param = params[param_key]
                print("\t\tName: " + param_key)
                print("\t\tDescription: " + param.description)
                print("\t\tRequired: " + str(param.required))
                print("\t\t---------------------------")

        ping_provider_id = provider_ids[0]

        # Ping 1
        profile = Profile(ping_provider_id)
        profile.provider_parameters = {"Target": "127.0.0.1"}
        profile_runner.add(profile)
        ping1_id = profile.profile_id

        # Ping 2
        profile = Profile(ping_provider_id)
        profile.provider_parameters = {"Target": "google.com"}
        profile_runner.add(profile)
        ping2_id = profile.profile_id

        # Fake Provider 1
        profile = Profile("FakeProvider")
        profile.provider_parameters = {
                                        "FakeParam1": "param 1",
                                        "FakeParam2": "param 1"
                                    }
        profile_runner.add(profile)

        profile_runner = ProfileRunner(profile_runner, providers_manager)

        results = []
        for x in range(10):
            results.extend(profile_runner.run_all_serial())

        ping1_results = filter(lambda res: res.profile_id == ping1_id, results)
        ping2_results = filter(lambda res: res.profile_id == ping2_id, results)

        # Plot
        plt.xlabel('Date-Time')
        plt.ylabel('Ping (ms)')

        plt.plot([o.result for o in ping1_results])
        plt.plot([o.result for o in ping2_results])
        plt.show()

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
