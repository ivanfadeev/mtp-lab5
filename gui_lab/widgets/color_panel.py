"""Вкладка с цветной панелью, меняющей цвет по кнопке."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QWidget

from gui_lab.colors import Color, ColorCycle, text_color_for


class ColorPanel(QWidget):
    """Цветная панель и кнопка «Сменить цвет».

    Каждое нажатие перекрашивает панель в следующий цвет палитры, а
    подпись с названием цвета становится чёрной или белой — в
    зависимости от того, что лучше читается на этом фоне.
    """

    def __init__(self, cycle: ColorCycle | None = None) -> None:
        super().__init__()
        self._cycle = cycle if cycle is not None else ColorCycle()
        self.panel = QFrame()
        self.panel.setObjectName("panel")
        self.panel.setMinimumSize(320, 220)
        self.caption = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        panel_layout = QVBoxLayout(self.panel)
        panel_layout.addWidget(self.caption)
        self.button = QPushButton("Сменить цвет")
        self.button.clicked.connect(self.next_color)
        layout = QVBoxLayout(self)
        layout.addWidget(self.panel, stretch=1)
        layout.addWidget(self.button)
        self._paint(self._cycle.current)

    @property
    def current_color(self) -> Color:
        """Цвет, в который сейчас окрашена панель."""
        return self._cycle.current

    def next_color(self) -> Color:
        """Перекрасить панель в следующий цвет и вернуть его."""
        color = self._cycle.next()
        self._paint(color)
        return color

    def _paint(self, color: Color) -> None:
        """Применить цвет к панели и обновить подпись."""
        self.panel.setStyleSheet(
            f"#panel {{ background-color: {color.hex}; border-radius: 10px; }}"
        )
        self.caption.setStyleSheet(
            f"color: {text_color_for(color.hex)}; font-size: 22px;"
        )
        self.caption.setText(f"{color.name}\n{color.hex}")
