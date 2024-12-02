from abc import ABC, abstractmethod
from typing import Iterator


class BaseReader(ABC):
    """
    Abstract base class for log file readers.
    """

    @abstractmethod
    def read(self, file_path: str) -> Iterator[str]:
        """
        Read lines from the file.

        :param file_path: Path of the file to read.
        :return: An iterator yielding lines of the file.
        """
        pass
