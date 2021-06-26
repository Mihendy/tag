from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QLabel, QApplication, QPushButton
from PyQt5 import QtCore
from tools import SIZE, shadowEffect


class PictureButton(QLabel):
    """Кнопка-изображение (QLabel, в котором находится Pixmap - Кнопка в формате svg)"""

    def __init__(self, *args, way=None, **kwargs):
        super().__init__(*args, *kwargs)
        if not way:
            self.icon = QIcon('icons/arrow.ico')
        else:
            self.icon = QIcon(way)
        # Так как увеличение размера QLabel не увеличит картинку,
        # находящуюся в нём (PixMap) Растянем картинку отдельно от QLabel,
        # потому как её формат (svg - формат векторного изображения) позволяет нам сделать это.
        self.pix = self.icon.pixmap(QSize(SIZE // 20, SIZE // 20))
        self.big_pix = self.icon.pixmap(QSize(int(SIZE // 20 * 1.25),
                                              int(SIZE // 20 * 1.25)))
        self.move(SIZE // 50 + SIZE // 100, SIZE // 25)
        self.setPixmap(self.pix)
        self.resize(SIZE // 20, SIZE // 20)

    def enterEvent(self, event):
        """Увеличение размера кнопки при наведении"""
        # Так как в отличие от обычного QPushButton с помощью resize
        # Размер самой картинки не изменится, не забываем про установку self.big_pix
        QApplication.setOverrideCursor(QtCore.Qt.PointingHandCursor)
        self.resize(QSize(int(SIZE // 20 * 1.25), int(SIZE // 20 * 1.25)))
        self.move(SIZE // 50, int(SIZE // 50 * 1.5))
        self.setPixmap(self.big_pix)

    def leaveEvent(self, event):
        """Приведение кнопки в привычное положение, при снятии курсора с неё"""
        # (Устанавливаем self.pix для Pixmap)
        QApplication.setOverrideCursor(QtCore.Qt.ArrowCursor)
        self.resize(QSize(SIZE // 20, SIZE // 20))
        self.move(int(SIZE // 50 * 1.5), SIZE // 25)
        self.setPixmap(self.pix)


class MyButton(QPushButton):
    """Класс обычной кнопки"""

    def __init__(self, *args, **kwargs):
        """Инициализация стилей кнопки"""
        super().__init__(*args, *kwargs)
        self.setStyleSheet(f'border-radius: {SIZE // 50 + SIZE // 100}px;')
        color = QColor('gray' if args[1].dark_mode else 'black')
        shadowEffect(self, color)

    def enterEvent(self, event):
        """Изменение стилей кнопки при наведении"""
        QApplication.setOverrideCursor(QtCore.Qt.PointingHandCursor)

    def leaveEvent(self, event):
        """Установка начальных стилей для кнопки при снятии курсора с неё"""
        QApplication.setOverrideCursor(QtCore.Qt.ArrowCursor)