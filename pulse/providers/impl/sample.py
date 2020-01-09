# Import system
from typing import Dict

# Local application imports
from .. import BaseProvider, ParameterMetadata, ProviderResult, ResultStatus


class SampleProvider(BaseProvider):
    """
    Description
    --
    A sample provider.
    """

    _p_sample_param = "SampleParam"

    def _run(self, parameters: Dict[str, str]) -> ProviderResult:
        # get the expected parameter
        param_value = parameters[self._p_sample_param]

        # TODO: Perform logic
        result = ProviderResult(ResultStatus.GREEN, 0)

        # and return result
        return result

    def _validate(self, parameters: Dict[str, str]) -> None:
        # Additional parameter validation
        param = self._p_sample_param
        param_value = parameters[param]

        # TODO: Do whatever with param_value and if things are not kosher, raise ValueError

    def _discover_parameters(self) -> Dict[str, ParameterMetadata]:
        return {
            self._p_sample_param: ParameterMetadata(description="Sample param description", required=True)
        }
