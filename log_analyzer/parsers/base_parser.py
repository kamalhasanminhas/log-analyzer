from abc import ABC, abstractmethod
from typing import Any, Dict, Iterator

from log_analyzer.readers.base_reader import BaseReader


class BaseParser(ABC):
    """
    Abstract base class for all log parsers.
    """

    def __init__(self, reader: BaseReader) -> None:
        """
        Initialize the parser with a reader.

        :param reader: A `BaseReader` instance to handle raw file reading.
        """
        self.reader = reader

    @abstractmethod
    def parse(self, file_path: str) -> Iterator[Dict[str, Any]]:
        """
        Parse the log file and yield rows as dictionaries.

        :param file_path: Path of the file to parse.
        :return: An iterator of parsed log entries as dictionaries.
        """
        pass
