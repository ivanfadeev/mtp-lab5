"""Хранение контактов в SQLite."""

import re
import sqlite3
from pathlib import Path
from typing import NamedTuple

PHONE_PATTERN = re.compile(r"^\+?[0-9 ()-]+$")


class Contact(NamedTuple):
    """Запись телефонной книги."""

    id: int
    name: str
    phone: str
    email: str


class ContactsDB:
    """Телефонная книга в базе SQLite.

    Все запросы параметризованы, поэтому кавычки и спецсимволы во
    вводе пользователя не ломают SQL. Путь ":memory:" создаёт базу в
    памяти — так её используют тесты.
    """

    def __init__(self, path: str | Path = ":memory:") -> None:
        self._connection = sqlite3.connect(str(path))
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS contacts (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                name  TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL DEFAULT ''
            )
            """
        )
        self._connection.commit()

    def add(self, name: str, phone: str, email: str = "") -> int:
        """Добавить контакт и вернуть его id."""
        values = validate(name, phone, email)
        with self._connection:
            cursor = self._connection.execute(
                "INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
                values,
            )
        return cursor.lastrowid

    def update(self, contact_id: int, name: str, phone: str,
               email: str = "") -> bool:
        """Изменить контакт; вернуть False, если такого id нет."""
        values = validate(name, phone, email)
        with self._connection:
            cursor = self._connection.execute(
                "UPDATE contacts SET name = ?, phone = ?, email = ? "
                "WHERE id = ?",
                (*values, contact_id),
            )
        return cursor.rowcount == 1

    def delete(self, contact_id: int) -> bool:
        """Удалить контакт; вернуть False, если такого id нет."""
        with self._connection:
            cursor = self._connection.execute(
                "DELETE FROM contacts WHERE id = ?", (contact_id,)
            )
        return cursor.rowcount == 1

    def find(self, text: str = "") -> list[Contact]:
        """Вернуть контакты, где имя, телефон или почта содержат text.

        Поиск по имени не зависит от регистра (в том числе для
        кириллицы), пустая строка возвращает все контакты.
        Результат отсортирован по имени.
        """
        rows = self._connection.execute(
            "SELECT id, name, phone, email FROM contacts"
        ).fetchall()
        needle = text.strip().casefold()
        contacts = [Contact(*row) for row in rows]
        found = [
            contact for contact in contacts
            if needle in contact.name.casefold()
            or needle in contact.phone
            or needle in contact.email.casefold()
        ]
        return sorted(found, key=lambda contact: contact.name.casefold())

    def get(self, contact_id: int) -> Contact | None:
        """Вернуть контакт по id или None."""
        row = self._connection.execute(
            "SELECT id, name, phone, email FROM contacts WHERE id = ?",
            (contact_id,),
        ).fetchone()
        return None if row is None else Contact(*row)

    def close(self) -> None:
        """Закрыть соединение с базой."""
        self._connection.close()

    def __enter__(self) -> "ContactsDB":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()


def validate(name: str, phone: str, email: str) -> tuple[str, str, str]:
    """Проверить и очистить поля контакта.

    Имя обязательно; в телефоне допустимы цифры, пробелы, скобки,
    дефис и «+» в начале, причём цифр не меньше пяти; почта
    необязательна, но если указана — должна содержать «@».
    """
    name, phone, email = name.strip(), phone.strip(), email.strip()
    if not name:
        raise ValueError("укажите имя")
    digits = re.findall(r"[0-9]", phone)
    if not PHONE_PATTERN.match(phone) or len(digits) < 5:
        raise ValueError("телефон: цифры, пробелы, скобки, дефис, «+»")
    if email and "@" not in email:
        raise ValueError("почта должна содержать @")
    return name, phone, email
