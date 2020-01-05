# System imports
import uuid
from typing import Dict


class Profile:
    """
    Description
    --
    A profile model.
    """

    def __init__(self, name: str, provider_id: str) -> None:
        """
        - name - the name of the profile.
        - provider_id - the Id of the provider that will run this profile.
        """

        if not name:
            raise ValueError("name is required")

        if not provider_id:
            raise ValueError("provider_id is required")

        # Auto-generate the profile Id
        self.profile_id = uuid.uuid4().hex
        self.name = name
        self.provider_id = provider_id
        self.provider_parameters = {}  # type: Dict[str, str]
