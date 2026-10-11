"""Логика простейшего калькулятора без привязки к интерфейсу."""

from decimal import Decimal, DivisionByZero, InvalidOperation

OPERATIONS = {
    "+": lambda left, right: left + right,
    "−": lambda left, right: left - right,
    "×": lambda left, right: left * right,
    "÷": lambda left, right: left / right,
}
DIGITS = "0123456789"
MAX_DIGITS = 15
ERROR = "Ошибка"


class Calculator:
    """Карманный калькулятор с немедленным выполнением операций.

    Как у обычного калькулятора, выражение считается слева направо:
    2 + 3 × 4 = даёт 20. Вычисления идут в Decimal, поэтому
    0.1 + 0.2 = 0.3 без ошибок округления. Деление на ноль переводит
    калькулятор в состояние «Ошибка», из которого выводит любая
    следующая клавиша.
    """

    def __init__(self) -> None:
        self.clear()

    @property
    def display(self) -> str:
        """Текст на экране калькулятора."""
        return self._display

    def clear(self) -> None:
        """Сбросить всё (клавиша C)."""
        self._display = "0"
        self._accumulator: Decimal | None = None
        self._operation: str | None = None
        self._start_new = True

    def press(self, key: str) -> str:
        """Обработать нажатие клавиши и вернуть новый текст экрана.

        Клавиши: цифры 0–9, «.», операции «+ − × ÷», «=», «C» (сброс)
        и «←» (стереть последний символ). Неизвестная клавиша
        вызывает ValueError.
        """
        if self._display == ERROR and key != "C":
            self.clear()
        if len(key) == 1 and key in DIGITS:
            self._input_digit(key)
        elif key == ".":
            self._input_point()
        elif key in OPERATIONS:
            self._choose_operation(key)
        elif key == "=":
            self._calculate()
            self._operation = None
        elif key == "C":
            self.clear()
        elif key == "←":
            self._backspace()
        else:
            raise ValueError(f"неизвестная клавиша: {key!r}")
        return self._display

    def _input_digit(self, digit: str) -> None:
        """Дописать цифру к текущему числу."""
        if self._start_new or self._display == "0":
            self._display = digit
            self._start_new = False
        elif len(self._display.replace(".", "")) < MAX_DIGITS:
            self._display += digit

    def _input_point(self) -> None:
        """Поставить десятичную точку, если её ещё нет."""
        if self._start_new:
            self._display = "0."
            self._start_new = False
        elif "." not in self._display:
            self._display += "."

    def _backspace(self) -> None:
        """Стереть последний введённый символ числа."""
        if self._start_new:
            return
        self._display = self._display[:-1] or "0"
        if self._display == "-":
            self._display = "0"

    def _choose_operation(self, operation: str) -> None:
        """Запомнить операцию; повторное нажатие заменяет её."""
        if not self._start_new:
            self._calculate()
        if self._display != ERROR:
            self._operation = operation

    def _calculate(self) -> None:
        """Применить отложенную операцию к накопленному и текущему числу."""
        current = Decimal(self._display)
        if self._operation is None or self._accumulator is None:
            self._accumulator = current
        else:
            try:
                result = OPERATIONS[self._operation](
                    self._accumulator, current
                )
            except (DivisionByZero, InvalidOperation):
                self._display = ERROR
                self._accumulator = None
                self._start_new = True
                return
            self._accumulator = result
        self._display = format_number(self._accumulator)
        self._start_new = True


def format_number(value: Decimal) -> str:
    """Записать число без экспоненты и лишних нулей.

    Дробная часть округляется до 10 знаков, так что 1 ÷ 3 даёт
    0.3333333333, а не бесконечную дробь.
    """
    rounded = value.quantize(Decimal("1e-10")).normalize()
    text = format(rounded, "f")
    return "0" if text == "-0" else text
