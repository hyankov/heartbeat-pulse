import unittest
from unittest.mock import MagicMock

# Local imports
from core.profiles import Profile, ProfileManager
from core.providers.management import ProvidersManager

class TestProfileManager(unittest.TestCase):
    _providers_manager = None
    _profiles = []

    def test_get_all_ids(self):
        # Arrange
        fake_providers_manager = MagicMock()
        fake_profile_storage = MagicMock()
        all_ids = [ "id1", "id2" ]
        fake_profile_storage.get_all_ids.return_value = all_ids
        profile_manager = ProfileManager(fake_providers_manager, fake_profile_storage)

        # Act
        result = profile_manager.get_all_ids()

        # Assert
        self.assertEqual(result, all_ids)

    def test_get_exists(self):
        # Arrange
        fake_providers_manager = MagicMock()
        fake_profile_storage = MagicMock()
        profile = Profile("random-provider-id")
        fake_profile_storage.get.return_value = profile
        profile_manager = ProfileManager(fake_providers_manager, fake_profile_storage)

        # Act
        result = profile_manager.get(profile.profile_id)

        # Assert
        self.assertEqual(result, profile)
        fake_profile_storage.get.assert_called_with(profile.profile_id)

    def test_add_valid(self):
        # Arrange
        provider_id = "random-provider-id"
        fake_provider_instance = MagicMock()
        fake_providers_manager = MagicMock()
        fake_providers_manager.get_all_ids.return_value = [ provider_id ]
        fake_providers_manager.instantiate.return_value = fake_provider_instance
        fake_profile_storage = MagicMock()
        profile = Profile(provider_id)
        profile.provider_parameters = { "SomeParam": "value 1"}
        profile_manager = ProfileManager(fake_providers_manager, fake_profile_storage)

        # Act
        profile_manager.add(profile)

        # Assert
        fake_providers_manager.instantiate.assert_called_with(profile.provider_id)
        fake_provider_instance.validate.assert_called_with(profile.provider_parameters)
        fake_profile_storage.add.assert_called_with(profile)

    def test_add_invalid_provider_id(self):
        # Arrange
        # Fake manager
        fake_providers_manager = MagicMock()
        fake_providers_manager.get_all_ids.return_value = [ "SomeOtherProvider" ]

        profile = Profile("SomeProvider")
        profile.provider_parameters = { "SomeParam": "value 1"}
        fake_profile_storage = MagicMock()
        profile_manager = ProfileManager(fake_providers_manager, fake_profile_storage)

        # Act & Assert
        with self.assertRaises(ValueError):
            profile_manager.add(profile)

    def test_delete_exists(self):
        # Arrange
        fake_providers_manager = MagicMock()
        fake_profile_storage = MagicMock()
        profile_manager = ProfileManager(fake_providers_manager, fake_profile_storage)
        profile_id = "random-id"
        fake_profile_storage.exists.return_value = True

        # Act
        profile_manager.delete(profile_id)

        # Assert
        fake_profile_storage.exists.assert_called_once_with(profile_id)
        fake_profile_storage.delete.assert_called_once_with(profile_id)

    def test_delete_not_exists(self):
        # Arrange
        fake_providers_manager = MagicMock()
        fake_profile_storage = MagicMock()
        profile_id = "random-id"
        fake_profile_storage.exists.return_value = False
        profile_manager = ProfileManager(fake_providers_manager, fake_profile_storage)

        # Act & Assert
        with self.assertRaises(ValueError):
            profile_manager.delete(profile_id)

        fake_profile_storage.exists.assert_called_once_with(profile_id)

    def test_update_exists_valid(self):
        # Arrange
        old_profile = Profile("random-provider-id")
        old_profile.provider_parameters = { "SomeParam": "value 1"}

        fake_provider_instance = MagicMock()
        
        fake_providers_manager = MagicMock()
        fake_providers_manager.instantiate.return_value = fake_provider_instance
        
        fake_profile_storage = MagicMock()
        fake_profile_storage.get.return_value = old_profile
        
        profile_manager = ProfileManager(fake_providers_manager, fake_profile_storage)

        # Act
        profile = Profile(old_profile.provider_id)
        profile.provider_parameters = { "SomeParam": "value 2"}
        profile_manager.update(profile)

        # Assert
        fake_profile_storage.get.assert_called_once_with(profile.profile_id)
        fake_providers_manager.instantiate.assert_called_with(profile.provider_id)
        fake_provider_instance.validate.assert_called_with(profile.provider_parameters)
        fake_profile_storage.update.assert_called_with(profile)

class TestProfile(unittest.TestCase):
    def test_provider_id(self):
        # Arrange
        provider_id = "random_provider_id"
        profile = Profile(provider_id)

        # Act & Assert
        self.assertEqual(profile.provider_id, provider_id)