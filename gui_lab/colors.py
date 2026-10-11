"""Палитра цветной панели и выбор контрастного текста."""

from collections.abc import Sequence
from typing import NamedTuple


class Color(NamedTuple):
    """Цвет: название и запись #RRGGBB."""

    name: str
    hex: str


PALETTE = (
    Color("Небесный", "#4A90D9"),
    Color("Мятный", "#3EB489"),
    Color("Солнечный", "#F5C542"),
    Color("Коралловый", "#FF6F61"),
    Color("Сливовый", "#7B4B94"),
    Color("Графит", "#2F3437"),
)


class ColorCycle:
    """Перебор цветов палитры по кругу.

    current — текущий цвет, next — переход к следующему; после
    последнего цвета снова идёт первый.
    """

    def __init__(self, palette: Sequence[Color] = PALETTE) -> None:
        if not palette:
            raise ValueError("палитра пуста")
        self._palette = tuple(palette)
        self._index = 0

    @property
    def current(self) -> Color:
        """Текущий цвет."""
        return self._palette[self._index]

    def next(self) -> Color:
        """Перейти к следующему цвету и вернуть его."""
        self._index = (self._index + 1) % len(self._palette)
        return self.current


def text_color_for(background: str) -> str:
    """Подобрать чёрный или белый текст для фона #RRGGBB.

    Используется относительная яркость по формуле WCAG: на светлом
    фоне текст чёрный, на тёмном — белый.
    """
    value = background.lstrip("#")
    if len(value) != 6:
        raise ValueError(f"ожидался цвет #RRGGBB: {background!r}")
    channels = [int(value[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [
        c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        for c in channels
    ]
    luminance = 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]
    return "#000000" if luminance > 0.179 else "#FFFFFF"
