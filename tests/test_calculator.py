"""Тесты логики калькулятора."""

import pytest

from gui_lab.calculator import Calculator


def press_all(keys):
    calculator = Calculator()
    for key in keys:
        calculator.press(key)
    return calculator.display


@pytest.mark.parametrize(
    "keys, expected",
    [
        ("12+30=", "42"),
        ("7−10=", "-3"),
        ("6×7=", "42"),
        ("1÷3=", "0.3333333333"),
        ("0.1+0.2=", "0.3"),
        ("2+3×4=", "20"),
        ("2.5×4=", "10"),
        ("9÷3=+1=", "4"),
    ],
)
def test_expressions(keys, expected):
    assert press_all(keys) == expected


def test_new_number_after_result():
    assert press_all("2+2=5") == "5"


def test_operator_can_be_replaced():
    assert press_all("8+−×2=") == "16"


def test_intermediate_result_on_next_operator():
    calculator = Calculator()
    for key in "5+4":
        calculator.press(key)
    assert calculator.press("×") == "9"


def test_single_point_and_leading_zero():
    assert press_all("..5.2") == "0.52"
    assert press_all("007") == "7"


def test_backspace():
    assert press_all("123←") == "12"
    assert press_all("5←") == "0"
    assert press_all("7−9=←") == "-2"


def test_division_by_zero_shows_error_and_recovers():
    calculator = Calculator()
    for key in "5÷0=":
        calculator.press(key)
    assert calculator.display == "Ошибка"
    assert calculator.press("3") == "3"
    for key in "+1=":
        calculator.press(key)
    assert calculator.display == "4"


def test_clear_resets_everything():
    assert press_all("9+9C2=") == "2"


def test_digit_limit():
    assert press_all("1" * 20) == "1" * 15


@pytest.mark.parametrize("key", ["x", "٣", "", "10"])
def test_unknown_key(key):
    with pytest.raises(ValueError):
        Calculator().press(key)
