# System imports
import uuid
from typing import Dict


class Profile:
    """
    Description
    --
    A profile model.
    """

    def __init__(self, name: str, provider_id: str, run_every_x_seconds: int) -> None:
        """
        Parameters
        --
        - name - the name of the profile.
        - provider_id - the Id of the provider that will run this profile.
        - run_every_x_seconds - every how many seconds should the profile be ran?
        """

        # Auto-generate the profile Id
        self.profile_id = uuid.uuid4().hex

        # Set the initializer parameters as properties
        self.name = name
        self.provider_id = provider_id
        self.run_every_x_seconds = run_every_x_seconds
        self.provider_parameters = {}  # type: Dict[str, str]

        # Validate the properties
        self.self_validate()

    def self_validate(self) -> None:
        """
        Self-validates, post-initialization.
        """

        if not self.name:
            raise ValueError("name is required")

        if len(self.name) > 100:
            raise ValueError("name max lenght is 100 characters")

        if not self.provider_id:
            raise ValueError("provider_id is required")

        if self.run_every_x_seconds is None:
            raise ValueError("run_every_x_seconds is required")

        if self.run_every_x_seconds <= 0:
            raise ValueError("run_every_x_seconds must be > 0")

        if not self.profile_id:
            raise ValueError("profile_id is required")
