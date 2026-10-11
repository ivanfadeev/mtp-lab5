"""Логика секундомера с кругами."""

import time
from collections.abc import Callable


class Stopwatch:
    """Секундомер: старт, пауза, круги и сброс.

    Время берётся из функции clock (по умолчанию time.monotonic,
    которую не сбивает перевод системных часов). В тестах вместо неё
    подставляются «ручные» часы.
    """

    def __init__(self, clock: Callable[[], float] = time.monotonic) -> None:
        self._clock = clock
        self._accumulated = 0.0
        self._started_at: float | None = None
        self._laps: list[float] = []

    @property
    def running(self) -> bool:
        """Идёт ли отсчёт времени."""
        return self._started_at is not None

    @property
    def elapsed(self) -> float:
        """Прошедшее время в секундах с учётом пауз."""
        if self._started_at is None:
            return self._accumulated
        return self._accumulated + self._clock() - self._started_at

    @property
    def laps(self) -> tuple[float, ...]:
        """Длительности кругов в секундах."""
        return tuple(self._laps)

    def start(self) -> None:
        """Запустить или продолжить отсчёт; повторный вызов игнорируется."""
        if self._started_at is None:
            self._started_at = self._clock()

    def stop(self) -> None:
        """Поставить на паузу; накопленное время сохраняется."""
        if self._started_at is not None:
            self._accumulated = self.elapsed
            self._started_at = None

    def lap(self) -> float:
        """Закончить текущий круг и вернуть его длительность.

        Круг можно отметить только во время отсчёта.
        """
        if not self.running:
            raise RuntimeError("секундомер не запущен")
        duration = self.elapsed - sum(self._laps)
        self._laps.append(duration)
        return duration

    def reset(self) -> None:
        """Остановить секундомер, обнулить время и круги."""
        self._accumulated = 0.0
        self._started_at = None
        self._laps.clear()


def format_time(seconds: float) -> str:
    """Записать время как ММ:СС.сс или Ч:ММ:СС.сс, если прошёл час."""
    if seconds < 0:
        raise ValueError("время не может быть отрицательным")
    hundredths = int(round(seconds * 100))
    minutes, rest = divmod(hundredths, 6000)
    secs, cents = divmod(rest, 100)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}.{cents:02d}"
    return f"{minutes:02d}:{secs:02d}.{cents:02d}"
