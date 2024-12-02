from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseReporter(ABC):
    def __init__(self, output_path: str):
        """
        Initializes the BaseReporter with the report path

        :param output_path: Report output path
        """
        self.output_path = output_path

    @abstractmethod
    def generate(self, operations_results: Dict[str, Any]):
        """
        Generates report

        :param operations_results: A dictionary where the key is the operation name and
        value is its result.
        """
        pass
