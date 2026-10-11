"""Лабораторная работа №5: графический интерфейс на PyQt6.

Окно с меню «Файл → Выход» и вкладками: калькулятор, цветная панель,
секундомер и телефонная книга в базе SQLite.
Автор: Фадеев Иван Александрович, группа 221141, вариант 7.
"""

import argparse
import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from gui_lab.contacts_db import ContactsDB
from gui_lab.widgets.calculator_tab import CalculatorTab
from gui_lab.widgets.color_panel import ColorPanel
from gui_lab.widgets.contacts_tab import ContactsTab
from gui_lab.widgets.main_window import MainWindow
from gui_lab.widgets.stopwatch_tab import StopwatchTab

APP_NAME = "lab5"
APP_VERSION = "1.0.0"


def build_parser() -> argparse.ArgumentParser:
    """Собрать разбор аргументов командной строки."""
    parser = argparse.ArgumentParser(
        prog=APP_NAME,
        description="Графический интерфейс на PyQt6 (вариант 7)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {APP_VERSION}",
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=Path("contacts.db"),
        help="файл базы SQLite с контактами (по умолчанию contacts.db)",
    )
    return parser


def create_window(db: ContactsDB) -> MainWindow:
    """Собрать главное окно со всеми вкладками."""
    tabs = [
        ("Калькулятор", CalculatorTab()),
        ("Цветная панель", ColorPanel()),
        ("Секундомер", StopwatchTab()),
        ("Контакты", ContactsTab(db)),
    ]
    window = MainWindow(tabs, version=APP_VERSION)
    window.resize(560, 560)
    return window


def main(argv: list[str] | None = None) -> int:
    """Запустить приложение и вернуть код завершения цикла событий."""
    args = build_parser().parse_args(argv)
    app = QApplication.instance() or QApplication(sys.argv[:1])
    with ContactsDB(args.db) as db:
        window = create_window(db)
        window.show()
        return app.exec()


if __name__ == "__main__":
    sys.exit(main())
