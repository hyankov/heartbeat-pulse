# Standard library imports
import abc
from datetime import datetime
import logging
from logging import Logger

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


class BaseResultHandler(abc.ABC):
    """
    Description
    --
    The base abstract results handler class.
    """

    @abc.abstractmethod
    def handle_result(self, result: ProfileResult) -> None:
        """
        Description
        --
        Handles the result.
        Must be overriden.

        Parameters
        --
        - result - the run result.
        """

        pass


class LoggerResultHandler(BaseResultHandler):
    """
    Description
    --
    A result handler that prints the results to a log.
    """

    def __init__(self):
        self._logger = self._get_logger()

    def _get_logger(self) -> Logger:
        logger = logging.getLogger(__name__)

        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False

        return logger

    def handle_result(self, result: ProfileResult) -> None:
        if result is None:
            return

        msg = "[{}] [{}] Started: {}, Finished: {}, Took: {}ms => {}".format(
                result.result.status.name,
                result.profile_name,
                result.started_at.strftime('%c'),
                result.finished_at.strftime('%c'),
                result.runtime_ms,
                result.result.value)

        if result.result.status == ResultStatus.RED:
            self._logger.error(msg)
        elif result.result.status == ResultStatus.YELLOW:
            self._logger.warn(msg)
        else:
            self._logger.info(msg)


class RabbitMQResultHandler(BaseResultHandler):
    """
    Description
    --
    A result handler that pushes the results into RabbitMQ.
    """

    def handle_result(self, result: ProfileResult) -> None:
        if result is None:
            return

        # TODO: Implement
        raise NotImplementedError()
