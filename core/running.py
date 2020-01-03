# System imports
from datetime import datetime
from typing import List, Any

# Local imports
from core.providers.management import ProvidersManager
from core.profiles.management import ProfileManager


class ProfileRunResult:
    """
    Description
    --
    The result of a profile run.
    """

    _datetime_of_run = None     # type: datetime
    _result = None              # type: Any
    _profile_id = None          # type: str

    def __init__(self, profile_id: str, result: Any) -> None:
        """
        Initializes the instance.

        Parameters
        --
        - profile_id - the Id of the profile that ran.
        - result - the result of the run.
        """

        self._profile_id = profile_id
        self._result = result
        self._datetime_of_run = datetime.now()

    @property
    def result(self) -> Any:
        return self._result

    @property
    def profile_id(self) -> str:
        return self._profile_id

    @property
    def datetime_of_run(self) -> datetime:
        return self._datetime_of_run


class ProfileRunner:
    """
    Description
    --
    - Runs profiles.
    """

    _profile_manager = None     # type: ProfileManager
    _providers_manager = None   # type: ProvidersManager

    def __init__(
            self,
            profile_manager: ProfileManager,
            providers_manager: ProvidersManager) -> None:
        """
        Description
        --
        Initializes the instance.

        Parameters
        --
        - profile_manager - an instance of a profile manager.
        - providers_manager - an instance of a providers manager.
        """

        if profile_manager is None:
            raise ValueError("profile_manager is required!")

        if providers_manager is None:
            raise ValueError("providers_manager is required!")

        self._profile_manager = profile_manager
        self._providers_manager = providers_manager

    def run_all_serial(self) -> List[ProfileRunResult]:
        """
        Description
        --
        Runs all available profiles, in a serial (one after the other) mode.

        Returns
        --
        A list of all profile run results.
        """

        results = []    # type: List[ProfileRunResult]

        # With every available profile Id
        for profile_id in self._profile_manager.get_all_ids():
            # Run the profile
            profile_run_result = self.run_one(profile_id)

            # Add the result to the list of results
            results.append(profile_run_result)

        # Return the list of results
        return results

    def run_all_parallel(self) -> List[ProfileRunResult]:
        """
        Description
        --
        Runs all available profiles, in a parallel (at the same time) mode.

        Returns
        --
        A list of all profile run results.
        """

        raise NotImplementedError()

    def run_one(self, profile_id: str) -> ProfileRunResult:
        """
        Description
        --
        Runs a single profile.

        Parameters
        --
        - profile_id - the Id of the profile to run.

        Returns
        --
        The profile run result.
        """

        if not profile_id:
            raise ValueError("profile_id is required!")

        # Load the profile
        profile = self._profile_manager.get(profile_id)

        # Create an instance of the provider associated with the profile
        provider_instance = self._providers_manager.instantiate(
                                                    profile.provider_id)

        # Run the provider, by passing the profile parameters
        result = provider_instance.run(profile.provider_parameters)

        # Wrap the result
        profile_run_result = ProfileRunResult(profile.profile_id, result)

        # And return it
        return profile_run_result

    def run_many_serial(self, profile_ids: List[str]):
        """
        Description
        --
        Runs multiple profiles, in a serial mode.

        Parameters
        --
        - profile_ids - a list of the Ids of the profiles to run.

        Returns
        --
        A list of all profile run results.
        """

        results = []    # type: List[ProfileRunResult]

        # with every profile Id in the list ...
        for profile_id in profile_ids:
            # run it
            profile_run_result = self.run_one(profile_id)

            # add it to the list of results
            results.append(profile_run_result)

        # return the list of resutls
        return results

    def run_many_parallel(self, profile_ids: List[str]) -> List[
                                                            ProfileRunResult]:
        """
        Description
        --
        Runs multiple profiles, in a parallel mode.

        Parameters
        --
        - profile_ids - a list of the Ids of the profiles to run.

        Returns
        --
        A list of all profile run results.
        """

        raise NotImplementedError()
