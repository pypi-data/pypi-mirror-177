import os
import sys
import datetime
import pathlib
import ctypes

from sty import bg, fg, rs
from playsound import playsound
import cursor

if sys.platform == "win32":
    os.system("color")

LF_FACESIZE = 32
STD_OUTPUT_HANDLE = -11


class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    def __init__(self, x, y):
        self.X = x
        self.Y = y


class CONSOLE_FONT_INFOEX(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_ulong),
        ("nFont", ctypes.c_ulong),
        ("dwFontSize", COORD),
        ("FontFamily", ctypes.c_uint),
        ("FontWeight", ctypes.c_uint),
        ("FaceName", ctypes.c_wchar * LF_FACESIZE),
    ]


def exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            timestamp = datetime.datetime.now().isoformat()
            f = open("log.txt", "a")
            f.write(timestamp)
            f.write(f" {func.__name__} {e}\n")
            f.close()

    return inner_function


class ConsoleMaster:

    title = ""
    font_size = ""
    window_width = ""
    window_height = ""

    def __init__(
        self, title="New Window", font_size=17, window_width=30, window_height=25
    ):
        self.change_windows_title(title)
        self.change_pixel_size(font_size)
        self.change_windows_size(window_width, window_height)
        self.hide_cursor()

    @exception_handler
    def pause(self):
        input()

    @exception_handler
    def print_with_color(self, rgb_background, rgb_foreground, element_to_print):
        print(
            fg(rgb_foreground[0], rgb_foreground[1], rgb_foreground[2])
            + bg(rgb_background[0], rgb_background[1], rgb_background[2])
            + element_to_print
            + rs.all,
            end="",
            flush=True,
        )

    @exception_handler
    def go_xy(self, x, y):
        INIT_POS = COORD(x, y)
        STD_OUTPUT_HANDLE = -11
        hOut = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        ctypes.windll.kernel32.SetConsoleCursorPosition(hOut, INIT_POS)

    @exception_handler
    def change_pixel_size(self, size):
        font = CONSOLE_FONT_INFOEX()
        font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
        # font.nFont = 12
        font.dwFontSize.X = size
        font.dwFontSize.Y = size
        # font.FontFamily = 54
        # font.FontWeight = 400
        # font.FaceName = "Lucida Console"

        handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        ctypes.windll.kernel32.SetCurrentConsoleFontEx(
            handle, ctypes.c_long(False), ctypes.pointer(font)
        )
        self.font_size = size

    @exception_handler
    def change_windows_size(self, width, height):
        cmd = "mode " + str(width) + "," + str(height)
        os.system(cmd)
        self.window_width = width
        self.window_height = height

    @exception_handler
    def show_cursor(self):
        cursor.show()

    @exception_handler
    def hide_cursor(self):
        cursor.hide()

    @exception_handler
    def change_windows_title(self, title):
        os.system("title " + str(title))
        self.title = title
