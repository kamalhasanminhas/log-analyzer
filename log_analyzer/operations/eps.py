from typing import Any, Dict

from log_analyzer.operations.base_operation import BaseOperation


class EventsPerSecond(BaseOperation):
    """
    Calculates the number of events per second.
    """

    name = "events_per_second"

    def __init__(self):
        self.event_count = 0
        self.min_timestamp = None  # Track the earliest timestamp
        self.max_timestamp = None  # Track the latest timestamp

    def process(self, entry: Dict[str, Any]):
        timestamp = entry["timestamp"]
        if timestamp is not None:
            self.event_count += 1
            if self.min_timestamp is None or timestamp < self.min_timestamp:
                self.min_timestamp = timestamp
            if self.max_timestamp is None or timestamp > self.max_timestamp:
                self.max_timestamp = timestamp

    @property
    def result(self) -> float:
        """
        Calculates events per second based on the collected min and max timestamps
        and event count.
        """
        if (
            self.min_timestamp is None
            or self.max_timestamp is None
            or self.event_count == 0
        ):
            return 0

        # Calculate the duration
        duration = self.max_timestamp - self.min_timestamp

        if duration <= 0:
            return 0.0

        return self.event_count / duration
