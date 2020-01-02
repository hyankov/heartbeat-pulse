# Standard library imports
import abc

class BaseProvider(abc.ABC):
    """
    Description
    --
    The base abstract provider class.
    - Basic run workflow.
    - Basic validation workflow.
    - Common parameters for all providers.
    """

    def run(self, parameters):
        """
        Description
        --
        Executes the provider, with the passed parameters, after their validation.

        Parameters
        --
        - parameters - the parameters to pass to the provider instance at runtime.

        Returns
        --
        A provider-specific format result.
        """

        # Validate parameters
        self.validate(parameters)

        # Run the implementation work-load
        result = self._run(parameters)

        # Return the provider result
        return result

    def validate(self, parameters: dict):
        """
        Description
        --
        Validates the parameters, which is done by a basic check if the required parameters are present,
        plus implementation-specific validation. Will raise exception if the parameters are invalid for the provider.

        Parameters
        --
        - parameters - the parameters to pass to the provider instance at runtime.
        """

        # All *required* parameters ...
        params = self.discover_parameters()
        for required_parameter_key in filter(lambda param_key: params[param_key].required, params):
            # ... must be present
            if required_parameter_key not in parameters:
                raise ValueError("'{required_parameter_name}' is required!".format(required_parameter_name = required_parameter_key))

        # ask the implementation to validate the parameters
        self._validate(parameters)

    def discover_parameters(self) -> dict:
        """
        Description
        --
        Discovers the parameters that the provider would require in runtime.
        
        Returns
        --
        The common parameters for all providers, plus the provider specific parameters.
        """

        common_parameters = {
            # A sample of a common parameter for all providers
            "Common.SampleParameter": ParameterMetadata("Example of a common parameter", False)
        }

        # merge with the provider-specific parameters & return
        common_parameters.update(self._discover_parameters())
        return common_parameters

    def _discover_parameters(self) -> dict:
        """
        Description
        --
        Any parameters specifically required by the provider implementation.
        Can be overriden.

        Returns
        --
        The parameters, specific to the provider implementation, if any.
        """

        return {}

    def _validate(self, parameters):
        """
        Description
        --
        Additional validation to be performed by the provider implementation.
        Can be overriden.

        Parameters
        --
        - parameters - the parameters to pass to the provider instance to validate.
        """

        pass

    @abc.abstractmethod
    def _run(self, parameters):
        """
        Description
        --
        The actual workload by the provider implementation.
        Must be overriden.

        Parameters
        --
        - parameters - the parameters to pass to the provider instance at runtime.

        Returns
        --
        The provider specific result.
        """

        pass

class ParameterMetadata:
    """
    Description
    --
    Meta description of a provider parameter.
    """

    _required = False
    _description = None

    def __init__(self, description, required):
        """
        Description
        --
        Initializes the instance.

        Parameters
        --
        - description - the description of the parameter.
        - required - true or false, whether the parameter is required.
        """

        self._description = description
        self._required = required

    @property
    def required(self):
        return self._required

    @property
    def description(self):
        return self._description