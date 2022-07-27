from random import shuffle as shuffle_array
from perfil.timing import Timers
from perfil.info import FunctionInfo, SubjectInfo


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
