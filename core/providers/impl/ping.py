# Import system
from typing import Dict

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
    """

    _unit = "ms"
    _count = 5
    _p_target = "Target"
    _p_threshold_ms = "ThresholdMs"

    def _run(self, parameters: Dict[str, str]) -> ProviderResult:
        target = parameters[self._p_target]
        ping_val = ping(target, unit=self._unit)

        if ping_val is None or ping_val is False:
            # Bad
            return ProviderResult(ResultStatus.RED)
        else:
            limit = int(parameters[self._p_threshold_ms])
            result = ProviderResult(ResultStatus.GREEN)
            result.value = int(ping_val)

            if (result.value > limit):
                result.status = ResultStatus.RED
            elif (result.value > limit - (limit / 10)):
                result.status = ResultStatus.YELLOW

            return result

    def _validate(self, parameters: Dict[str, str]) -> None:
        def is_int(input: str) -> bool:
            try:
                int(input)
            except ValueError:
                return False
            return True

        param = self._p_threshold_ms
        if not is_int(parameters[param]):
            raise ValueError("Invalid integer for {}".format(param))

        if int(parameters[self._p_threshold_ms]) < 0:
            raise ValueError("{} cannot be less than 0".format(param))

        # TODO: IP/hostname format validation
        pass

    def _discover_parameters(self) -> Dict[str, ParameterMetadata]:
        return {
            # IP / Hostname
            self._p_target: ParameterMetadata(description="IP or hostname", required=True),

            # Threshold
            self._p_threshold_ms: ParameterMetadata(description="Threshold (ms)", required=True)
        }
