# Standard library imports
import abc
import pickle
from typing import List, Dict
from os import path
import os

# Local imports
from core.profiles.base import Profile


class BaseProfileStorage(abc.ABC):
    """
    Description
    --
    The base abstract profile storage.
    """

    @abc.abstractmethod
    def get_all_ids(self) -> List[str]:
        """
        Description
        --
        Gets all available profiles Ids.
        Must be overriden.

        Returns
        --
        A list of the Ids of all available profiles.
        """

        pass

    @abc.abstractmethod
    def get(self, profile_id: str) -> Profile:
        """
        Description
        --
        Gets a profile by Id.
        Must be overriden.

        Parameters
        --
        - profile_id - the Id of the profile to get.

        Returns
        --
        The profile.
        """

        pass

    @abc.abstractmethod
    def add(self, profile: Profile) -> None:
        """
        Description
        --
        Adds a profile.
        Must be overriden.

        Parameters
        --
        - profile - the profile to add.
        """

        pass

    @abc.abstractmethod
    def delete(self, profile_id: str) -> None:
        """
        Description
        --
        Deletes a profile by Id.
        Must be overriden.

        Parameters
        --
        - profile_id - the Id of the profile to delete.
        """

        pass

    @abc.abstractmethod
    def exists(self, profile_id: str) -> bool:
        """
        Description
        --
        Checks if a profile exists.
        Must be overriden.

        Parameters
        --
        - profile_id - the Id of the profile to check.
        """

        pass

    @abc.abstractmethod
    def update(self, profile: Profile) -> None:
        """
        Description
        --
        Updates a profile.
        Must be overriden.

        Parameters
        --
        - profile - the updated profile.
        """

        pass


class InMemoryProfileStorage(BaseProfileStorage):
    """
    Description
    --
    An in-memory profile storage.
    """

    _profiles = {}  # type: Dict[str, Profile]

    def get_all_ids(self) -> List[str]:
        """
        Description
        --
        Gets all available profiles Ids.

        Returns
        --
        A list of the Ids of all available profiles.
        """

        return list(self._profiles.keys())

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

        # Find the profile by Id
        return self._profiles[profile_id]

    def add(self, profile: Profile) -> None:
        """
        Description
        --
        Adds a profile.

        Parameters
        --
        - profile - the profile to add.
        """

        if profile is None:
            raise ValueError("profile is required!")

        # Store
        self._profiles[profile.profile_id] = profile

    def delete(self, profile_id: str) -> None:
        """
        Description
        --
        Deletes a profile by Id.

        Parameters
        --
        - profile_id - the Id of the profile to delete.
        """

        if not profile_id:
            raise ValueError("profile_id is required!")

        del self._profiles[profile_id]

    def exists(self, profile_id: str) -> bool:
        """
        Description
        --
        Checks if a profile exists.

        Parameters
        --
        - profile_id - the Id of the profile to check.
        """

        if not profile_id:
            raise ValueError("profile_id is required!")

        return profile_id in self._profiles.keys()

    def update(self, profile: Profile) -> None:
        """
        Description
        --
        Updates a profile.

        Parameters
        --
        - profile - the updated profile.
        """

        if profile is None:
            raise ValueError("profile is required!")

        # Replace the profile
        self._profiles[profile.profile_id] = profile


class FileProfileStorage(BaseProfileStorage):
    """
    Description
    --
    A file-based profile storage. Serializes and deserializes data to file.
    """

    _file_path = None    # type: str

    def __init__(self, data_file: str) -> None:
        if not data_file:
            raise ValueError("data_file is required!")

        self._file_path = data_file

    def _get_profiles(self) -> Dict[str, Profile]:
        profiles = {}  # type: Dict[str, Profile]

        if path.exists(self._file_path):
            if os.stat(self._file_path).st_size > 0:
                with open(self._file_path, 'rb') as file:
                    profiles = pickle.load(file)

        return profiles

    def _set_profiles(self, profiles: Dict[str, Profile]) -> None:
        with open(self._file_path, 'wb') as file:
            pickle.dump(profiles, file)

    def get_all_ids(self) -> List[str]:
        """
        Description
        --
        Gets all available profiles Ids.

        Returns
        --
        A list of the Ids of all available profiles.
        """

        return list(self._get_profiles().keys())

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

        # Find the profile by Id
        return self._get_profiles()[profile_id]

    def add(self, profile: Profile) -> None:
        """
        Description
        --
        Adds a profile.

        Parameters
        --
        - profile - the profile to add.
        """

        if profile is None:
            raise ValueError("profile is required!")

        profiles = self._get_profiles()
        profiles[profile.profile_id] = profile
        self._set_profiles(profiles)

    def delete(self, profile_id: str) -> None:
        """
        Description
        --
        Deletes a profile by Id.

        Parameters
        --
        - profile_id - the Id of the profile to delete.
        """

        if not profile_id:
            raise ValueError("profile_id is required!")

        profiles = self._get_profiles()
        del profiles[profile_id]
        self._set_profiles(profiles)

    def exists(self, profile_id: str) -> bool:
        """
        Description
        --
        Checks if a profile exists.

        Parameters
        --
        - profile_id - the Id of the profile to check.
        """

        if not profile_id:
            raise ValueError("profile_id is required!")

        return profile_id in self._get_profiles().keys()

    def update(self, profile: Profile) -> None:
        """
        Description
        --
        Updates a profile.

        Parameters
        --
        - profile - the updated profile.
        """

        if profile is None:
            raise ValueError("profile is required!")

        # Replace the profile
        profiles = self._get_profiles()
        profiles[profile.profile_id] = profile
        self._set_profiles(profiles)
