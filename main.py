"""Версия 1.0"""
import sys
import time
from random import choice

from PyQt5 import QtCore
from PyQt5.QtCore import QRect, Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap, QKeyEvent, QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, \
    QMainWindow, QFileDialog, QInputDialog, QComboBox, \
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QPlainTextEdit, \
    QGraphicsDropShadowEffect

# В файле tools.py хранятся вспомогательные функции для работы с приложением,
# а также важные константы импортируем их:
from tools import *


def blur(obj, color: QColor):
    """Эффект теневого размытия"""
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(10)
    shadow.setXOffset(0)
    shadow.setYOffset(0)
    shadow.setColor(color)
    obj.setGraphicsEffect(shadow)


"""
В коде программы ниже представлены классы для различных обьектов,
которые используются в программе в качестве виджетов.
В основном, в таких классах описаны события и стили для виджетов.
"""


class Explanation(QLabel):
    """Класс пояснительного комментария в программе"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        QtGui.QFontDatabase.addApplicationFont("data/HoboStd.otf")
        self.setFont(QFont("Clickuper"))
        self.setStyleSheet(f"""
                    font-size: 8pt;
                    font-bold: bold;
                    color: #cfcfcf;
        """)


class Frame(QLabel):
    """Класс стиллизированной рамки"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)


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
        blur(self, color)


class MyButton(QPushButton):
    """Класс обычной кнопки"""

    def __init__(self, *args, **kwargs):
        """Инициализация стилей кнопки"""
        super().__init__(*args, *kwargs)
        self.setStyleSheet(f'border-radius: {SIZE // 50 + SIZE // 100}px;')
        color = QColor('gray' if args[1].dark_mode else 'black')
        blur(self, color)

    def enterEvent(self, event):
        """Изменение стилей кнопки при наведении"""
        QApplication.setOverrideCursor(QtCore.Qt.PointingHandCursor)

    def leaveEvent(self, event):
        """Установка начальных стилей для кнопки при снятии курсора с неё"""
        QApplication.setOverrideCursor(QtCore.Qt.ArrowCursor)


