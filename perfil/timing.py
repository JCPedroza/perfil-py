from timeit import default_timer as time


class Timer:
    def __init__(self):
        self.__time = time
        self.__buffer = 0.0
        self.__total = 0.0

    def __str__(self) -> str:
        return f"Timer total: {self.__total}"

    @property
    def total(self) -> float:
        return self.__total

    def start(self):
        self.__buffer = self.__time()

    def stop(self):
        stop_time = self.__time()
        self.__total += stop_time - self.__buffer

    def reset(self):
        self.__buffer = 0.0
        self.__total = 0.0
