# Third party imports
from ping3 import ping

# Local application imports
from core.providers.base import BaseProvider, ParameterMetadata, ProviderResult, ResultStatus


class PingProvider(BaseProvider):
    """
    Description
    --
    A Ping provider.
    - Pings a hostname/IP address

    TODO
    --
    - Hostname/IP validation
    - Threshold setting
    """

    _unit = "ms"
    _count = 5
    _p_target = "Target"

    def _run(self, parameters) -> ProviderResult:
        target = parameters[self._p_target]
        ping_val = ping(target, unit=self._unit)

        if ping_val is None or ping_val is False:
            # Bad
            return ProviderResult(ResultStatus.RED)
        else:
            # Good
            result = ProviderResult(ResultStatus.GREEN)
            result.value = int(ping_val)
            return result

    def _validate(self, parameters):
        # Validate the target
        if (not parameters[self._p_target]):
            raise ValueError("'{}' is required!".format(self._p_target))

        # TODO: IP/hostname format validation

    def _discover_parameters(self) -> dict:
        return {
            # IP / Hostname
            self._p_target: ParameterMetadata(description="IP or hostname", required=True)
        }
