"""Тесты палитры и выбора цвета текста."""

import pytest

from gui_lab.colors import PALETTE, Color, ColorCycle, text_color_for


def test_cycle_goes_round():
    cycle = ColorCycle()
    assert cycle.current == PALETTE[0]
    seen = [cycle.next() for _ in PALETTE]
    assert seen == [*PALETTE[1:], PALETTE[0]]


def test_custom_palette():
    cycle = ColorCycle([Color("a", "#000000"), Color("b", "#FFFFFF")])
    assert cycle.next().name == "b"
    assert cycle.next().name == "a"


def test_empty_palette_rejected():
    with pytest.raises(ValueError):
        ColorCycle([])


@pytest.mark.parametrize(
    "background, text",
    [("#FFFFFF", "#000000"), ("#000000", "#FFFFFF"), ("#F5C542", "#000000"),
     ("#2F3437", "#FFFFFF")],
)
def test_contrast_text(background, text):
    assert text_color_for(background) == text


def test_bad_color():
    with pytest.raises(ValueError):
        text_color_for("#FFF")


def test_palette_colors_are_valid():
    for color in PALETTE:
        assert text_color_for(color.hex) in ("#000000", "#FFFFFF")
