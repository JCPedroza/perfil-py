from typing import Callable
from random import shuffle as shuffle_array
from timeit import default_timer as timer
from time import perf_counter as counter


class Timers:
    def __init__(self):
        self.__funs = (timer, counter)
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


class FunctionInfo:
    def __init__(self, *, fun: Callable, args: tuple):
        self.fun = fun
        self.args = args


class SubjectInfo:
    def __init__(self, *, shuffle: bool, reps: int, label: str):
        if reps < 1:
            raise ValueError(f"reps < 1: {reps}")

        self.reps = reps
        self.shuffle = shuffle
        self.label = label


class TimeSubject:
    def __init__(self, funinfo: FunctionInfo, subinfo: SubjectInfo):
        self.__funinfo = funinfo
        self.__subinfo = subinfo
        self.__timers = Timers()
        self.__shuffable_args = list(funinfo.args)

    def __str__(self):
        head = f"\nTimeSubject\n{self.label=}\n{self.name=}\n{self.reps=}"
        mid = f"\n{self.shuffle=}\nself.timers={str(self.__timers)}"
        bot = f"\n{self.args=}\n{self.shuffled_args=}"
        return f"{head}{mid}{bot}"

    def __shuffle_args(self):
        shuffle_array(self.__shuffable_args)

    def __time_fun_call(self, arg):
        self.__timers.start()
        self.__funinfo.fun(arg)
        self.__timers.stop()

    def __time_fun_arglist(self):
        if self.shuffle:
            self.__shuffle_args()

        for arg in self.__shuffable_args:
            self.__time_fun_call(arg)

    def profile(self):
        for _ in range(self.reps):
            self.__time_fun_arglist()

    def print(self):
        print(self)

    @property
    def name(self) -> str:
        return self.__funinfo.fun.__name__

    @property
    def args(self) -> tuple:
        return self.__funinfo.args

    @property
    def shuffled_args(self) -> tuple:
        return tuple(self.__shuffable_args)

    @property
    def reps(self) -> int:
        return self.__subinfo.reps

    @property
    def label(self) -> str:
        return self.__subinfo.label

    @property
    def shuffle(self) -> bool:
        return self.__subinfo.shuffle
