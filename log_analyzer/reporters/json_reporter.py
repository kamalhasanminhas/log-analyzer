import json
from typing import Any, Dict

from log_analyzer.reporters.base_reporter import BaseReporter


class JsonReporter(BaseReporter):
    def __init__(self, output_path) -> None:
        super().__init__(output_path)

    def generate(self, operations_results: Dict[str, Any]):
        """
        Generates report
        """
        with open(self.output_path, mode="w") as file:
            json.dump(operations_results, file, indent=4)
