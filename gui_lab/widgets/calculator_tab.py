"""Вкладка простейшего калькулятора."""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QKeyEvent
from PyQt6.QtWidgets import QGridLayout, QLineEdit, QPushButton, QWidget

from gui_lab.calculator import DIGITS, Calculator

# клавиша: (строка, столбец, высота, ширина) в сетке кнопок
BUTTONS = {
    "C": (0, 0, 1, 1), "←": (0, 1, 1, 1), "÷": (0, 2, 1, 1),
    "×": (0, 3, 1, 1),
    "7": (1, 0, 1, 1), "8": (1, 1, 1, 1), "9": (1, 2, 1, 1),
    "−": (1, 3, 1, 1),
    "4": (2, 0, 1, 1), "5": (2, 1, 1, 1), "6": (2, 2, 1, 1),
    "+": (2, 3, 1, 1),
    "1": (3, 0, 1, 1), "2": (3, 1, 1, 1), "3": (3, 2, 1, 1),
    "=": (3, 3, 2, 1),
    "0": (4, 0, 1, 2), ".": (4, 2, 1, 1),
}
KEYBOARD = {
    Qt.Key.Key_Plus: "+",
    Qt.Key.Key_Minus: "−",
    Qt.Key.Key_Asterisk: "×",
    Qt.Key.Key_Slash: "÷",
    Qt.Key.Key_Equal: "=",
    Qt.Key.Key_Return: "=",
    Qt.Key.Key_Enter: "=",
    Qt.Key.Key_Escape: "C",
    Qt.Key.Key_Backspace: "←",
    Qt.Key.Key_Period: ".",
    Qt.Key.Key_Comma: ".",
}


class CalculatorTab(QWidget):
    """Калькулятор: экран, сетка кнопок и ввод с клавиатуры.

    Нажатия кнопок и клавиш передаются в логику Calculator, а её
    ответ выводится на экран. С клавиатуры работают цифры, «+ - * /»,
    Enter или «=», Backspace и Esc (сброс).
    """

    def __init__(self, calculator: Calculator | None = None) -> None:
        super().__init__()
        self.calculator = calculator if calculator is not None else (
            Calculator()
        )
        self.display = QLineEdit(self.calculator.display)
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFont(QFont(self.display.font().family(), 24))
        self.display.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        grid = QGridLayout(self)
        grid.addWidget(self.display, 0, 0, 1, 4)
        self.buttons: dict[str, QPushButton] = {}
        for key, (row, column, height, width) in BUTTONS.items():
            button = QPushButton(key)
            button.setMinimumHeight(44)
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            button.clicked.connect(lambda _, pressed=key: self.press(pressed))
            grid.addWidget(button, row + 1, column, height, width)
            self.buttons[key] = button
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def press(self, key: str) -> None:
        """Передать нажатую клавишу калькулятору и обновить экран."""
        self.display.setText(self.calculator.press(key))

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Обработать нажатие клавиши на клавиатуре."""
        text = event.text()
        if len(text) == 1 and text in DIGITS:
            self.press(text)
        elif event.key() in KEYBOARD:
            self.press(KEYBOARD[event.key()])
        else:
            super().keyPressEvent(event)
