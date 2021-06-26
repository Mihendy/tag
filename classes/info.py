from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont, QFontDatabase


class Information(QLabel):
    """Класс пояснительного комментария в программе"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        QFontDatabase.addApplicationFont("data/HoboStd.otf")
        self.setFont(QFont("Clickuper"))
        self.setStyleSheet(f"""
                    font-size: 8pt;
                    font-bold: bold;
                    color: #cfcfcf;
        """)