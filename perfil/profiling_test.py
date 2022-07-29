from profiling import Profile


def my_test_function(my_test_arg):
    return my_test_arg


def test_profiling():
    time_subject = Profile(my_test_function, (0, 5, 9, -3), 10, True)

    assert time_subject.name == "my_test_function"
    assert time_subject.reps == 10
    assert time_subject.shuffle is True
    assert time_subject.profile() > 0
