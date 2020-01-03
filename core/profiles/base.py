# System imports
import uuid
from typing import Dict


class Profile:
    """
    Description
    --
    A profile model.
    """

    _profile_id = None          # type: str
    _provider_id = None         # type: str
    provider_parameters = {}    # type: Dict[str, str]
    # TODO: schedule = None

    @property
    def provider_id(self) -> str:
        return self._provider_id

    @property
    def profile_id(self) -> str:
        return self._profile_id

    def __init__(self, provider_id: str) -> None:
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
