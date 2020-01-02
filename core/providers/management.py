# Standard library imports
import importlib, inspect, os, pkgutil, sys

# Local application imports
from core.providers.base import BaseProvider

# Load all provider implementation modules
from core.providers.impl import *

class ProvidersManager:
    """
    Description
    --    
    - Lists available providers.
    - Creates an instance of a provider.
    """

    # Initialized once, at loading and then cached
    _providers = {}

    def __init__(self):
        """
        Description
        --
        Initializes the instance.
        - Loads and caches the list of providers.
        """
        # Find all classes that inherit from the base (works because the implementation modules are imported)
        providers = BaseProvider.__subclasses__()
        for provider in providers:
            # Dictionary of provider_id:provider_module
            self._providers[provider.__name__] = provider.__module__

    def get_all_ids(self):
        """
        Description
        --
        Gets all available provider Ids.

        Returns
        --
        A list of the Ids of all available providers.
        """

        return list(self._providers.keys())

    def discover_provider_parameters(self, provider_id):
        """
        Description
        --
        Discovers the parameters a provider would expect at runtime.

        Parameters
        --
        - provider_id - the Id of the provider of which we want to discover the runtime parameters.

        Returns
        --
        A dictionary of the parameters a provider would expect at runtime.
        """

        # Create an instance of the provider
        provider_instance = self.instantiate(provider_id)

        # Ask the instance of the provider to reveal its runtime parameters.
        return provider_instance.discover_parameters()

    def instantiate(self, provider_id):
        """
        Description
        --
        Creates an insance of a provider.

        Parameters
        --
        - provider_id - the Id of the provider which we want to create an instance of.

        Returns
        --
        An instance of the provider.
        """

        if not provider_id or provider_id == "":
            raise ValueError("provider_id is required!")

        # Use 'reflection' to create an instance
        provider_class_ = getattr(sys.modules[self._providers[provider_id]], provider_id)
        instance = provider_class_()

        # Return the instance
        return instance