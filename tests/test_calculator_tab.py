"""Тесты вкладки калькулятора: кнопки и клавиатура."""

from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest

from gui_lab.widgets.calculator_tab import BUTTONS, CalculatorTab


def test_every_button_exists():
    tab = CalculatorTab()
    assert set(tab.buttons) == set(BUTTONS)


def test_buttons_compute():
    tab = CalculatorTab()
    for key in "12.5×4=":
        QTest.mouseClick(tab.buttons[key], Qt.MouseButton.LeftButton)
    assert tab.display.text() == "50"


def test_keyboard_input():
    tab = CalculatorTab()
    QTest.keyClicks(tab, "7")
    QTest.keyClick(tab, Qt.Key.Key_Asterisk)
    QTest.keyClicks(tab, "6")
    QTest.keyClick(tab, Qt.Key.Key_Return)
    assert tab.display.text() == "42"
    QTest.keyClick(tab, Qt.Key.Key_Escape)
    assert tab.display.text() == "0"


def test_display_is_read_only():
    assert CalculatorTab().display.isReadOnly()
