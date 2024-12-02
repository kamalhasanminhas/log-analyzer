from typing import Any, Dict

from log_analyzer.operations.base_operation import BaseOperation


class TotalBytesExchanged(BaseOperation):
    """
    Calculates the total number of bytes exchanged
    """

    # Assumption: only provided response size,
    # no request payload size provided

    name = "total_bytes_exchanged"

    def __init__(self):
        self.total_bytes = 0

    def process(self, entry: Dict[str, Any]):
        """
        Updates the total bytes exchanged.

        :param entry: A dictionary representing a single log entry.
        """
        response_size = entry["response_size"]
        if response_size is not None:
            self.total_bytes += response_size

    @property
    def result(self) -> int:
        """
        Returns the total number of bytes exchanged.
        """
        return self.total_bytes
