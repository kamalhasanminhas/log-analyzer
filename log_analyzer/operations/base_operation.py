from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseOperation(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def process(self, entry: Dict[str, Any]):
        """Process log entry"""
        pass

    @property
    @abstractmethod
    def result(self) -> Any:
        """Return the result of the operation."""
        pass
