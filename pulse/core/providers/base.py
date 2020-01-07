# Import system
import abc
from typing import Any, Dict, NamedTuple
from enum import Enum


class ParameterMetadata(NamedTuple):
    """
    Description
    --
    Meta description of a provider parameter.
    """

    description: str
    required: bool = False


class ResultStatus(Enum):
    """
    Description
    --
    The status of a provider run result.
    """

    GREEN = 'GREEN'
    YELLOW = 'YELLOW'
    RED = 'RED'
    ERROR = 'ERROR'
    TIMEOUT = 'TIMEOUT'


class ProviderResult:
    """
    Description
    --
    The result of a  provider run.
    """

    def __init__(self, status: ResultStatus) -> None:
        """
        Parameters
        --
        - status - the status of the result.
        """

        self.status = status    # type: ResultStatus
        self.value = None       # type: Any


class BaseProvider(abc.ABC):
    """
    Description
    --
    The base abstract provider class.
    - Basic run workflow.
    - Basic validation workflow.
    - Common parameters for all providers.
    """

    def _discover_parameters(self) -> Dict[str, ParameterMetadata]:
        """
        Description
        --
        Any parameters specifically required by the provider implementation.
        Can be overriden.

        Returns
        --
        The parameters, specific to the provider implementation, if any.
        """

        return {}  # type Dict[str, ParameterMetadata]

    def _validate(self, parameters: Dict[str, str]) -> None:
        """
        Description
        --
        Additional validation to be performed by the provider implementation.
        Can be overriden.

        Parameters
        --
        - parameters - the parameters to pass to the provider instance to
        validate.
        """

        pass

    @abc.abstractmethod
    def _run(self, parameters: Dict[str, str]) -> ProviderResult:
        """
        Description
        --
        The actual workload by the provider implementation.
        Must be overriden.

        Parameters
        --
        - parameters - the parameters to pass to the provider instance at
        runtime.

        Returns
        --
        The run result.
        """

        pass

    def run(self, parameters: Dict[str, str]) -> ProviderResult:
        """
        Description
        --
        Executes the provider, with the passed parameters,
        after their validation.

        Parameters
        --
        - parameters - the parameters to pass to the provider instance at
        runtime.

        Returns
        --
        The run result.
        """

        try:
            # Validate parameters
            self.validate(parameters)

            # Run the implementation work-load and return the result
            return self._run(parameters)
        except Exception:
            # TODO: Log
            return ProviderResult(ResultStatus.ERROR)

    def validate(self, parameters: Dict[str, str]) -> None:
        """
        Description
        --
        Validates the parameters, which is done by a basic check if the
        required parameters are present, plus implementation-specific
        validation. Will raise exception if the parameters are invalid for
        the provider.

        Parameters
        --
        - parameters - the parameters to pass to the provider instance at
        runtime.
        """

        # All *required* parameters ...
        params = self.discover_parameters()
        for key in filter(lambda p_key: params[p_key].required, params):
            # ... must be present
            if key not in parameters or parameters[key] is None or parameters[key] == "":
                raise ValueError("'{name}' is required!".format(name=key))

        # ask the implementation to validate the parameters
        self._validate(parameters)

    def discover_parameters(self) -> Dict[str, ParameterMetadata]:
        """
        Description
        --
        Discovers the parameters that the provider would require in runtime.

        Returns
        --
        The common parameters for all providers, plus the provider specific
        parameters.
        """

        common_parameters = {
            # A sample of a common parameter for all providers
            "Common.SampleParameter": ParameterMetadata(description="Example of a common parameter")
        }

        # merge with the provider-specific parameters & return
        common_parameters.update(self._discover_parameters())
        return common_parameters
