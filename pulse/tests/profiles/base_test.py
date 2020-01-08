import unittest

# Local imports
from profiles import Profile


class TestProfile(unittest.TestCase):
    def test_provider_id(self):
        # Arrange
        name = "random name"
        provider_id = "random_provider_id"
        profile = Profile(name, provider_id, 1)

        # Act & Assert
        self.assertEqual(profile.name, name)
        self.assertEqual(profile.provider_id, provider_id)
