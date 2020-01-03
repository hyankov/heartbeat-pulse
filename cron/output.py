# Standard library imports
import abc
from typing import List

# Local imports
from core.running import ProfileRunResult


class BaseResultsHandler(abc.ABC):
    """
    Description
    --
    The base abstract results handler class.
    """

    @abc.abstractmethod
    def handle_results(self, results: List[ProfileRunResult]) -> None:
        """
        Description
        --
        Handles the results.
        Must be overriden.

        Parameters
        --
        - results - the run results.
        """

        pass


class ConsoleResultsHandler(BaseResultsHandler):
    """
    Description
    --
    A result handler that prints the results to the console.
    """

    def _handle_result(self, result: ProfileRunResult) -> None:
        print(result)

    def handle_results(self, results: List[ProfileRunResult]) -> None:
        for result in results:
            self._handle_result(result)


class RabbitMQResultsHandler(BaseResultsHandler):
    """
    Description
    --
    A result handler that pushes the results into RabbitMQ.
    """

    def _handle_result(self, result: ProfileRunResult) -> None:
        # TODO: Implement
        raise NotImplementedError()

    def handle_results(self, results: List[ProfileRunResult]) -> None:
        for result in results:
            self._handle_result(result)
