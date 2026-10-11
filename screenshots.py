"""Снимки вкладок приложения для README без показа окон на экране.

Запуск из корня проекта:
    QT_QPA_PLATFORM=offscreen python screenshots.py
Снимки сохраняются в docs/screenshots. Для повторяемости секундомер
работает на «ручных» часах, а контакты берутся из базы в памяти.
"""

import sys
from pathlib import Path

from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QApplication

from gui_lab.contacts_db import ContactsDB
from gui_lab.stopwatch import Stopwatch
from gui_lab.widgets.calculator_tab import CalculatorTab
from gui_lab.widgets.color_panel import ColorPanel
from gui_lab.widgets.contacts_tab import ContactsTab
from gui_lab.widgets.main_window import MainWindow
from gui_lab.widgets.stopwatch_tab import StopwatchTab
from main import APP_VERSION

OUTPUT = Path("docs/screenshots")
CONTACTS = [
    ("Ольга Смирнова", "+7 900 111-22-33", "olga@example.ru"),
    ("Андрей Ковалёв", "8 (495) 123-45-67", ""),
    ("Мария Лебедева", "+7 912 555-01-02", "maria@example.ru"),
]


class ManualClock:
    """Часы, которые показывают заданное время."""

    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


def prepare(db: ContactsDB) -> tuple[MainWindow, ManualClock]:
    """Собрать окно и привести вкладки в показательное состояние."""
    for contact in CONTACTS:
        db.add(*contact)
    clock = ManualClock()
    calculator = CalculatorTab()
    for key in "1250×12=":
        calculator.press(key)
    colors = ColorPanel()
    colors.next_color()
    stopwatch = StopwatchTab(Stopwatch(clock))
    stopwatch.toggle()
    for moment in (12.48, 25.03, 38.91):
        clock.now = moment
        stopwatch.add_lap()
    clock.now = 43.27
    stopwatch.toggle()
    contacts = ContactsTab(db)
    contacts.table.selectRow(1)
    tabs = [
        ("Калькулятор", calculator),
        ("Цветная панель", colors),
        ("Секундомер", stopwatch),
        ("Контакты", contacts),
    ]
    window = MainWindow(tabs, version=APP_VERSION)
    window.resize(560, 560)
    return window, clock


def save_tabs(app: QApplication, window: MainWindow) -> None:
    """Сохранить снимок каждой вкладки."""
    names = ["calculator", "color_panel", "stopwatch", "contacts"]
    for index, name in enumerate(names):
        window.tabs.setCurrentIndex(index)
        app.processEvents()
        window.grab().save(str(OUTPUT / f"{name}.png"))


def save_menu(app: QApplication, window: MainWindow) -> None:
    """Сохранить снимок окна с раскрытым меню «Файл»."""
    window.tabs.setCurrentIndex(0)
    bar = window.menuBar()
    corner = bar.actionGeometry(window.file_menu.menuAction()).bottomLeft()
    window.file_menu.popup(window.mapToGlobal(bar.pos() + corner))
    app.processEvents()
    picture = window.grab()
    painter = QPainter(picture)
    painter.drawPixmap(QPoint(bar.pos() + corner), window.file_menu.grab())
    painter.end()
    window.file_menu.hide()
    picture.save(str(OUTPUT / "menu_file_exit.png"))


def main() -> None:
    """Сделать все снимки."""
    OUTPUT.mkdir(parents=True, exist_ok=True)
    app = QApplication.instance() or QApplication(sys.argv[:1])
    with ContactsDB() as db:
        window, _ = prepare(db)
        window.show()
        app.processEvents()
        save_tabs(app, window)
        save_menu(app, window)
    print(f"снимки сохранены в {OUTPUT}")


if __name__ == "__main__":
    main()
