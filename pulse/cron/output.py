# Standard library imports
import abc
from datetime import datetime
import logging

# Local imports
from core.providers.base import ProviderResult, ResultStatus


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


class ConsoleResultHandler(BaseResultHandler):
    """
    Description
    --
    A result handler that prints the results to the console.
    """

    def __init__(self):
        self.log = logging.getLogger()
        self.log.addHandler(logging.StreamHandler())

    def handle_result(self, result: ProfileResult) -> None:
        if result is None:
            return

        msg = "[{}] [{}] Started: {}, Finished: {}, Took: {}ms => {}".format(
                result.result.status.name,
                result.profile_name,
                result.started_at,
                result.finished_at,
                result.runtime_ms,
                result.result.value)

        if result.result.status == ResultStatus.GREEN:
            self.log.info(msg)
        elif result.result.status == ResultStatus.YELLOW:
            self.log.warn(msg)
        else:
            self.log.error(msg)


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
