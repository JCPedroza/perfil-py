from profiling import build_profile_group


def my_first_test_function(my_test_arg):
    return my_test_arg


def my_second_test_function(my_test_arg):
    return my_test_arg


def my_third_test_function(my_test_arg):
    return my_test_arg


def test_profiling():
    funs = [my_first_test_function, my_second_test_function, my_third_test_function]
    args = (-5, -2, 0, 2, 5)
    reps = 30
    shuffle = True
    profiles = build_profile_group(funs, args, reps, shuffle)

    profiles.mute()

    # Profile group must be indexable.
    assert profiles[0].name == "my_first_test_function"
    assert profiles[1].name == "my_second_test_function"
    assert profiles[2].name == "my_third_test_function"
    assert len(profiles) == 3

    results = profiles.profile()

    # Check that results are in ascending order.
    for index in range(len(results) - 1):
        assert results[index].total <= results[index + 1].total

    # Profile group must be iterable
    for profile in profiles:
        assert profile.total > 0
        assert profile.args == args
        assert profile.reps == reps
        assert profile.shuffle == shuffle
