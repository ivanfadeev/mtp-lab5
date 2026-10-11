"""Тесты хранения контактов в SQLite."""

import pytest

from gui_lab.contacts_db import Contact, ContactsDB


@pytest.fixture
def db():
    with ContactsDB() as database:
        database.add("Ольга", "+7 900 111-22-33", "olga@example.ru")
        database.add("андрей", "8 (495) 123-45-67")
        yield database


def test_add_and_get(db):
    new_id = db.add("  Борис ", "12345", " ")
    assert db.get(new_id) == Contact(new_id, "Борис", "12345", "")


def test_find_all_sorted_by_name(db):
    assert [c.name for c in db.find()] == ["андрей", "Ольга"]


@pytest.mark.parametrize(
    "text, names",
    [("ОЛЬ", ["Ольга"]), ("Андр", ["андрей"]), ("495", ["андрей"]),
     ("example", ["Ольга"]), ("нет такого", [])],
)
def test_find_is_case_insensitive(db, text, names):
    assert [c.name for c in db.find(text)] == names


def test_update(db):
    contact = db.find("Ольга")[0]
    assert db.update(contact.id, "Ольга К.", "+7 900 000-00-00")
    assert db.get(contact.id).name == "Ольга К."
    assert db.update(999, "Кто-то", "12345") is False


def test_delete(db):
    contact = db.find("андрей")[0]
    assert db.delete(contact.id) is True
    assert db.delete(contact.id) is False
    assert db.get(contact.id) is None


@pytest.mark.parametrize(
    "name, phone, email",
    [("", "12345", ""), ("Имя", "12-34", ""), ("Имя", "телефон", ""),
     ("Имя", "12345", "без собаки"), ("Имя", "١٢٣٤٥٦", "")],
)
def test_validation(db, name, phone, email):
    with pytest.raises(ValueError):
        db.add(name, phone, email)
    assert len(db.find()) == 2


def test_quotes_do_not_break_sql(db):
    tricky = "Robert'); DROP TABLE contacts;--"
    new_id = db.add(tricky, "12345")
    assert db.get(new_id).name == tricky
    assert len(db.find()) == 3


def test_data_survives_reopen(tmp_path):
    path = tmp_path / "book.db"
    with ContactsDB(path) as first:
        first.add("Вера", "54321")
    with ContactsDB(path) as second:
        assert [c.name for c in second.find()] == ["Вера"]
