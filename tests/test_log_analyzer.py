import unittest
from unittest.mock import patch

from log_analyzer.log_analyzer import LogAnalyzer
from log_analyzer.operations.ip_frequency import LeastFrequentIP, MostFrequentIP
from log_analyzer.operations.eps import EventsPerSecond
from log_analyzer.parsers.custom_csv_parser import CustomCSVParser
from log_analyzer.readers.file_reader import FileReader
from log_analyzer.operations.bytes import TotalBytesExchanged
from log_analyzer.reporters.json_reporter import JsonReporter


class TestLogAnalyzer(unittest.TestCase):
    def setUp(self):
        self.reader = FileReader()
        self.parser = CustomCSVParser(self.reader)
        self.reporter = JsonReporter("output.json")
        self.operations = [
            MostFrequentIP(),
            LeastFrequentIP(),
            TotalBytesExchanged(),
            EventsPerSecond(),
        ]

    @patch("log_analyzer.readers.file_reader.FileReader.read")
    def test_analyze(self, mock_read):
        log_analyzer = LogAnalyzer(
            parser=self.parser,
            operations=self.operations,
        )

        log_file = [
            "1698771200 320 192.168.1.1 200 1500 GET http://example.com - - text/html",
            "1698771201 310 192.168.1.1 200 1500 GET http://example.com - -/207.58.145.61 text/html",
            "1698771202 300 192.168.1.2 200 500 GET http://example.com - DIRECT/- text/html",
        ]
        mock_read.return_value = iter(log_file)
        report_json = log_analyzer.analyze(log_file)

        self.assertIn("most_frequent_ip", report_json)
        self.assertIn("least_frequent_ip", report_json)
        self.assertEqual(report_json["most_frequent_ip"], "192.168.1.1")
        self.assertEqual(report_json["least_frequent_ip"], "192.168.1.2")
        self.assertEqual(report_json["total_bytes_exchanged"], 3500)
        self.assertEqual(report_json["events_per_second"], 1.5)
