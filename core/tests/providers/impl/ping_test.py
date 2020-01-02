import unittest

# Local application imports
from core.providers.impl.ping import PingProvider

class TestPingProvider(unittest.TestCase):
    def test_run_valid_params(self):
        # Arrange
        parameters = {
            "Target": "127.0.0.1"
        }
        provider = PingProvider()

        # Act
        provider.run(parameters)

        # Assert
        self.assertTrue(True)

    def test_run_invalid_params(self):
        # Arrange
        parameters = {
            "Target": ""
        }
        provider = PingProvider()

        # Act & Assert
        with self.assertRaises(ValueError):
            provider.run(parameters)

    def test_validate_validparams(self):
        # Arrange
        parameters = {
            "Target": "127.0.0.1"
        }
        provider = PingProvider()

        # Act
        provider.validate(parameters)

        # Assert
        self.assertTrue(True)

    def test_validate_invalidparams(self):
        # Arrange
        parameters = {}
        provider = PingProvider()

        # Act & Assert
        with self.assertRaises(ValueError):
            provider.validate(parameters)

    def test_discover_parameters(self):
        # Arrange
        ping_provider = PingProvider()

         # Act
        discovered_params = ping_provider.discover_parameters()

        # Assert
        self.assertEqual(len(discovered_params), 2)
        self.assertTrue("Target" in discovered_params.keys())
        self.assertTrue("Common.SampleParameter" in discovered_params.keys())