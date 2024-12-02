from typing import Any, Dict, List

from log_analyzer.operations.base_operation import BaseOperation
from log_analyzer.parsers.base_parser import BaseParser
from log_analyzer.utils.logger import get_logger

logger = get_logger(__name__)


class LogAnalyzer:
    def __init__(
        self,
        parser: BaseParser,
        operations: List[BaseOperation],
    ):
        """
        Initializes the LogAnalyzer with a parser and operations.

        :param parser: The parser to extract data from the log file.
        :param operations: A list of operations to perform on the log data.
        """
        self.parser = parser
        self.operations = operations

    def analyze(self, file_path: str) -> Dict[str, Any]:
        """
        Perform the analysis on a single log file.

        :param file_path: Path of the file to analyze.
        """
        # Parse log entries from the file
        # As next step we could use multiprocessing to analyze log files in chunks,
        # at the end we can collect the Operation results from each process,
        # combine them and run some calculations if needed.
        # That would reduce the time drastically depending on the number of processes.
        for entry in self.parser.parse(file_path):
            for operation in self.operations:
                operation.process(entry)

        # Collect results from all operations
        return {operation.name: operation.result for operation in self.operations}
