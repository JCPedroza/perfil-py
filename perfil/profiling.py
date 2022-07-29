from random import shuffle as shuffle_list
from typing import Callable
from timing import Timer


class Profile:
    def __init__(self, fun: Callable, args: tuple, reps: int, shuffle: bool):
        self.__fun = fun
        self.__args = args
        self.__shuffle = shuffle
        self.__reps = reps
        self.__timer = Timer()
        self.__shufflable_args = list(args)
        self.__verbose = True

    def __str__(self):
        head = f"\n{self.name=}\n{self.reps=}\n{self.verbose=}"
        mid = f"\n{self.shuffle=}\n{self.args=}\n{self.shufflable_args=}"
        bot = f"\nself.timers={str(self.__timer)}"

        return f"{head}{mid}{bot}"

    def __shuffle_args(self):
        shuffle_list(self.__shufflable_args)

    def __time_fun_call(self, *args):
        if self.__verbose is True:
            print(f"Profiling {self.__fun.__name__}({args})...")

        self.__timer.start()
        self.__fun(*args)
        self.__timer.stop()

    def __time_fun_arglist(self):
        if self.shuffle:
            self.__shuffle_args()

        for args in self.__shufflable_args:
            self.__time_fun_call(args)

    def mute(self):
        self.__verbose = False

    def unmute(self):
        self.__verbose = True

    def profile(self) -> float:
        self.__timer.reset()
        for _ in range(self.reps):
            self.__time_fun_arglist()

        return self.__timer.total

    @property
    def name(self) -> str:
        return self.__fun.__name__

    @property
    def args(self) -> tuple:
        return self.__args

    @property
    def shufflable_args(self) -> tuple:
        return tuple(self.__shufflable_args)

    @property
    def reps(self) -> int:
        return self.__reps

    @property
    def shuffle(self) -> bool:
        return self.__shuffle

    @property
    def verbose(self) -> bool:
        return self.__verbose


class ProfileCollection:
    def __init__(self, profiles: tuple[Profile, ...], shuffle: bool):
        self.__profiles = profiles
        self.__shuffle = shuffle

    def __shuffle_profiles(self):
        shuffle_list(self.__profiles)

    def profile(self) -> tuple[float, ...]:
        if self.__shuffle:
            self.__shuffle_profiles()

        return tuple(profile.profile() for profile in self.__profiles)

    @property
    def profiles(self):
        return self.__profiles

    @property
    def shuffle(self):
        return self.__shuffle
