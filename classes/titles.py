from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from tools import SIZE, COOL_FONT, shadowEffect


class Title(QLabel):
    """Класс названий окон"""

    #  P.S. на первый взгляд это просто копия QLabel, но
    #  дело в том, что стили, прописанные в /data/styles.css, работают
    #  для этого класса по-другому.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)


class SubTitle(QLabel):
    """Класс подзаголовков"""

    # Работа стилей отлична от работы стилей для родительского класса (QLabel)
    # P.s. Стили прописанны в /data/styles.css.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.resize(int(SIZE // 5 + SIZE // 6.25), SIZE // 10 + SIZE // 100)
        self.move((SIZE - self.size().width()) // 2, SIZE // 100)
        self.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.setFont(COOL_FONT)
        self.setStyleSheet(f'''font-size: {SIZE // 25}pt;''')
        color = QColor('gray' if args[1].dark_mode else 'black')
        shadowEffect(self, color)
