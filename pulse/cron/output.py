# Standard library imports
from datetime import datetime
import logging
from logging.config import fileConfig
from os import path

# Local imports
from ..providers import ProviderResult, ResultStatus


class ProfileResult:
    """
    Description
    --
    Associates a profile with its result.
    """

    def __init__(self, profile_id: str, profile_name: str, started_at: datetime) -> None:
        """
        Parameters
        --
        - profile_id - the Id of the profile that was executed.
        - profile_name - the name of the profile that was executed.
        - started_at - when was it started.
        """

        if not profile_id:
            raise ValueError("profile_id is required!")

        if not profile_name:
            raise ValueError("profile_name is required!")

        if started_at is None:
            raise ValueError("started_at is required!")

        self.profile_id = profile_id
        self.profile_name = profile_name
        self.result = None              # type: ProviderResult
        self.started_at = started_at
        self.finished_at = None         # type: datetime

    @property
    def runtime_ms(self) -> int:
        if self.finished_at is None:
            return None
        else:
            return int((self.finished_at - self.started_at).total_seconds() * 1000)


class LogResultHandler():
    """
    Description
    --
    A result handler that prints the results to a log.
    """

    def __init__(self) -> None:
        log_file_path = path.join(path.dirname(path.abspath(__file__)), '../../config/output.config.ini')
        fileConfig(log_file_path)
        self._logger = logging.getLogger('pulseoutput')

    def handle_result(self, result: ProfileResult) -> None:
        if result is None:
            return

        msg = {
                'status': result.result.status.name,
                'profile_name': result.profile_name,
                'profile_id': result.profile_id,
                'start_date': result.started_at,
                'end_date': result.finished_at,
                'runtime_ms': result.runtime_ms,
                'result_value': result.result.value
        }

        if result.result.status == ResultStatus.TIMEOUT:
            self._logger.error('', extra=msg)
        elif result.result.status in [ResultStatus.RED, ResultStatus.YELLOW]:
            self._logger.warn('', extra=msg)
        else:
            self._logger.info('', extra=msg)
