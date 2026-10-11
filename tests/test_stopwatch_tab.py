"""Тесты вкладки секундомера."""

from gui_lab.stopwatch import Stopwatch
from gui_lab.widgets.stopwatch_tab import StopwatchTab


class FakeClock:
    """Часы, время которых двигает тест."""

    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


def make_tab():
    clock = FakeClock()
    return StopwatchTab(Stopwatch(clock)), clock


def test_initial_state():
    tab, _ = make_tab()
    assert tab.time_label.text() == "00:00.00"
    assert tab.start_button.text() == "Старт"
    assert not tab.lap_button.isEnabled()


def test_start_pause_continue():
    tab, clock = make_tab()
    tab.start_button.click()
    assert tab.timer.isActive()
    assert tab.start_button.text() == "Пауза"
    clock.now = 75.25
    tab.refresh()
    assert tab.time_label.text() == "01:15.25"
    tab.start_button.click()
    assert not tab.timer.isActive()
    assert tab.start_button.text() == "Продолжить"


def test_laps_listed_newest_first():
    tab, clock = make_tab()
    tab.start_button.click()
    clock.now = 10
    tab.lap_button.click()
    clock.now = 13.5
    tab.lap_button.click()
    laps = tab.laps_list
    items = [laps.item(i).text() for i in range(laps.count())]
    assert items == ["Круг 2: 00:03.50", "Круг 1: 00:10.00"]


def test_reset():
    tab, clock = make_tab()
    tab.start_button.click()
    clock.now = 5
    tab.lap_button.click()
    tab.reset_button.click()
    assert tab.time_label.text() == "00:00.00"
    assert tab.laps_list.count() == 0
    assert tab.start_button.text() == "Старт"
    assert not tab.timer.isActive()
