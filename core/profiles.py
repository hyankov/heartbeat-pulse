import uuid

class ProfileManager:
    """
    Description
    --
    - Lists provider parameter expectations.
    - CRUD profiles.
    """

    _providers_manager = None
    _profile_storage = None

    def __init__(self, providers_manager, profile_storage):
        """
        Initializes the instance.

        Parameters
        --
        - providers_manager - an instance of the providers manager.
        - profile_storage - an instance of profile storage implementation.
        """

        if not providers_manager:
            raise ValueError("providers_manager is required!")

        if not profile_storage:
            raise ValueError("profile_storage is required!")

        self._providers_manager = providers_manager
        self._profile_storage = profile_storage

    def get_all_ids(self):
        """
        Description
        --
        Runs all available profiles Ids.

        Returns
        --
        A list of the Ids of all available profiles.
        """

        return self._profile_storage.get_all_ids()

    def get(self, profile_id):
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

        if not profile_id or profile_id == "":
            raise ValueError("profile_id is required!")

        # Get the profile by Id
        profile = self._profile_storage.get(profile_id)

        # If the profile was not found ...
        if not profile:
            raise ValueError("Profile not found by Id!")

        # Return the profile
        return profile

    def add(self, profile):
        """
        Description
        --
        Adds a profile. The parameters in the profile will be validated by the provider prior to adding.

        Parameters
        --
        - profile - the profile to add.

        Returns
        --
        The Id of the newly added profile.
        """

        if not profile:
            raise ValueError("profile is required!")

        # The provider must be a valid available provider identifier
        if profile.provider_id not in self._providers_manager.get_all_ids():
            raise ValueError("Provider id '{provider_id}' not valid!".format(provider_id = profile.provider_id))

        # The parameters must be valid for that provider
        provider_instance = self._providers_manager.instantiate(profile.provider_id)
        provider_instance.validate(profile.provider_parameters)

        # Store
        self._profile_storage.add(profile)

        # Return the profile Id
        return profile.profile_id

    def delete(self, profile_id):
        """
        Description
        --
        Deletes a profile by Id.

        Parameters
        --
        - profile_id - the Id of the profile to delete.
        """

        # Validations
        if not profile_id or profile_id == "":
            raise ValueError("profile_id is required!")

        if not self._profile_storage.exists(profile_id):
            raise ValueError("Profile does not exist")

        # Replace the profile
        self._profile_storage.delete(profile_id)

    def update(self, profile):
        """
        Description
        --
        Updates a profile.

        Parameters
        --
        - profile - the updated profile.
        """

        # Validations
        if not profile:
            raise ValueError("profile is required!")

        # Load the current version of the profile
        current_profile = self.get(profile.profile_id)

        if profile.provider_id != current_profile.provider_id:
            raise ValueError("Cannot change provider!")

        # If we have changed the parameters
        if profile.provider_parameters != current_profile.provider_parameters:
            # The parameters must be valid for that provider
            provider_instance = self._providers_manager.instantiate(profile.provider_id)
            provider_instance.validate(profile.provider_parameters)

        # Update the profile
        self._profile_storage.update(profile)

class InMemoryProfileStorage:
    """
    Description
    --
    An in-memory profile storage.
    """

    _profiles = {}

    def get_all_ids(self):
        """
        Description
        --
        Gets all available profiles Ids.

        Returns
        --
        A list of the Ids of all available profiles.
        """
        
        return list(self._profiles.keys())

    def get(self, profile_id):
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

        if not profile_id or profile_id == "":
            raise ValueError("profile_id is required!")

        # Find the profile by Id
        return self._profiles[profile_id]

    def add(self, profile):
        """
        Description
        --
        Adds a profile.

        Parameters
        --
        - profile - the profile to add.
        """

        if not profile:
            raise ValueError("profile is required!")

        # Store
        self._profiles[profile.profile_id] = profile

    def delete(self, profile_id):
        """
        Description
        --
        Deletes a profile by Id.

        Parameters
        --
        - profile_id - the Id of the profile to delete.
        """

        if not profile_id or profile_id == "":
            raise ValueError("profile_id is required!")

        del self._profiles[profile_id]

    def exists(self, profile_id):
        """
        Description
        --
        Checks if a profile exists.

        Parameters
        --
        - profile_id - the Id of the profile to check.
        """

        if not profile_id or profile_id == "":
            raise ValueError("profile_id is required!")

        return profile_id in self._profiles.keys()

    def update(self, profile):
        """
        Description
        --
        Updates a profile.

        Parameters
        --
        - profile - the updated profile.
        """

        if not profile:
            raise ValueError("profile is required!")

        # Replace the profile
        self._profiles[profile.profile_id] = profile

class Profile:
    """
    Description
    --
    A profile model.
    """

    _profile_id = None
    _provider_id = None
    provider_parameters = {}
    schedule = None #TODO

    @property
    def provider_id(self):
        return self._provider_id

    @property
    def profile_id(self):
        return self._profile_id

    def __init__(self, provider_id):
        """
        Initializes the instance.

        Parameters
        --
        - provider_id - the Id of the provider that will run this profile.
        """

        if not provider_id:
            raise ValueError("provider_id is required!")

        # Auto-generate the profile Id
        self._profile_id = uuid.uuid4().hex
        self._provider_id = provider_id