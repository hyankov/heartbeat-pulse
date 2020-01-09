# Import system
from typing import Dict

# Third party imports
from ping3 import ping

# Local application imports
from .. import BaseProvider, ParameterMetadata, ProviderResult, ResultStatus


class PingProvider(BaseProvider):
    """
    Description
    --
    A Ping provider. Pings a hostname/IP address.
    """

    _unit = "ms"
    _count = 5
    _p_target = "Target"
    _p_threshold_ms = "ThresholdMs"

    def _run(self, parameters: Dict[str, str]) -> ProviderResult:
        target = parameters[self._p_target]
        ping_val = ping(target, unit=self._unit)

        if ping_val is None or not ping_val:
            # Resolution issue - bad
            return ProviderResult(ResultStatus.RED)
        else:
            limit = int(parameters[self._p_threshold_ms])
            result = ProviderResult(ResultStatus.GREEN, int(ping_val))

            if (result.value > limit):
                # Over the limit
                result.status = ResultStatus.RED
            elif (result.value > limit - (limit / 10)):
                # Close to the limit (over 90%)
                result.status = ResultStatus.YELLOW

            return result

    def _validate(self, parameters: Dict[str, str]) -> None:
        def is_int(input: str) -> bool:
            try:
                int(input)
            except ValueError:
                return False
            return True

        # Threshold validation
        param = self._p_threshold_ms
        if not is_int(parameters[param]):
            raise ValueError("Param '{}' is not an integer".format(param))

        if int(parameters[self._p_threshold_ms]) < 0:
            raise ValueError("Param '{}' cannot be less than 0".format(param))

        # IP/hostname format validation
        param = self._p_target
        if " " in parameters[param]:
            raise ValueError("Param '{}' contains spaces".format(param))

    def _discover_parameters(self) -> Dict[str, ParameterMetadata]:
        return {
            # IP / Hostname
            self._p_target: ParameterMetadata(description="IP or hostname", required=True),

            # Threshold
            self._p_threshold_ms: ParameterMetadata(description="Threshold (ms)", required=True)
        }
