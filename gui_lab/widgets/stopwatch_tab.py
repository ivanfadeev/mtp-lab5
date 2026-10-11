"""Вкладка секундомера с кругами."""

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from gui_lab.stopwatch import Stopwatch, format_time


class StopwatchTab(QWidget):
    """Секундомер: табло, кнопки «Старт/Пауза», «Круг», «Сброс» и круги.

    Пока отсчёт идёт, QTimer несколько раз в секунду обновляет табло;
    само время считает Stopwatch, поэтому задержки таймера Qt на
    точность не влияют.
    """

    def __init__(
        self, stopwatch: Stopwatch | None = None, interval_ms: int = 31
    ) -> None:
        super().__init__()
        self.stopwatch = stopwatch if stopwatch is not None else Stopwatch()
        self.time_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.time_label.setFont(QFont("Menlo", 40))
        self.start_button = QPushButton("Старт")
        self.start_button.clicked.connect(self.toggle)
        self.lap_button = QPushButton("Круг")
        self.lap_button.clicked.connect(self.add_lap)
        self.reset_button = QPushButton("Сброс")
        self.reset_button.clicked.connect(self.reset)
        self.laps_list = QListWidget()
        self.timer = QTimer(self)
        self.timer.setInterval(interval_ms)
        self.timer.timeout.connect(self.refresh)

        buttons = QHBoxLayout()
        for button in (self.start_button, self.lap_button, self.reset_button):
            buttons.addWidget(button)
        layout = QVBoxLayout(self)
        layout.addWidget(self.time_label)
        layout.addLayout(buttons)
        layout.addWidget(QLabel("Круги (последний — сверху):"))
        layout.addWidget(self.laps_list, stretch=1)
        self._update_buttons()
        self.refresh()

    def toggle(self) -> None:
        """Запустить секундомер или поставить его на паузу."""
        if self.stopwatch.running:
            self.stopwatch.stop()
            self.timer.stop()
        else:
            self.stopwatch.start()
            self.timer.start()
        self._update_buttons()
        self.refresh()

    def add_lap(self) -> None:
        """Отметить круг и добавить его в начало списка."""
        duration = self.stopwatch.lap()
        number = len(self.stopwatch.laps)
        self.laps_list.insertItem(0, f"Круг {number}: {format_time(duration)}")

    def reset(self) -> None:
        """Остановить и обнулить секундомер, очистить круги."""
        self.stopwatch.reset()
        self.timer.stop()
        self.laps_list.clear()
        self._update_buttons()
        self.refresh()

    def refresh(self) -> None:
        """Показать на табло текущее время."""
        self.time_label.setText(format_time(self.stopwatch.elapsed))

    def _update_buttons(self) -> None:
        """Обновить подписи и доступность кнопок по состоянию."""
        running = self.stopwatch.running
        if running:
            self.start_button.setText("Пауза")
        elif self.stopwatch.elapsed > 0:
            self.start_button.setText("Продолжить")
        else:
            self.start_button.setText("Старт")
        self.lap_button.setEnabled(running)
