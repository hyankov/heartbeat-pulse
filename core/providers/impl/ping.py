# Third party imports
from ping3 import ping

# Local application imports
from core.providers.base import BaseProvider, ParameterMetadata

class PingProvider(BaseProvider):
    """
    Description
    --
    A Ping provider.
    - Pings a hostname/IP address

    TODO
    --
    - Hostname/IP validation
    """

    _unit = "ms"
    _count = 5
    _parameter_target = "Target"

    def _run(self, parameters):
        target = parameters[self._parameter_target]
        return ping(target, unit = self._unit)

    def _validate(self, parameters):
        # Validate the target
        if (not parameters[self._parameter_target]):
            raise ValueError("'{param}' value is required!".format(param = self._parameter_target))

        #TODO: IP/hostname format validation

    def _discover_parameters(self) -> dict:
        return {
            # IP / Hostname
            self._parameter_target: ParameterMetadata("IP or hostname", True)
        }