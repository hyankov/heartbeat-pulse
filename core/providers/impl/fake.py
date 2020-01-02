# Local application imports
from core.providers.base import BaseProvider, ParameterMetadata

class FakeProvider(BaseProvider):
    """
    Description
    --
    A Fake provider.
    - For testing purposes
    """

    isRan = False

    def _run(self, parameters):
        self.isRan = True

        return { "IsRan": True, "Parameters": parameters }

    def _validate(self, parameters):
        if (not parameters["FakeParam1"]):
            raise ValueError("'FakeParam1' value is required!")

    def _discover_parameters(self) -> dict:
        return {
            "FakeParam1": ParameterMetadata("Fake required param", True),
            "FakeParam2": ParameterMetadata("Fake optional param", False)
        }