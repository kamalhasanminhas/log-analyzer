from collections import Counter


class SingletonCounter(Counter):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonCounter, cls).__new__(cls)
        return cls._instance
