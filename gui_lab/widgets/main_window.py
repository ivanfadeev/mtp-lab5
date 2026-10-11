"""Главное окно приложения с меню «Файл → Выход»."""

from collections.abc import Sequence

from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTabWidget, QWidget

APP_TITLE = "Лабораторная №5 — графический интерфейс"


class MainWindow(QMainWindow):
    """Главное окно: меню и вкладки с заданиями.

    Меню «Файл» содержит пункт «Выход» с сочетанием Ctrl+Q (Cmd+Q на
    macOS), который закрывает окно, меню «Справка» — сведения о
    программе. Меню встроено в окно и на macOS, а не вынесено в
    системную строку меню, чтобы выглядеть одинаково на всех системах.
    """

    def __init__(
        self,
        tabs: Sequence[tuple[str, QWidget]] = (),
        version: str = "",
    ) -> None:
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self._version = version
        self.tabs = QTabWidget()
        for title, widget in tabs:
            self.tabs.addTab(widget, title)
        self.setCentralWidget(self.tabs)
        self.menuBar().setNativeMenuBar(False)
        self.file_menu = self.menuBar().addMenu("Файл")
        self.exit_action = self._create_exit_action()
        self.file_menu.addAction(self.exit_action)
        help_menu = self.menuBar().addMenu("Справка")
        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        self.statusBar().showMessage("Готово")

    def _create_exit_action(self) -> QAction:
        """Создать пункт меню «Выход», закрывающий окно."""
        action = QAction("Выход", self)
        action.setShortcut(QKeySequence.StandardKey.Quit)
        action.setMenuRole(QAction.MenuRole.NoRole)
        action.setStatusTip("Закрыть приложение")
        action.triggered.connect(self.close)
        return action

    def show_about(self) -> None:
        """Показать окно «О программе»."""
        QMessageBox.about(
            self,
            "О программе",
            f"{APP_TITLE}\nВерсия {self._version}\n"
            "Фадеев Иван Александрович, группа 221141, вариант 7",
        )
