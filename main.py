"""Лабораторная работа №5: графический интерфейс на PyQt6.

Автор: Фадеев Иван Александрович, группа 221141, вариант 7.
"""

import argparse

APP_NAME = "lab5"
APP_VERSION = "1.0.0"


def build_parser() -> argparse.ArgumentParser:
    """Собрать разбор аргументов командной строки."""
    parser = argparse.ArgumentParser(
        prog=APP_NAME,
        description="Графический интерфейс на PyQt6 (вариант 7)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {APP_VERSION}",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    """Разобрать аргументы командной строки."""
    build_parser().parse_args(argv)


if __name__ == "__main__":
    main()
