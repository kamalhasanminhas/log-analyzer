from log_analyzer.readers.base_reader import BaseReader


class FileReader(BaseReader):
    def read(self, file_path: str):
        """
        Reads lines from a local file.

        :param file_path: Path of the file to read.
        :return: An iterator yielding lines of the file.
        """
        with open(file_path, mode="r", encoding="utf-8") as file:
            for line in file:
                yield line
