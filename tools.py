import os
import sqlite3
from PyQt5 import QtGui

SIZE = 900

START_GAME_BTN_ID = 1
SETTINGS_BTN_ID = 2
HELP_BTN_ID = 3
GO_TO_MAIN_MENU_BTN_ID = 4
EASY_BTN_ID = 5
NORMAL_BTN_ID = 6
HARD_BTN_ID = 7
tips_BTN_ID = 8
LEADER_BOARD_BTN_ID = 9
VERSION = 'V 1.0 By Igorase & Mihendy'

COOL_FONT = QtGui.QFont("Clickuper", SIZE // 250 + SIZE // 50, QtGui.QFont.Bold, False)


def win_check(matrix):
    """Для победы все кирпичики должны стоять на своём месте, этот факт тут проверяется"""
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if (i, j) != matrix[i][j]:
                return False
    return True


def show(widgets):
    for widget in widgets:
        try:
            widget.show()
            widget.setEnabled(True)
        except AttributeError:
            if isinstance(widget, list):
                show(widget)


def clear(widgets):
    for widget in widgets:
        try:
            widget.hide()
        except AttributeError:
            if isinstance(widget, list):
                clear(widget)


def make_game_files(obj, directory_name='data'):
    try:
        os.mkdir(directory_name)
    except FileExistsError:
        pass
    finally:
        obj.con = sqlite3.connect(f"{directory_name}/leaderboard.db")
        cur = obj.con.cursor()
        try:
            cur.execute('''CREATE TABLE leaders (
                    id         INTEGER PRIMARY KEY ASC AUTOINCREMENT
                               NOT NULL,
                    name       STRING,
                    difficulty STRING  NOT NULL,
                    time               NOT NULL);''')
            obj.con.commit()
        except sqlite3.OperationalError:
            pass
        except sqlite3.DatabaseError:
            pass
    obj.cur = obj.con.cursor()
