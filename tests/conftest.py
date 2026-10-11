"""Общая фикстура: одно приложение Qt на все тесты, без показа окон."""

import os

import pytest
from PyQt6.QtWidgets import QApplication


@pytest.fixture(scope="session", autouse=True)
def qapp():
    """Создать QApplication в offscreen-режиме (окна не появляются)."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    app = QApplication.instance() or QApplication([])
    yield app
