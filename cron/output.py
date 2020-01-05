# Standard library imports
import abc

# Local imports
from core.providers.base import ProviderRun


class ProfileRun:
    """
    Description
    --
    The representation of a run of a profile.
    """

    def __init__(self, profile_id: str, profile_name: str, provider_run: ProviderRun) -> None:
        """
        - profile_id - the Id of the profile that ran.
        - provider_run - the provider run.
        """

        self.profile_id = profile_id
        self.profile_name = profile_name
        self.provider_run = provider_run


class BaseResultHandler(abc.ABC):
    """
    Description
    --
    The base abstract results handler class.
    """

    @abc.abstractmethod
    def handle_result(self, results: ProfileRun) -> None:
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

    def handle_result(self, result: ProfileRun) -> None:
        print(
            "[{}] Started: {}, Took: {}ms => {}".format(
                result.profile_name,
                result.provider_run.started_at,
                result.provider_run.runtime_ms,
                result.provider_run.result))


class RabbitMQResultHandler(BaseResultHandler):
    """
    Description
    --
    A result handler that pushes the results into RabbitMQ.
    """

    def handle_result(self, result: ProfileRun) -> None:
        # TODO: Implement
        raise NotImplementedError()
