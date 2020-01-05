# Import system
import abc
from typing import Any, Dict
from datetime import datetime


class ParameterMetadata:
    """
    Description
    --
    Meta description of a provider parameter.
    """

    def __init__(self, description: str, required: bool) -> None:
        """
        - description - the description of the parameter.
        - required - true or false, whether the parameter is required.
        """

        self.description = description
        self.required = required


class ProviderRun:
    """
    A provider run.
    """

    def __init__(
                self,
                started_at: datetime,
                finished_at: datetime,
                result: Any) -> None:
        """
        - started_at - When was the run started.
        - finished_at - When was the run finished.
        - result - The result of th run.
        """

        self.started_at = started_at
        self.finished_at = finished_at
        self.result = result

    @property
    def runtime_ms(self) -> int:
        return (self.finished_at - self.started_at).microseconds / 1000


class BaseProvider(abc.ABC):
    """
    Description
    --
    The base abstract provider class.
    - Basic run workflow.
    - Basic validation workflow.
    - Common parameters for all providers.
    """

    def run(self, parameters: Dict[str, str]) -> ProviderRun:
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
        A provider-specific format result.
        """

        # Validate parameters
        self.validate(parameters)

        # Run the implementation work-load
        started_at = datetime.utcnow()
        result = self._run(parameters)
        finished_at = datetime.utcnow()

        # Return the provider run
        return ProviderRun(started_at, finished_at, result)

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
            if key not in parameters:
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
            "Common.SampleParameter": ParameterMetadata(
                                        "Example of a common parameter", False)
        }

        # merge with the provider-specific parameters & return
        common_parameters.update(self._discover_parameters())
        return common_parameters

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
    def _run(self, parameters: Dict[str, str]) -> None:
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
        The provider specific result.
        """

        pass
