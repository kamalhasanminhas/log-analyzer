from typing import Any, Dict

from log_analyzer.operations.base_operation import BaseOperation
from log_analyzer.utils.collection import SingletonCounter


class BaseIPFrequencyOperation(BaseOperation):
    """
    Base class for IP frequency-related operations.
    This class maintains a shared Counter object for tracking IP occurrences.
    """

    def __init__(self):
        self.ip_counter = SingletonCounter()


class MostFrequentIP(BaseIPFrequencyOperation):
    name = "most_frequent_ip"

    def process(self, entry: Dict[str, Any]):
        ip_match = entry["client_ip"]
        if ip_match:
            self.ip_counter[ip_match] += 1

    @property
    def result(self):
        return str(self.ip_counter.most_common(1)[0][0]) if self.ip_counter else None


class LeastFrequentIP(BaseIPFrequencyOperation):
    name = "least_frequent_ip"

    def process(self, entry: Dict[str, Any]):
        ip_match = entry["client_ip"]
        if ip_match:
            self.ip_counter[ip_match] += 1

    @property
    def result(self):
        ip, _ = min(self.ip_counter.items(), key=lambda x: x[1])
        return str(ip)
