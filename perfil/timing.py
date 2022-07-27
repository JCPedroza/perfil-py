from timeit import default_timer as time
from time import perf_counter as count


class Timers:
    def __init__(self):
        self.__funs = (time, count)
        self.__totals = [0.0, 0.0]
        self.__buffer = [0.0, 0.0]

    def __str__(self) -> str:
        return f"{self.totals}"

    @property
    def totals(self) -> tuple[float, float]:
        return (self.__totals[0], self.__totals[1])

    def start(self):
        self.__buffer[0] = self.__funs[0]()
        self.__buffer[1] = self.__funs[1]()

    def stop(self):
        stop_time = self.__funs[0]()
        stop_count = self.__funs[1]()
        self.__totals[0] += stop_time - self.__buffer[0]
        self.__totals[1] += stop_count - self.__buffer[1]
