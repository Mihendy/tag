from PyQt5.QtWidgets import QLabel


class Frame(QLabel):
    """Класс стиллизированной рамки"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
