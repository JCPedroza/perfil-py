from typing import Callable


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
