import unittest

# Local imports
from core.providers.management import ProvidersManager
from core.providers.impl.fake import FakeProvider


class TestProvidersManager(unittest.TestCase):
    _fake_provider_id = "FakeProvider"

    def test_get_all_ids(self):
        # Arrange
        providers_manager = ProvidersManager()

        # Act
        provider_ids = providers_manager.get_all_ids()

        # Assert
        self.assertGreaterEqual(len(provider_ids), 1)
        self.assertTrue(self._fake_provider_id in provider_ids)

    def test_discover_parameters(self):
        # Arrange
        providers_manager = ProvidersManager()

        # Act
        provider_params = providers_manager.discover_parameters(
                                            self._fake_provider_id)

        # Assert
        self.assertEqual(len(provider_params), 3)
        self.assertTrue("FakeParam1" in provider_params.keys())
        self.assertTrue("FakeParam2" in provider_params.keys())

    def test_instantiate(self):
        # Arrange
        providers_manager = ProvidersManager()

        # Act
        fake_provider_instance = providers_manager.instantiate(
                                                    self._fake_provider_id)

        # Assert
        self.assertIsInstance(fake_provider_instance, FakeProvider)


if __name__ == '__main__':
    unittest.main()
