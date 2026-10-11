"""Тест сборки главного окна из main.py."""

import pytest

import main
from gui_lab.contacts_db import ContactsDB


def test_window_has_all_tabs():
    with ContactsDB() as db:
        window = main.create_window(db)
        titles = [window.tabs.tabText(i) for i in range(window.tabs.count())]
    assert titles == ["Калькулятор", "Цветная панель", "Секундомер",
                      "Контакты"]


def test_version_option(capsys):
    with pytest.raises(SystemExit) as exit_info:
        main.main(["--version"])
    assert exit_info.value.code == 0
    assert capsys.readouterr().out.strip() == "lab5 1.0.0"
