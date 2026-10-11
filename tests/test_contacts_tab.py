"""Тесты вкладки «Контакты» — GUI к базе SQLite."""

import pytest

from gui_lab.contacts_db import ContactsDB
from gui_lab.widgets.contacts_tab import ContactsTab


@pytest.fixture
def tab():
    with ContactsDB() as db:
        db.add("Ольга", "+7 900 111-22-33", "olga@example.ru")
        db.add("Андрей", "8 (495) 123-45-67")
        widget = ContactsTab(db)
        widget.confirm = lambda question: True
        yield widget


def table_names(tab):
    return [tab.table.item(r, 1).text() for r in range(tab.table.rowCount())]


def fill(tab, name, phone, email=""):
    tab.name_edit.setText(name)
    tab.phone_edit.setText(phone)
    tab.email_edit.setText(email)


def test_table_shows_contacts(tab):
    assert table_names(tab) == ["Андрей", "Ольга"]
    assert not tab.save_button.isEnabled()


def test_add_contact(tab):
    fill(tab, "Борис", "12345", "b@example.ru")
    tab.add_button.click()
    assert table_names(tab) == ["Андрей", "Борис", "Ольга"]
    assert tab.selected_id() is not None
    assert "добавлен" in tab.status.text()


def test_add_invalid_contact_shows_error(tab):
    fill(tab, "", "12345")
    tab.add_button.click()
    assert tab.status.text().startswith("Ошибка")
    assert table_names(tab) == ["Андрей", "Ольга"]


def test_select_fills_form_and_save(tab):
    tab.table.selectRow(1)
    assert tab.name_edit.text() == "Ольга"
    tab.name_edit.setText("Ольга Петрова")
    tab.save_button.click()
    assert table_names(tab) == ["Андрей", "Ольга Петрова"]


def test_search_filters_table(tab):
    tab.search.setText("495")
    assert table_names(tab) == ["Андрей"]
    tab.search.clear()
    assert len(table_names(tab)) == 2


def test_delete_with_confirmation(tab):
    tab.table.selectRow(0)
    tab.delete_button.click()
    assert table_names(tab) == ["Ольга"]
    assert "удалён" in tab.status.text()


def test_delete_cancelled(tab):
    tab.confirm = lambda question: False
    tab.table.selectRow(0)
    tab.delete_button.click()
    assert table_names(tab) == ["Андрей", "Ольга"]
