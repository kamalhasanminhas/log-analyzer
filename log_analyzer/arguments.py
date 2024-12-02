import argparse


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the log analyzer tool.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="Log Analyzer",
        description="""Analyze log files for insights such as most/least frequent IPs,
          events per second, and bytes exchanged.""",
    )
    parser.add_argument("input", nargs="+", help="Path(s) to input log file(s).")
    parser.add_argument("output", help="Path to save output as JSON.")
    parser.add_argument(
        "--mfip", action="store_true", help="Find the most frequent IP."
    )
    parser.add_argument(
        "--lfip", action="store_true", help="Find the least frequent IP."
    )
    parser.add_argument(
        "--eps", action="store_true", help="Calculate events per second."
    )
    parser.add_argument(
        "--bytes", action="store_true", help="Calculate total bytes exchanged."
    )
    return parser.parse_args()
