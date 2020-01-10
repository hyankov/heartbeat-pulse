# System imports
import abc
from typing import List, Dict
from os import path
import os
import yaml

# Local imports
from . import Profile


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

        # Get the profile by Id
        profile = self._profiles[profile_id]

        # If the profile was not found ...
        if profile is None:
            raise ValueError("Profile not found by Id!")

        # Return the profile
        return profile


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
        profiles = []  # type: List[Profile]

        if path.exists(self._file_path):
            if os.stat(self._file_path).st_size > 0:
                with open(self._file_path, 'r') as file:
                    profiles = list(yaml.load(file, Loader=yaml.FullLoader))

        return {profile.id: profile for profile in profiles}

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

        # Get the profile by Id
        profile = self._get_profiles()[profile_id]

        # If the profile was not found ...
        if profile is None:
            raise ValueError("Profile not found by Id!")

        # Return the profile
        return profile
