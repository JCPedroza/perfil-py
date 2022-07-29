from time import sleep
from timing import Timer


def test_timing():
    timer = Timer()

    assert timer.total == 0.0

    timer.start()
    sleep(0.005)
    timer.stop()

    assert timer.total > 0.0

    timer.reset()

    assert timer.total == 0.0
