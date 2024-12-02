import os
import sys

# Fix the sys.path to ensure correct imports
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Remove incorrectly ordered paths
sys.path = [path for path in sys.path if not path.endswith("log_analyzer")]
# Add the parent directory to sys.path if it's not already there
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from log_analyzer.arguments import parse_arguments  # noqa: E402
from log_analyzer.log_analyzer import LogAnalyzer  # noqa: E402
from log_analyzer.operations.bytes import TotalBytesExchanged  # noqa: E402
from log_analyzer.operations.eps import EventsPerSecond  # noqa: E402
from log_analyzer.operations.ip_frequency import (  # noqa: E402
    LeastFrequentIP,
    MostFrequentIP,
)
from log_analyzer.parsers.custom_csv_parser import CustomCSVParser  # noqa: E402 E501
from log_analyzer.readers.file_reader import FileReader  # noqa: E402
from log_analyzer.reporters.json_reporter import JsonReporter  # noqa: E402
from log_analyzer.utils.logger import get_logger  # noqa: E402

logger = get_logger(__name__)


def main():
    args = parse_arguments()

    output_path = args.output
    results = {}

    # Validating input file
    for file_path in set(args.input):
        if not os.path.isfile(file_path):
            print(f"Error: File '{file_path}' does not exist.")
            return

        # FileReader for local file reading
        reader = FileReader()

        # CustomCSVParser for Squid Proxy logs
        parser = CustomCSVParser(reader)

        # Initializing operations list
        operations = []
        if args.mfip:
            operations.append(MostFrequentIP())
        if args.lfip:
            operations.append(LeastFrequentIP())
        if args.eps:
            operations.append(EventsPerSecond())
        if args.bytes:
            operations.append(TotalBytesExchanged())

        # Creating the LogAnalyzer
        log_analyzer = LogAnalyzer(parser, operations)

        # Assuming and performing the analysis on each file separately.
        results[file_path] = log_analyzer.analyze(file_path)

    # JSON Reporter
    reporter = JsonReporter(output_path)
    reporter.generate(results)
    logger.debug(f"Analysis complete. Results saved to {output_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error occurred %s", e)
