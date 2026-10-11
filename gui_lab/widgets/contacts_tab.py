"""Вкладка «Контакты» — графический интерфейс к базе SQLite."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from gui_lab.contacts_db import ContactsDB

COLUMNS = ("№", "Имя", "Телефон", "Почта")


class ContactsTab(QWidget):
    """Просмотр, поиск, добавление, изменение и удаление контактов.

    Таблица показывает записи из ContactsDB, поле поиска фильтрует их
    на лету. Выбор строки заполняет форму, из которой запись можно
    сохранить или удалить (с подтверждением). Ошибки ввода
    показываются в строке состояния под формой.
    """

    def __init__(self, db: ContactsDB) -> None:
        super().__init__()
        self.db = db
        self.search = QLineEdit(placeholderText="Поиск по имени, телефону "
                                                "или почте")
        self.search.textChanged.connect(self.refresh)
        self.table = self._create_table()
        self.name_edit = QLineEdit()
        self.phone_edit = QLineEdit(placeholderText="+7 900 123-45-67")
        self.email_edit = QLineEdit()
        form = QFormLayout()
        form.addRow("Имя:", self.name_edit)
        form.addRow("Телефон:", self.phone_edit)
        form.addRow("Почта:", self.email_edit)
        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_contact)
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_contact)
        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete_contact)
        self.clear_button = QPushButton("Очистить")
        self.clear_button.clicked.connect(self.clear_form)
        buttons = QHBoxLayout()
        for button in (self.add_button, self.save_button,
                       self.delete_button, self.clear_button):
            buttons.addWidget(button)
        self.status = QLabel()
        layout = QVBoxLayout(self)
        layout.addWidget(self.search)
        layout.addWidget(self.table, stretch=1)
        layout.addLayout(form)
        layout.addLayout(buttons)
        layout.addWidget(self.status)
        self.refresh()

    def _create_table(self) -> QTableWidget:
        """Создать таблицу контактов только для чтения."""
        table = QTableWidget(0, len(COLUMNS))
        table.setHorizontalHeaderLabels(COLUMNS)
        table.verticalHeader().setVisible(False)
        table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(True)
        table.itemSelectionChanged.connect(self.fill_form)
        return table

    def refresh(self) -> None:
        """Перечитать контакты из базы с учётом строки поиска."""
        contacts = self.db.find(self.search.text())
        self.table.setRowCount(len(contacts))
        for row, contact in enumerate(contacts):
            for column, value in enumerate(contact):
                item = QTableWidgetItem(str(value))
                item.setData(Qt.ItemDataRole.UserRole, contact.id)
                self.table.setItem(row, column, item)
        self._update_buttons()

    def selected_id(self) -> int | None:
        """id контакта в выбранной строке или None."""
        items = self.table.selectedItems()
        if not items:
            return None
        return items[0].data(Qt.ItemDataRole.UserRole)

    def select_contact(self, contact_id: int) -> None:
        """Выделить строку контакта с данным id, если она видна."""
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item.data(Qt.ItemDataRole.UserRole) == contact_id:
                self.table.selectRow(row)
                return

    def fill_form(self) -> None:
        """Перенести выбранный контакт в поля формы."""
        contact_id = self.selected_id()
        contact = None if contact_id is None else self.db.get(contact_id)
        if contact is not None:
            self.name_edit.setText(contact.name)
            self.phone_edit.setText(contact.phone)
            self.email_edit.setText(contact.email)
        self._update_buttons()

    def add_contact(self) -> None:
        """Добавить контакт из формы в базу."""
        try:
            new_id = self.db.add(*self._form_values())
        except ValueError as error:
            self.show_error(str(error))
            return
        name = self.name_edit.text().strip()
        self.search.clear()
        self.refresh()
        self.select_contact(new_id)
        self.show_message(f"Контакт «{name}» добавлен")

    def save_contact(self) -> None:
        """Сохранить изменения выбранного контакта."""
        contact_id = self.selected_id()
        if contact_id is None:
            self.show_error("выберите контакт в таблице")
            return
        try:
            self.db.update(contact_id, *self._form_values())
        except ValueError as error:
            self.show_error(str(error))
            return
        self.refresh()
        self.select_contact(contact_id)
        self.show_message("Изменения сохранены")

    def delete_contact(self) -> None:
        """Удалить выбранный контакт после подтверждения."""
        contact_id = self.selected_id()
        contact = None if contact_id is None else self.db.get(contact_id)
        if contact is None:
            self.show_error("выберите контакт в таблице")
            return
        if not self.confirm(f"Удалить контакт «{contact.name}»?"):
            return
        self.db.delete(contact.id)
        self.clear_form()
        self.refresh()
        self.show_message(f"Контакт «{contact.name}» удалён")

    def clear_form(self) -> None:
        """Очистить поля формы и снять выделение."""
        for edit in (self.name_edit, self.phone_edit, self.email_edit):
            edit.clear()
        self.table.clearSelection()

    def confirm(self, question: str) -> bool:
        """Спросить подтверждение у пользователя."""
        answer = QMessageBox.question(self, "Подтверждение", question)
        return answer == QMessageBox.StandardButton.Yes

    def show_message(self, text: str) -> None:
        """Показать сообщение об успешной операции."""
        self.status.setStyleSheet("color: #2E7D32;")
        self.status.setText(text)

    def show_error(self, text: str) -> None:
        """Показать сообщение об ошибке."""
        self.status.setStyleSheet("color: #C62828;")
        self.status.setText(f"Ошибка: {text}")

    def _form_values(self) -> tuple[str, str, str]:
        """Значения полей формы: имя, телефон, почта."""
        return (
            self.name_edit.text(),
            self.phone_edit.text(),
            self.email_edit.text(),
        )

    def _update_buttons(self) -> None:
        """Разрешить «Сохранить» и «Удалить» только при выбранной строке."""
        selected = self.selected_id() is not None
        self.save_button.setEnabled(selected)
        self.delete_button.setEnabled(selected)
