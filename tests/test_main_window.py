"""Тесты главного окна и меню «Файл → Выход»."""

from PyQt6.QtGui import QKeySequence
from PyQt6.QtWidgets import QLabel

from gui_lab.widgets.main_window import MainWindow


def test_file_menu_has_exit():
    window = MainWindow()
    titles = [action.text() for action in window.menuBar().actions()]
    assert titles == ["Файл", "Справка"]
    assert [a.text() for a in window.file_menu.actions()] == ["Выход"]
    assert window.exit_action.shortcut() == QKeySequence(
        QKeySequence.StandardKey.Quit
    )


def test_exit_closes_window():
    window = MainWindow()
    window.show()
    assert window.isVisible()
    window.exit_action.trigger()
    assert not window.isVisible()


def test_menu_is_inside_window():
    assert MainWindow().menuBar().isNativeMenuBar() is False


def test_tabs_are_added_in_order():
    window = MainWindow([("Первая", QLabel("1")), ("Вторая", QLabel("2"))])
    titles = [window.tabs.tabText(i) for i in range(window.tabs.count())]
    assert titles == ["Первая", "Вторая"]
