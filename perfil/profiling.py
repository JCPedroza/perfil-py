from random import shuffle as shuffle_list
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Callable, overload

from timing import Timer


@dataclass(frozen=True)
class ProfileSpec:
    """Immutable container of profile specifications."""

    fun: Callable
    args: tuple
    reps: int
    shuffle: bool


@dataclass(frozen=True)
class ProfileResult:
    """Immutable container of profile results."""

    spec: ProfileSpec
    total: float


class Profile:
    """Handles function profiling."""

    def __init__(self, spec: ProfileSpec):
        self.__spec = spec
        self.__timer = Timer()
        self.__shufflable_args = list(spec.args)
        self.__verbose = True

    def __str__(self):
        head = f"\n{self.name=}\n{self.reps=}\n{self.verbose=}"
        mid = f"\n{self.shuffle=}\n{self.args=}\n{self.shufflable_args=}"
        bot = f"\nself.timer={str(self.__timer)}"

        return f"{head}{mid}{bot}"

    def __lt__(self, other):
        return self.total < other.total

    def __le__(self, other):
        return self.total <= other.total

    def __eq__(self, other):
        return self.total == other.total

    def __ne__(self, other):
        return self.total != other.total

    def __gt__(self, other):
        return self.total > other.total

    def __ge__(self, other):
        return self.total >= other.total

    def __shuffle_args(self):
        shuffle_list(self.shufflable_args)

    def __time_fun_call(self, *args):
        if self.__verbose:
            print(f"Profiling {self.name}{args}...")

        fun = self.__spec.fun
        timer = self.__timer

        timer.start()
        fun(*args)
        timer.stop()

    def __time_fun_arglist(self):
        if self.shuffle:
            self.__shuffle_args()

        for args in self.__shufflable_args:
            self.__time_fun_call(args)

    def mute(self):
        self.__verbose = False

    def unmute(self):
        self.__verbose = True

    def profile(self) -> ProfileResult:
        self.__timer.reset()
        for _ in range(self.reps):
            self.__time_fun_arglist()

        return ProfileResult(self.__spec, self.__timer.total)

    @property
    def total(self) -> float:
        return self.__timer.total

    @property
    def name(self) -> str:
        return self.__spec.fun.__name__

    @property
    def args(self) -> tuple:
        return self.__spec.args

    @property
    def shufflable_args(self) -> list:
        return self.__shufflable_args[:]

    @property
    def reps(self) -> int:
        return self.__spec.reps

    @property
    def shuffle(self) -> bool:
        return self.__spec.shuffle

    @property
    def verbose(self) -> bool:
        return self.__verbose


class ProfileGroup(Sequence[Profile]):
    """Groups and handles multiple profiles."""

    def __init__(self, profiles: tuple[Profile, ...], shuffle: bool):
        self.__profiles = profiles
        self.__shufflable_profiles = list(profiles)
        self.__shuffle = shuffle
        super().__init__()

    @overload
    def __getitem__(self, index: int) -> Profile:
        ...

    @overload
    def __getitem__(self, indexes: slice) -> Sequence[Profile]:
        ...

    def __getitem__(self, index: int | slice) -> Profile | Sequence[Profile]:
        if isinstance(index, int):
            if index >= len(self):
                raise IndexError("Index out of range")
        return self.__profiles[index]

    def __len__(self) -> int:
        return len(self.__profiles)

    def __shuffle_profiles(self):
        shuffle_list(self.__shufflable_profiles)

    def profile(self) -> tuple[ProfileResult, ...]:
        if self.__shuffle:
            self.__shuffle_profiles()

        results = (profile.profile() for profile in self.__shufflable_profiles)
        return tuple(sorted(results, key=lambda a: a.total))

    def mute(self):
        for profile in self.__profiles:
            profile.mute()

    def unmute(self):
        for profile in self.__profiles:
            profile.unmute()

    @property
    def profiles(self):
        return self.__profiles

    @property
    def shuffle(self):
        return self.__shuffle


def build_profile_group(
    funs: Sequence[Callable],
    args: tuple,
    reps: int,
    shuffle: bool,
) -> ProfileGroup:
    """Create a profile group."""
    profiles = tuple(Profile(ProfileSpec(fun, args, reps, shuffle)) for fun in funs)
    return ProfileGroup(profiles, shuffle)
