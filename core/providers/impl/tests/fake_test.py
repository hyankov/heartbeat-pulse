import unittest

# Local application imports
from core.providers.impl.fake import FakeProvider


class TestFakeProvider(unittest.TestCase):
    def test_run_valid_params(self):
        # Arrange
        parameters = {
            "FakeParam1": "value 1",
            "FakeParam2": "value 2"
        }
        provider = FakeProvider()

        # Act
        provider.run(parameters)

        # Assert
        self.assertTrue(provider.isRan)

    def test_run_invalid_params(self):
        # Arrange
        parameters = {
            "FakeParam1": "",
            "FakeParam2": "value 2"
        }
        provider = FakeProvider()

        # Act & Assert
        with self.assertRaises(ValueError):
            provider.run(parameters)

        self.assertFalse(provider.isRan)

    def test_validate_validparams(self):
        # Arrange
        parameters = {
            "FakeParam1": "value 1",
            "FakeParam2": "value 2"
        }
        provider = FakeProvider()

        # Act
        provider.validate(parameters)

        # Assert
        self.assertTrue(True)

    def test_validate_invalidparams(self):
        # Arrange
        parameters = {
            "FakeParam2": "value 2"
        }
        provider = FakeProvider()

        # Act & Assert
        with self.assertRaises(ValueError):
            provider.validate(parameters)

    def test_discover_parameters(self):
        # Arrange
        provider = FakeProvider()

        # Act
        discovered_params = provider.discover_parameters()

        # Assert
        self.assertEqual(len(discovered_params), 3)
        self.assertTrue("FakeParam1" in discovered_params.keys())
        self.assertTrue("FakeParam2" in discovered_params.keys())
        self.assertTrue("Common.SampleParameter" in discovered_params.keys())
