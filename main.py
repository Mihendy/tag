"""Версия 1.1"""
import sys

from PyQt5.QtWidgets import QApplication

from classes.main_window import MainWindow

"""
В коде программы ниже представлены классы для различных обьектов,
которые используются в программе в качестве виджетов.
В основном, в таких классах описаны события и стили для виджетов. (дириктория classes)
"""


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def main():
    """Непосредственно запуск приложения"""
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
