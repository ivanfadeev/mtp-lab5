"""Тесты вкладки с цветной панелью."""

from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest

from gui_lab.colors import PALETTE
from gui_lab.widgets.color_panel import ColorPanel


def test_starts_with_first_color():
    panel = ColorPanel()
    assert PALETTE[0].hex in panel.panel.styleSheet()
    assert panel.caption.text() == f"{PALETTE[0].name}\n{PALETTE[0].hex}"


def test_button_click_changes_color():
    panel = ColorPanel()
    QTest.mouseClick(panel.button, Qt.MouseButton.LeftButton)
    assert panel.current_color == PALETTE[1]
    assert PALETTE[1].hex in panel.panel.styleSheet()
    assert PALETTE[1].name in panel.caption.text()


def test_full_circle_returns_to_first():
    panel = ColorPanel()
    for _ in PALETTE:
        panel.button.click()
    assert panel.current_color == PALETTE[0]


def test_dark_background_gets_white_text():
    panel = ColorPanel()
    while panel.current_color.name != "Графит":
        panel.button.click()
    assert "#FFFFFF" in panel.caption.styleSheet()
