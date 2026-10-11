"""Тесты логики секундомера."""

import pytest

from gui_lab.stopwatch import Stopwatch, format_time


class FakeClock:
    """Часы, время которых двигает тест."""

    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now


@pytest.fixture
def clock():
    return FakeClock()


def test_counts_only_while_running(clock):
    watch = Stopwatch(clock)
    clock.now += 5
    assert watch.elapsed == 0
    watch.start()
    clock.now += 2.5
    assert watch.elapsed == pytest.approx(2.5)
    watch.stop()
    clock.now += 100
    assert watch.elapsed == pytest.approx(2.5)
    watch.start()
    clock.now += 1
    assert watch.elapsed == pytest.approx(3.5)


def test_repeated_start_and_stop_are_harmless(clock):
    watch = Stopwatch(clock)
    watch.start()
    clock.now += 1
    watch.start()
    clock.now += 1
    watch.stop()
    watch.stop()
    assert watch.elapsed == pytest.approx(2)


def test_laps(clock):
    watch = Stopwatch(clock)
    watch.start()
    clock.now += 10
    assert watch.lap() == pytest.approx(10)
    clock.now += 4
    assert watch.lap() == pytest.approx(4)
    assert watch.laps == pytest.approx((10, 4))


def test_lap_requires_running(clock):
    with pytest.raises(RuntimeError):
        Stopwatch(clock).lap()


def test_reset(clock):
    watch = Stopwatch(clock)
    watch.start()
    clock.now += 3
    watch.lap()
    watch.reset()
    assert (watch.running, watch.elapsed, watch.laps) == (False, 0, ())


@pytest.mark.parametrize(
    "seconds, text",
    [(0, "00:00.00"), (5.678, "00:05.68"), (61.5, "01:01.50"),
     (3599.999, "1:00:00.00"), (3725.04, "1:02:05.04")],
)
def test_format_time(seconds, text):
    assert format_time(seconds) == text


def test_format_negative():
    with pytest.raises(ValueError):
        format_time(-1)
