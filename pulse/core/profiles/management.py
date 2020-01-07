# System imports
from typing import List

# Local imports
from core.providers.management import ProvidersManager
from core.profiles.storage import BaseProfileStorage
from core.profiles.base import Profile


class ProfileManager:
    """
    Description
    --
    - Lists provider parameter expectations.
    - CRUD profiles.
    """

    def __init__(
                self,
                providers_manager: ProvidersManager,
                profile_storage: BaseProfileStorage) -> None:
        """
        - providers_manager - an instance of the providers manager.
        - profile_storage - an instance of profile storage implementation.
        """

        self._providers_manager = providers_manager
        self._profile_storage = profile_storage

    def get_all_ids(self) -> List[str]:
        """
        Description
        --
        Runs all available profiles Ids.

        Returns
        --
        A list of the Ids of all available profiles.
        """

        return self._profile_storage.get_all_ids()

    def get(self, profile_id: str) -> Profile:
        """
        Description
        --
        Gets a profile by Id.

        Parameters
        --
        - profile_id - the Id of the profile to get.

        Returns
        --
        The profile.
        """

        if not profile_id:
            raise ValueError("profile_id is required!")

        # Get the profile by Id
        profile = self._profile_storage.get(profile_id)

        # If the profile was not found ...
        if profile is None:
            raise ValueError("Profile not found by Id!")

        # Return the profile
        return profile

    def add(self, profile: Profile) -> str:
        """
        Description
        --
        Adds a profile. The parameters in the profile will be validated by
        the provider prior to adding.

        Parameters
        --
        - profile - the profile to add.

        Returns
        --
        The Id of the newly added profile.
        """

        if profile is None:
            raise ValueError("profile is required!")

        # The provider must be a valid available provider identifier
        if profile.provider_id not in self._providers_manager.get_all_ids():
            raise ValueError(
                            "Provider id '{provider_id}' not valid!"
                            .format(provider_id=profile.provider_id))

        # The parameters must be valid for that provider
        provider_instance = self._providers_manager.instantiate(
                            profile.provider_id)

        provider_instance.validate(profile.provider_parameters)

        # Store
        self._profile_storage.add(profile)

        # Return the profile Id
        return profile.profile_id

    def delete(self, profile_id: str) -> None:
        """
        Description
        --
        Deletes a profile by Id.

        Parameters
        --
        - profile_id - the Id of the profile to delete.
        """

        # Validations
        if not profile_id:
            raise ValueError("profile_id is required!")

        if not self._profile_storage.exists(profile_id):
            raise ValueError("Profile does not exist")

        # Replace the profile
        self._profile_storage.delete(profile_id)

    def update(self, profile: Profile) -> None:
        """
        Description
        --
        Updates a profile.

        Parameters
        --
        - profile - the updated profile.
        """

        # Validations
        if profile is None:
            raise ValueError("profile is required!")

        # Load the current version of the profile
        current_profile = self.get(profile.profile_id)

        if profile.provider_id != current_profile.provider_id:
            raise ValueError("Cannot change provider!")

        # If we have changed the parameters
        if profile.provider_parameters != current_profile.provider_parameters:
            # The parameters must be valid for that provider
            provider_instance = self._providers_manager.instantiate(
                                profile.provider_id)

            provider_instance.validate(profile.provider_parameters)

        # Update the profile
        self._profile_storage.update(profile)
