import re
from typing import Any, Dict, Iterator

from log_analyzer.parsers.base_parser import BaseParser
from log_analyzer.parsers.schema import LogEntry
from log_analyzer.readers.base_reader import BaseReader
from log_analyzer.utils.logger import get_logger

logger = get_logger(__name__)


class CustomCSVParser(BaseParser):
    """
    Custom parser for Squid Proxy logs.
    """

    def __init__(self, reader: BaseReader):
        super().__init__(reader)

    def parse(self, file_path: str) -> Iterator[Dict[str, Any]]:
        """
        Parse a single Squid Proxy log file yield rows as dictionaries.

        :param file_path: Path of the Squid Proxy log file to parse.
        :return: An iterator of parsed log entries as dictionaries.
        """
        for line_number, line in enumerate(self.reader.read(file_path)):
            try:
                # Split fields by whitespace
                fields = re.split(r"\s+", line.strip())
                if len(fields) != 10:
                    logger.warning(
                        f"""Malformed line at {line_number}: Expected 10 fields,
                          found {len(fields)}"""
                    )
                    continue
                # Validate and parse using the schema
                yield LogEntry.from_raw(fields, line_number)

            except Exception as e:
                logger.error(f"Error processing line {line_number}: {e}")
                continue
