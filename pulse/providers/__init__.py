# System imports
import abc
import importlib
import os
import pkgutil
import sys
from enum import Enum
from typing import Dict, List, NamedTuple


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
    UNKNOWN = 'UNKNOWN'


class ProviderResult:
    """
    Description
    --
    The result of a  provider run.
    """

    def __init__(self, status: ResultStatus, value: int = None) -> None:
        """
        Parameters
        --
        - status - the status of the result.
        - value - the value of the result.
        """

        self.status = status                            # type: ResultStatus
        self.value = value if value is not None else 0  # type: int


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

        # Validate parameters
        self.validate(parameters)

        # Run the implementation work-load and return the result
        return self._run(parameters)

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
            if key not in parameters or not parameters[key]:
                raise ValueError("Param '{}' is required!".format(key))

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


class ProvidersManager:
    """
    Description
    --
    - Lists available providers.
    - Creates an instance of a provider.
    """

    # Initialized once, at loading and then cached
    _providers = {}     # Dict[str, str]

    def __init__(self) -> None:
        """
        Loads and caches the list of providers.
        """

        impl_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'impl')
        for (module_loader, name, ispkg) in pkgutil.iter_modules([impl_dir]):
            importlib.import_module('.impl.' + name, __package__)

        # Find all classes that inherit from the base (works because the
        # implementation modules are imported)
        providers = BaseProvider.__subclasses__()
        for provider in providers:
            # Dictionary of provider_id:provider_module
            self._providers[provider.__name__] = provider.__module__

    def get_all_ids(self) -> List[str]:
        """
        Description
        --
        Gets all available provider Ids.

        Returns
        --
        A list of the Ids of all available providers.
        """

        return list(self._providers.keys())

    def discover_parameters(self, provider_id: str) -> Dict[
                                                        str,
                                                        ParameterMetadata]:
        """
        Description
        --
        Discovers the parameters a provider would expect at runtime.

        Parameters
        --
        - provider_id - the Id of the provider of which we want to discover
        the runtime parameters.

        Returns
        --
        A dictionary of the parameters a provider would expect at runtime.
        """

        if not provider_id:
            raise ValueError("provider_id is required!")

        # Create an instance of the provider
        provider_instance = self.instantiate(provider_id)

        # Ask the instance of the provider to reveal its runtime parameters.
        return provider_instance.discover_parameters()

    def instantiate(self, provider_id: str) -> BaseProvider:
        """
        Description
        --
        Creates an insance of a provider.

        Parameters
        --
        - provider_id - the Id of the provider which we want to create an
        instance of.

        Returns
        --
        An instance of the provider.
        """

        if not provider_id:
            raise ValueError("provider_id is required!")

        if self._providers[provider_id] is None:
            raise ValueError("Provider with Id '{}' not found!".format(provider_id))

        # Use 'reflection' to create an instance
        provider_class_ = getattr(
                            sys.modules[self._providers[provider_id]],
                            provider_id)

        # Return the instance
        return provider_class_()
