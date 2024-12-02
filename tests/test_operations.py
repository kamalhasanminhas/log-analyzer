import unittest

from log_analyzer.operations.bytes import TotalBytesExchanged
from log_analyzer.operations.eps import EventsPerSecond
from log_analyzer.operations.ip_frequency import LeastFrequentIP, MostFrequentIP


class TestOperations(unittest.TestCase):
    def test_most_frequent_ip(self):
        operation = MostFrequentIP()
        entries = [
            {"client_ip": "192.168.1.1"},
            {"client_ip": "192.168.1.1"},
            {"client_ip": "192.168.1.2"},
        ]
        for entry in entries:
            operation.process(entry)
        self.assertEqual(operation.result, "192.168.1.1")

    def test_least_frequent_ip(self):
        operation = LeastFrequentIP()
        entries = [
            {"client_ip": "192.168.1.1"},
            {"client_ip": "192.168.1.1"},
            {"client_ip": "192.168.1.2"},
        ]
        for entry in entries:
            operation.process(entry)
        self.assertEqual(operation.result, "192.168.1.2")

    def test_events_per_second(self):
        operation = EventsPerSecond()
        entries = [
            {"timestamp": 1698771200},
            {"timestamp": 1698771203},
            {"timestamp": 1698771201},
        ]
        for entry in entries:
            operation.process(entry)
        self.assertEqual(operation.result, 1.0)  # 3 events over 3 seconds

    def test_total_bytes_exchanged(self):
        operation = TotalBytesExchanged()
        entries = [
            {"response_size": 1500},
            {"response_size": 2000},
            {"response_size": 500},
        ]
        for entry in entries:
            operation.process(entry)
        self.assertEqual(operation.result, 4000)
