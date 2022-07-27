from perfil.profiling import TimeSubject
from perfil.info import FunctionInfo, SubjectInfo


def test_subjects():
    time_subject = TimeSubject(
        FunctionInfo(fun=lambda x: x, args=(0, 5, 9, -3)),
        SubjectInfo(label="test label", shuffle=True, reps=10),
    )

    assert time_subject.label == "test label"
    assert time_subject.reps == 10
    assert time_subject.shuffle is True
