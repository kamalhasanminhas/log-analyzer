import unittest
from unittest.mock import mock_open, patch

from log_analyzer.reporters.json_reporter import JsonReporter


class TestJsonReporter(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_generate_report(self, mock_json_dump, mock_file):
        file_path = "output.json"
        reporter = JsonReporter(file_path)
        results = {
            "most_frequent_ip": "192.168.1.1",
            "events_per_second": 1.0,
            "least_frequent_ip": "10.10.20.10",
        }
        reporter.generate(results)
        mock_file.assert_called_once_with(file_path, mode="w")
        mock_json_dump.assert_called_once_with(results, mock_file(), indent=4)