class MainWindow(QMainWindow):
    """Класс окна приложения"""

    def __init__(self):
        """Подготовка приложения к запуску"""
        super().__init__()

        # Инициализация непосредственно таблицы лидеров, и специального файла,
        # для хранения таблицы, если его ещё не существует в директории (FROM TOOLS.PY):
        make_game_files(self)
        self.leaders = []
        # Словарь, в котором хранятся контейнеры окон приложения,
        # содержащие соответствующие виджеты окна.
        self.window_widgets = {
            "main_menu": [],
            "game": [],
            "settings": [],
            "leader_board": [],
            "tips": []}

        self.setWindowTitle('Пятнашки')
        self.setGeometry(100, 100, 0, 0)
        self.setFixedSize(SIZE, SIZE)
        self.in_progress = True
        self.is_drawing = False
        self.dark_mode = False
        self.setWindowIcon(QIcon('icons/Window_icon.jpg'))
        self.statusBar().showMessage(VERSION)
        # В игре существуют режимы сложности, градация которых
        # связана с увеличением размера игрового поля
        # (выше сложность - больше поле, собирать его будет сложнее)
        self.num_of_br = {'hard': 16, 'normal': 9, 'easy': 4}
        # По умолчанию уровень сложности установлен простой,
        # для демонстрации работы приложения.
        self.difficulty = "easy"
        self.number_of_bricks = self.num_of_br[self.difficulty]
        self.n = 0
        self.cords_mtx = []
        QtGui.QFontDatabase.addApplicationFont("fonts/HoboStd.otf")
        self.init_ui()
        if self.dark_mode:
            self.setStyleSheet(open('css/_styles.CSS').read())
        else:
            self.setStyleSheet(open('css/styles.CSS').read())

    def clear_window(self):
        """Скрытие всех элементов с экрана приложения"""
        # from tools.py
        clear(self.window_widgets.values())

    def show_widgets(self, window):
        """Вывод окна 'window' на экран приложения"""
        # from tools.py
        show(self.window_widgets.get(window, "main_menu"))

    def init_ui(self):
        """Инициализация вспомогательных окон приложения (всех кроме окна игры)"""

        """ ИНИЦИАЛИЗАЦИЯ МЕНЮ """
        name_of_game = Title('Пятнашки', self)
        name_of_game.resize(SIZE // 5 * 2 + SIZE // 25, SIZE // 50 * 6)
        name_of_game.move((SIZE - name_of_game.size().width()) // 2, SIZE // 5)
        name_of_game.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        name_of_game.setFont(COOL_FONT)
        name_of_game.setStyleSheet(f'font-size: {SIZE // 25 + SIZE // 60}pt;')

        self.window_widgets["main_menu"].append(name_of_game)

        begin_btn = MyButton('Начать игру', self)
        begin_btn.id = START_GAME_BTN_ID
        begin_btn.setFont(COOL_FONT)
        begin_btn.resize(SIZE // 5 * 2, SIZE // 50 * 3)
        begin_btn.move((SIZE - begin_btn.size().width()) // 2, SIZE // 5 * 2)
        begin_btn.installEventFilter(self)

        self.window_widgets["main_menu"].append(begin_btn)

        settings_btn = MyButton('Настройки', self)
        settings_btn.id = SETTINGS_BTN_ID
        settings_btn.setFont(COOL_FONT)
        settings_btn.resize(SIZE // 5 * 2, SIZE // 50 * 3)
        settings_btn.move((SIZE - settings_btn.size().width()) // 2, SIZE // 2)
        settings_btn.installEventFilter(self)
        self.window_widgets["main_menu"].append(settings_btn)

        leader_board_btn = MyButton('Таблица лидеров', self)
        leader_board_btn.setFont(COOL_FONT)
        leader_board_btn.id = LEADER_BOARD_BTN_ID
        leader_board_btn.resize(SIZE // 5 * 2, SIZE // 50 * 3)
        leader_board_btn.move((SIZE - leader_board_btn.size().width()) // 2, SIZE // 5 * 3)
        leader_board_btn.installEventFilter(self)

        self.window_widgets["main_menu"].append(leader_board_btn)

        info_btn = MyButton('Обучение', self)
        info_btn.setFont(COOL_FONT)
        info_btn.id = HELP_BTN_ID
        info_btn.resize(SIZE // 5 * 2, SIZE // 50 * 3)
        info_btn.move((SIZE - info_btn.size().width()) // 2, SIZE * 7 // 10)
        info_btn.installEventFilter(self)

        self.window_widgets["main_menu"].append(info_btn)

        """ ИНИЦИАЛИЗАЦИЯ НАСТРОЕК ПРИЛОЖЕНИЯ (Сложности игры) """

        if self.dark_mode:
            go_to_menu_btn = PictureButton(self, way='icons/_arrow.ico')
        else:
            go_to_menu_btn = PictureButton(self)
        go_to_menu_btn.id = GO_TO_MAIN_MENU_BTN_ID
        go_to_menu_btn.installEventFilter(self)

        self.window_widgets["settings"].append(go_to_menu_btn)

        section_title = SubTitle('Настройки', self)

        self.window_widgets["settings"].append(section_title)

        difficulty = QLabel('Сложность', self)
        difficulty.setFont(COOL_FONT)
        difficulty.resize(SIZE // 5 + (SIZE // 100 * 7), SIZE // 10)
        difficulty.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        difficulty.move((SIZE - difficulty.size().width()) // 2, SIZE // 50 * 7)
        difficulty.setStyleSheet(f'''
                            border-radius: {SIZE // 100 + SIZE // 50}px;
                            color: white;
                            background-color: black;
                            font: url(HoboStd.otf);
                            font-size: {SIZE // 35}pt;
                        ''')

        self.window_widgets["settings"].append(difficulty)

        COOL_FONT.setPointSize(SIZE // 50)

        difficulty_easy = MyButton('Легко', self)
        difficulty_easy.id = EASY_BTN_ID
        difficulty_easy.setFont(COOL_FONT)
        difficulty_easy.resize(SIZE // 5 + SIZE // 10, SIZE // 5)
        difficulty_easy.move(SIZE // 50, SIZE // 5 + SIZE // 50 * 4)
        difficulty_easy.installEventFilter(self)

        self.window_widgets["settings"].append(difficulty_easy)

        difficulty_medium = MyButton('Нормально', self)
        difficulty_medium.id = NORMAL_BTN_ID
        difficulty_medium.setFont(COOL_FONT)
        difficulty_medium.resize(SIZE // 5 + SIZE // 10, SIZE // 5)
        difficulty_medium.move(SIZE // 5 + SIZE // 20 * 3, SIZE // 5 + SIZE // 50 * 4)
        difficulty_medium.installEventFilter(self)

        self.window_widgets["settings"].append(difficulty_medium)

        difficulty_hard = MyButton('Сложно', self)
        difficulty_hard.id = HARD_BTN_ID
        difficulty_hard.setFont(COOL_FONT)
        difficulty_hard.resize(SIZE // 5 + SIZE // 10, SIZE // 5)
        difficulty_hard.move(SIZE // 5 * 3 + SIZE // 50 * 4, SIZE // 5 + SIZE // 50 * 4)
        difficulty_hard.installEventFilter(self)

        self.window_widgets["settings"].append(difficulty_hard)

        dark_button = MyButton('', self)
        dark_button.id = DARK_MODE_BTN_ID
        dark_button.setFont(COOL_FONT)
        dark_button.resize(SIZE // 10, SIZE // 10)
        dark_button.move(SIZE // 100 * 95, SIZE // 100 * 95)
        dark_button.installEventFilter(self)

        self.window_widgets["settings"].append(dark_button)

        # # ---регулеровка звука с помощью слайдеров (работа с PyQTGraph в будующем)---
        # volume_lbl = QLabel('Звук', self)
        # volume_lbl.resize(200, 50)
        # volume_lbl.move(220, 230)
        #
        # volume_lbl.setStyleSheet('''
        #                     color: black;
        #                     font: url(HoboStd.otf);
        #                     font-size: 20pt;
        #                 ''')
        #
        # self.window_widgets["settings"].append(volume_lbl)
        #
        # vol_sld = QSlider(QtCore.Qt.Horizontal, self)
        # vol_sld.setValue(vol_sld.width() // 2)
        # vol_sld.resize(200, 20)
        # vol_sld.move(150, 300)
        #
        # self.window_widgets["settings"].append(vol_sld)
        #
        # music_lbl = QLabel('Музыка', self)
        # music_lbl.resize(200, 50)
        # music_lbl.move(200, 330)
        #
        # music_lbl.setStyleSheet('''
        #                     color: black;
        #                     font: url(HoboStd.otf);
        #                     font-size: 20pt;
        #                 ''')
        #
        # self.window_widgets["settings"].append(music_lbl)
        #
        # music_sld = QSlider(QtCore.Qt.Horizontal, self)
        # music_sld.setValue(music_sld.width() // 2)
        # music_sld.resize(200, 20)
        # music_sld.move(150, 400)
        #
        # self.window_widgets["settings"].append(music_sld)

        """ ИНИЦИАЛИЗАЦИЯ ОКНА ОБУЧЕНИЯ """

        section_title = SubTitle('Обучение', self)

        self.window_widgets["tips"].append(section_title)

        # go_to_menu_btn уже была инициализирована ранее.
        self.window_widgets["tips"].append(go_to_menu_btn)

        fine_layout = Frame('', self)
        fine_layout.resize(int(SIZE // 1.25 + SIZE // 6.25), int(SIZE // 5 + SIZE // 100))
        fine_layout.move(int(SIZE // 50), int(SIZE // 7.7))

        self.window_widgets["tips"].append(fine_layout)
        '''
        self.icon = QIcon('data/icons/arrow.svg') if not way else QIcon(way)
        # Так как увеличение размера QLabel не увеличит картинку,
        # находящуюся в нём (PixMap) Растянем картинку отдельно от QLabel,
        # потому как её формат (svg - формат векторного изображения) позволяет нам сделать это.
        self.pix = self.icon.pixmap(QSize(SIZE // 20, SIZE // 20))
        '''
        arrows_pix = QIcon('icons/keyboard.ico').pixmap(QSize(SIZE // 3, SIZE // 3))
        arrows = QLabel(self)
        arrows.resize(SIZE // 3, SIZE // 3)
        arrows.move(SIZE // 25, SIZE // 20 + SIZE // 50)
        arrows.setPixmap(arrows_pix)

        self.window_widgets["tips"].append(arrows)

        explanation_to_arrows = QLabel('', self)
        explanation_to_arrows.resize(int(SIZE // 2.5 + SIZE // 6.25), SIZE // 10)
        explanation_to_arrows.move(int(SIZE // 2.5), int(SIZE // 6.25 + SIZE // 100))
        font = QtGui.QFont('Arial', int(f'{SIZE // 50 + SIZE // 166}'))
        font.setBold(True)
        font.setStyle(QtGui.QFont.StyleItalic)
        exp = 'С помощью стрелочек можно\nдвигать части картинки'
        explanation_to_arrows.setText(exp)
        explanation_to_arrows.setFont(font)

        self.window_widgets["tips"].append(explanation_to_arrows)

        reference = QPlainTextEdit('', self)
        reference.resize(int(SIZE // 1.25 + SIZE // 6.25), int(SIZE // 1.6 + SIZE // 100))
        reference.move(SIZE // 50, int(SIZE // 5 + SIZE // 6.6))
        if self.dark_mode:
            reference.setStyleSheet(
                """
                                color: black;
                                border: 1px solid white;
                                border-radius: 5px;
                                background: gray;
                """)
        else:
            reference.setStyleSheet(
                """
                                color: black;
                                border: 1px solid black;
                                border-radius: 5px;
                                background: #d4d4d4;
                """)
        reference.setFont(QFont("fonts/HoboStd.odt", 15))
        reference.setReadOnly(True)
        reference.setPlainText(open("ref/Reference.txt", 'r', encoding='utf8').read())

        self.window_widgets["tips"].append(reference)

        """ ИНИЦИАЛИЗАЦИЯ ОКНА С ТАБЛИЦЕЙ ЛИДЕРОВ """

        # go_to_menu_btn уже была инициализирована ранее.
        self.window_widgets["leader_board"].append(go_to_menu_btn)

        section_title = SubTitle('Таблица лидеров', self)
        section_title.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        section_title.move(SIZE // 5 + SIZE // 100 * 7, SIZE // 100)
        section_title.resize(SIZE // 2 - SIZE // 25, SIZE // 10)
        section_title.setFont(COOL_FONT)
        section_title.setStyleSheet(f'''font-size: {SIZE // 30}pt;''')
        self.window_widgets["leader_board"].append(section_title)
        self.sort_by_difficulty = QComboBox(self)
        if self.dark_mode:
            self.sort_by_difficulty.setStyleSheet("""
                        background-color:  #cfcfcf;
                        QComboBox::down-arrow
                                                 {
                                                 border : 2px solid black;
                                                 border-width : 5px 1px 10px 3px;
                                                 color: #cfcfcf
                                                 };
                    border:                 none;
                     """)
        else:
            self.sort_by_difficulty.setStyleSheet("""
                background-color:  white;
                QComboBox::down-arrow
                                         {
                                         border : 2px solid black;
                                         border-width : 5px 1px 10px 3px;
                                         };
            border:                 none;
             """)

        self.sort_by_difficulty.resize(SIZE // 25 * 4, SIZE // 20)
        self.sort_by_difficulty.move(SIZE // 5 * 4 + SIZE // 50 + SIZE // 100,
                                     SIZE // 20 + SIZE // 50)
        self.sort_by_difficulty.addItem('easy')
        self.sort_by_difficulty.addItem('normal')
        self.sort_by_difficulty.addItem('hard')
        self.sort_by_difficulty.currentTextChanged.connect(self.tbl_update)

        self.window_widgets["leader_board"].append(self.sort_by_difficulty)

        self.leader_board = QTableWidget(self)
        self.leader_board.setFixedSize(SIZE + 3, SIZE - (SIZE // 50 * 6))
        self.leader_board.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.leader_board.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.leader_board.move(0, SIZE // 50 * 6)

        self.exp = Explanation(self)
        self.exp.resize(300, 30)
        self.exp.move(100, 200)
        self.window_widgets["leader_board"].append(self.exp)

        self.tbl_update()

        self.window_widgets["leader_board"].append(self.leader_board)

        self.clear_window()
        self.show_widgets("main_menu")

    def start_game(self):
        """Инициализация алгоритмов самой игры и всех окон, связанных с её началом"""
        self.statusBar().showMessage('')
        self.in_progress = False
        file_name = self.dialog()
        if not file_name:
            self.in_progress = True
            return

        pix_map = QPixmap(file_name)
        size = pix_map.size()
        if size.width() == 0 or size.height() == 0:
            return
        if size.width() != size.height():
            # проверяется тот факт, что картинка квадратная, если нет пользователь может её
            # отредактировать
            info = ('Внимание',
                    'Стороны картинки не пропорциональны.'
                    ' Выберите действие ниже:',
                    ['Сжать фото до разрешения 1:1',
                     'Обрезать лишнее'], 1, False)
            dialog = QInputDialog()
            name, ok_pressed = dialog.getItem(self, *info)
            if ok_pressed:
                if name == 'Обрезать лишнее':
                    min_side = min(size.width(), size.height())
                    rectangle = QRect(0, 0, min_side, min_side)
                    pix_map = pix_map.copy(rectangle)
                    self.clear_window()
            else:
                self.statusBar().showMessage(VERSION)
                self.in_progress = True
                return
        self.clear_window()
        # "разрезаем" изображение и и раскладываем каждый в свой pixmap
        pix_map = pix_map.scaled(SIZE, SIZE)
        self.n = int(self.number_of_bricks ** 0.5)
        pix_map_list = []
        for i in range(1, self.n + 1):
            for j in range(1, self.n + 1):
                if i == self.n and self.n == j:
                    break
                x1, y1 = (i - 1) * (SIZE // self.n), (j - 1) * (SIZE // self.n)
                rectangle = QRect(x1, y1, SIZE // self.n, SIZE // self.n)
                pix_map_list.append((pix_map.copy(rectangle), (i - 1, j - 1)))

        # раскладываем каждый pixmap в свой Qlable, заводим систему координат,
        # чтобы можно было понять, когда картинка собрана и где что находится.
        self.cords_mtx = []
        i = j = 0
        for i in range(1, self.n + 1):
            cords = []
            images = []
            for j in range(1, self.n + 1):
                image = QLabel(self)
                image.move(5 + (i - 1) * (SIZE // self.n + 5), 5 + (j - 1)
                           * (SIZE // self.n + 5))
                image.resize(SIZE // self.n, SIZE // self.n)
                if i == self.n == j:
                    cords.append((i - 1, j - 1))
                    images.append(None)
                    self.start_pos = (i - 1, j - 1)
                    break
                pixmap = pix_map_list.pop(0)
                image.setPixmap(pixmap[0])
                cords.append(pixmap[1])
                images.append(image)
            self.cords_mtx.append(cords)
            self.window_widgets["game"].append(images)

        self.setFixedSize(5 + SIZE + 5 * i, 5 + SIZE + 5 * j)
        self.field_generation()

        # проверка на мгновенный выйгрыш
        while win_check(self.cords_mtx):
            self.field_generation()
        self.show_widgets("game")
        self.start_time = time.time()
        self.update()
        self.setFocus()

    def settings(self):
        """Открытие окна настроек игры"""
        self.clear_window()
        self.show_widgets("settings")
        self.statusBar().showMessage(f'Cложность: {self.difficulty}')

    def tips(self):
        """Открытие окна справки по игре и советов по собиранию 'Пятнашек'"""
        self.clear_window()
        self.show_widgets("tips")
        self.statusBar().showMessage('')

    def leader_board_show(self):
        """Открытие окна таблицы лидеров"""
        self.clear_window()
        self.show_widgets("leader_board")
        self.statusBar().showMessage('')
        self.tbl_update()

    def field_generation(self):
        """Поле генерируется с помощью 1000 ходов, это могут быть
         правильные и неправильные ходы,
        программа мешает кирпичики не случайным образом,
         а как бы запутывает головоломку, делая случайный ход"""
        for _ in range(1000):
            key = choice((Qt.Key_Down, Qt.Key_Up, Qt.Key_Left, Qt.Key_Right))
            self.move_check(key)

    def move_check(self, key):
        """Проверка корректности хода игрока"""
        x, y = self.start_pos  # позиция без кирпичика
        if key == Qt.Key_Down:
            if y != 0:  # проверка, чтобы не выйти за края матриц и виджета,
                # такие попытки будут игнорироваться

                # меняем местами значения в матрицах
                self.cords_mtx[x][y], self.cords_mtx[x][y - 1] = \
                    self.cords_mtx[x][y - 1], self.cords_mtx[x][y]
                self.window_widgets["game"][x][y], \
                self.window_widgets["game"][x][y - 1] = \
                    self.window_widgets["game"][x][y - 1], \
                    self.window_widgets["game"][x][y]

                # поэтому меняем и позицию без кирпичика
                self.start_pos = (x, y - 1)
                self.window_widgets["game"][x][y].move(5 + x *
                                                       (SIZE // self.n + 5),
                                                       5 + y *
                                                       (SIZE // self.n + 5))

        # с другими кнопками всё тоже самое, только направления другие
        if key == Qt.Key_Up:
            if y != self.n - 1:
                self.cords_mtx[x][y], self.cords_mtx[x][y + 1] = \
                    self.cords_mtx[x][y + 1], self.cords_mtx[x][y]
                self.window_widgets["game"][x][y], \
                self.window_widgets["game"][x][y + 1] = \
                    self.window_widgets["game"][x][y + 1], \
                    self.window_widgets["game"][x][y]
                self.start_pos = (x, y + 1)
                self.window_widgets["game"][x][y].move(5 + x *
                                                       (SIZE // self.n + 5),
                                                       5 + y *
                                                       (SIZE // self.n + 5))
        if key == Qt.Key_Right:
            if x != 0:
                self.cords_mtx[x][y], self.cords_mtx[x - 1][y] = \
                    self.cords_mtx[x - 1][y], self.cords_mtx[x][y]
                self.window_widgets["game"][x][y], \
                self.window_widgets["game"][x - 1][y] = \
                    self.window_widgets["game"][x - 1][y], \
                    self.window_widgets["game"][x][y]
                self.start_pos = (x - 1, y)
                self.window_widgets["game"][x][y].move(5 + x *
                                                       (SIZE // self.n + 5),
                                                       5 + y *
                                                       (SIZE // self.n + 5))
        if key == Qt.Key_Left:
            if x != self.n - 1:
                self.cords_mtx[x][y], self.cords_mtx[x + 1][y] = \
                    self.cords_mtx[x + 1][y], self.cords_mtx[x][y]
                self.window_widgets["game"][x][y], \
                self.window_widgets["game"][x + 1][y] = \
                    self.window_widgets["game"][x + 1][y], \
                    self.window_widgets["game"][x][y]
                self.start_pos = (x + 1, y)
                self.window_widgets["game"][x][y].move(5 + x *
                                                       (SIZE // self.n + 5),
                                                       5 + y *
                                                       (SIZE // self.n + 5))

    def read_the_database(self):
        """Синхронизация базы данных лидеров с таблицей лидеров в самом приложении"""
        difficulties = {'easy': 1, 'normal': 2, 'hard': 3}
        con = sqlite3.connect('data/leaderboard.db')
        cur = con.cursor()
        self.leaders = cur.execute(f"""
        SELECT * FROM leaders
            WHERE difficulty = '{self.sort_by_difficulty.currentText()}'
        """).fetchall()
        con.close()
        for _ in range(len(self.leaders) - 1):
            for i in range(len(self.leaders) - 1):
                if difficulties[self.leaders[i][2]] > \
                        difficulties[self.leaders[i + 1][2]]:
                    self.leaders[i], self.leaders[i + 1] = self.leaders[i + 1], \
                                                           self.leaders[i]
                # Если вдруг в таблице встречаются два рекорда на одинаковой сложности
                # и с одинаковым отрезком времени с точностью до 0.001 секунды,
                # то правильно будет поставить на позицию выше самый новый результат,
                # так как в этом случае его данные будет актуальнее.
                # Поэтому ставим знак ">=":
                elif float(self.leaders[i][3]) >= float(self.leaders[i + 1][3]) and \
                        difficulties[self.leaders[i][2]] == \
                        difficulties[self.leaders[i + 1][2]]:
                    self.leaders[i], self.leaders[i + 1] = self.leaders[i + 1], \
                                                           self.leaders[i]

    def tbl_update(self):
        """Обновление данных таблицы лидеров, при постановлении нового рекорда игрока"""

        def set_row_color(_row, color):
            """Изменение цвета ячейки, находящейся в таблице лидеров"""
            for i in range(self.leader_board.columnCount()):
                self.leader_board.item(_row, i).setBackground(color)

        self.read_the_database()
        self.leader_board.setColumnCount(3)
        self.leader_board.setHorizontalHeaderLabels([
            'name', 'difficulty', 'time'
        ])
        self.leader_board.setRowCount(0)
        top = set()
        for row in range(len(self.leaders)):
            self.leader_board.setRowCount(self.leader_board.rowCount() + 1)
            for col in range(len(self.leaders[row]) - 1):
                if isinstance(self.leaders[row][col + 1], float):
                    win_time_console = self.leaders[row][col + 1]
                    win_time = [(int(win_time_console // 3600), 'ч.'),
                                (int(win_time_console // 60 % 60), 'мин.'),
                                ("%.3f" % (win_time_console % 60), 'сек.')]
                    elem = ''.join(list(map(
                        lambda x: f'{x[0]} {x[1]} '
                        if x[0] else '', win_time)))
                    elem = QTableWidgetItem(str(elem))
                else:
                    elem = QTableWidgetItem(str(self.leaders[row][col + 1]))
                elem.setFlags(QtCore.Qt.ItemIsEnabled)
                self.leader_board.setItem(
                    row, col, elem)
            clr = QColor(255, 255, 255)
            if len(top) <= 3:
                top.add(row)
                if len(top) == 1:
                    clr = QColor(255, 215, 0)
                elif len(top) == 2:
                    clr = QColor(151, 153, 151)
                elif len(top) == 3:
                    clr = QColor(150, 75, 0)
            set_row_color(self.leader_board.rowCount() - 1, clr)
        if self.leader_board.rowCount() == 0:
            self.exp.setText('В данной категории пока нет никаних \nрезультатов. '
                             'Будь первым!')
        else:
            self.exp.setText('')

    def eventFilter(self, obj, event):
        """Обработка событий для виджетов приложения"""
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if obj.id == START_GAME_BTN_ID:
                self.start_game()
            elif obj.id == HELP_BTN_ID:
                self.tips()
            elif obj.id == SETTINGS_BTN_ID:
                self.settings()
            elif obj.id in (EASY_BTN_ID, NORMAL_BTN_ID, HARD_BTN_ID):
                self.change_difficulty(obj)
            elif obj.id == LEADER_BOARD_BTN_ID:
                self.leader_board_show()
            elif obj.id == GO_TO_MAIN_MENU_BTN_ID:
                self.clear_window()
                self.statusBar().showMessage(VERSION)
                self.show_widgets("main_menu")
            elif obj.id == DARK_MODE_BTN_ID:
                self.dark_mode = not self.dark_mode
                self.clear_window()
                self.window_widgets = {
                    "main_menu": [],
                    "game": [],
                    "settings": [],
                    "leader_board": [],
                    "tips": []}
                self.init_ui()
                if self.dark_mode:
                    self.setStyleSheet(open('css/_styles.CSS').read())
                else:
                    self.setStyleSheet(open('css/styles.CSS').read())
                self.clear_window()
                self.show_widgets("settings")
            return True
        return False

    def keyPressEvent(self, event):
        """С помощью имеющихся в Qt QKeyEvent и keyPressEvent
         реализовано управление стрелочками"""
        key_event = QKeyEvent(event)
        key = key_event.key()
        if not self.in_progress:
            self.move_check(key)
            if win_check(self.cords_mtx):
                self.in_progress = True
                # определяем время сборки и делаем его читабельным
                win_time_console = round(time.time() - self.start_time, 3)
                win_time = [(int(win_time_console // 3600), 'ч.'),
                            (int(win_time_console // 60 % 60), 'мин.'),
                            ("%.3f" % (win_time_console % 60), 'сек.')]
                win_time = ''.join(list(map(
                    lambda x: f'{x[0]} {x[1]} '
                    if x[0] else '', win_time)))

                result = self.cur.execute(
                    f"""SELECT * FROM leaders
                    WHERE difficulty = '{self.difficulty}'""").fetchall()
                data = list(map(lambda x: str(x[1]), result))
                info = ('Победа', f'Ваш результат: {win_time}'
                                  f' Введите ваш ник:',
                        data, 1, True)
                name, ok_pressed = QInputDialog.getItem(self, *info)

                # вносим данные в файл с некоторыми поправками
                if not name or name.isspace():
                    # желательно, чтобы ник был из читабельных символов:
                    name = 'UnnamedPlayer'
                if ok_pressed:
                    if name not in data:
                        self.cur.execute(f"""
                                    INSERT INTO leaders(name,difficulty,time)
                                    VALUES('{name}','{self.difficulty}',
                                    {win_time_console})""")
                    else:
                        self.cur.execute(f"""UPDATE leaders
                                    SET time = {win_time_console} WHERE time >
                                    {win_time_console} and name = '{name}' 
                                    and difficulty = '{self.difficulty}'""")
                    self.con.commit()
                self.clear_window()
                self.window_widgets["game"] = []
                self.cords_mtx = []
                self.show_widgets("main_menu")
                self.statusBar().showMessage(VERSION)
                self.setFixedSize(SIZE, SIZE)

    def change_difficulty(self, btn):
        """Смена уровня сложности игры (размера поля)"""
        if btn.id == EASY_BTN_ID:
            self.difficulty = "easy"
        elif btn.id == NORMAL_BTN_ID:
            self.difficulty = "normal"
        elif btn.id == HARD_BTN_ID:
            self.difficulty = "hard"
        self.number_of_bricks = self.num_of_br[self.difficulty]
        self.statusBar().showMessage(f'Cложность: {self.difficulty}')

    def dialog(self):
        """Сам диалог с пользователем о выборе картинки,
         возвращает путь до картинки"""
        return QFileDialog.getOpenFileName(self, 'Выбрать картинку',
                                           'Примеры',
                                           'Изображение '
                                           '(*.jpg *.png *.gif *.tif *.tiff'
                                           ' *.bmp *.jpeg *.dib *.raw *.svg)')[0]

    # def do_draw(self):
    #     self.is_drawing = True
    #     for i in range(SIZE * 2):
    #         self._i = i
    #         self.repaint()
    #     self.is_drawing = False
    #
    # def paintEvent(self, event):
    #     if self.is_drawing:
    #         qp = QPainter()
    #         qp.begin(self)
    #         self.modeChangeAnimation(qp, SIZE, SIZE, self._i, self._i)
    #         qp.end()
    #
    # def modeChangeAnimation(self, qp, x, y, w, h):
    #     color = QColor('#121212')
    #     qp.setPen(QPen(color, -1))
    #     qp.setBrush(color)
    #     qp.drawEllipse(x, y, w, h)


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
