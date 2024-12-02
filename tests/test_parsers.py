import unittest
from unittest.mock import patch

from log_analyzer.parsers.custom_csv_parser import CustomCSVParser
from log_analyzer.readers.file_reader import FileReader


class TestCustomCSVLogParser(unittest.TestCase):
    def setUp(self):
        self.reader = FileReader()
        self.parser = CustomCSVParser(self.reader)

    @patch("log_analyzer.readers.file_reader.FileReader.read")
    def test_valid_csv_row(self, mock_read):
        row = "1157689320.327   2864 10.105.21.199 TCP_MISS/200 10182 GET http://www.goonernews.com/ badeyek DIRECT/207.58.145.61 text/html\n"
        mock_read.return_value = iter([row])
        expected_output = {
            "timestamp": 1157689320.327,
            "response_header_size": 2864,
            "client_ip": "10.105.21.199",
            "http_response_code": 200,
            "response_size": 10182,
            "http_method": "GET",
            "url": "http://www.goonernews.com/",
            "username": "badeyek",
            "access_type": "DIRECT",
            "destination_ip": "207.58.145.61",
            "response_type": "text/html",
        }
        gen = self.parser.parse(row)
        parsed_dict = next(gen)
        self.assertDictEqual(parsed_dict, expected_output)

    @patch("log_analyzer.readers.file_reader.FileReader.read")
    def test_invalid_csv_row(self, mock_read):
        row = "invalid_row_data\n"
        mock_read.return_value = iter([row])
        gen = self.parser.parse(row)
        self.assertFalse(any(gen))

    @patch("log_analyzer.readers.file_reader.FileReader.read")
    def test_partial_valid_csv_row(self, mock_read):
        row = "1157689320.327   2864 10.105.21.199 TCP_MISS/- 10182 GET http://www.goonernews.com/ badeyek -/207.58.145.61 text/html\n"
        mock_read.return_value = iter([row])
        expected_output = {
            "timestamp": 1157689320.327,
            "response_header_size": 2864,
            "client_ip": "10.105.21.199",
            "http_response_code": None,
            "response_size": 10182,
            "http_method": "GET",
            "url": "http://www.goonernews.com/",
            "username": "badeyek",
            "access_type": None,
            "destination_ip": "207.58.145.61",
            "response_type": "text/html",
        }
        gen = self.parser.parse(row)
        parsed_dict = next(gen)
        self.assertDictEqual(parsed_dict, expected_output)
