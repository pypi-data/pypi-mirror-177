"""
The Core Part of The Pakage:
    all of Functions and Classes are Defined Heres
"""
import sys
import os
import io

import getch
from . import style

py_stds = [sys.stdout, sys.stdin, sys.stderr]


class StdOut(object):
    """New Standard Output Class"""
    def start_tui(self):
        """Functions That Run if tui_mode == True"""
        self.con.clear()

    def __init__(self, txtctrl, con):
        self.con = con
        self.start_tui()
        self.txtctrl = txtctrl
        self.texts = ''

    def write(self, string):
        """
        Print Text to Terminal
            args:
                string: the String to Output
        """
        self.con.print_to_terminal(style.apply_style(string), end='')
        self.texts += string
        self.flush()

    def read(self, x_pos, y_pos) -> str:
        """
        Read a Character from Terminal
            args:
                x: X Location
                y: Y Location
            output:
                Character in X and Y location
        """
        return self.texts.split('\n')[y_pos][x_pos]

    def add(self, string):
        """
        Add Text to StdOut Class But not Output
            args:
                string: the String to Add
        """
        self.texts += string
        py_stds[0].flush()
        self.flush()

    def flush(self):
        """Refresh The Screen"""
        if len(self.texts.split('\n')) >= os.get_terminal_size().lines:
            self.texts = ""
            self.con.clear()
        py_stds[0].flush()


StdErr = StdOut


class StdIn(object):
    """New Standard Input Class"""
    def __init__(self, txtctrl, con):
        self.con = con
        self.con.clear()
        self.txtctrl = txtctrl
        self.texts = ''

    def readline(self):
        """
        Get a Input Line From User
            output:
                the Input of User
        """
        self.flush()
        return self.con.input_from_terminal()

    def flush(self):
        """Refresh The Screen"""


class Terminal(object):
    """
    The Main Terminal Class
        Help:
            To Set The Input, Error and Output to Defaut:
                Run: "del {Name of Terminal}"
            Note: Don't Use print_to_terminal, error_to_terminal and
            input_from_terminal Functions Directly Instand Use Normal print,
            raise and input Functions
    """
    def __init__(self, tui_mode: bool = False):
        self.tui_mode = tui_mode
        self.cols = os.get_terminal_size().columns
        self.lines = os.get_terminal_size().lines
        if self.tui_mode is False:
            StdOut.flush = lambda self: (py_stds[0].flush())
            StdOut.start_tui = lambda self: (...)
        sys.stdout = StdOut(io.StringIO(""), self)
        print()
        sys.stderr = StdErr(io.StringIO(""), self)
        sys.stdin = StdIn(io.StringIO(""), self)

    def print_to_terminal(self, text: str = "", end: str = ""):
        """
        Sends a String to Main Terminal Output
            Args:
                text[str]: the String To Output
                end[str]="\\n": the String That Adds to Text
        """
        return py_stds[0].write(text + end)

    def input_from_terminal(self, pos: tuple | None = (10, 4),
                            max_char_lenth: int = 10, _style: str = ''):
        """
        Gets a String from Main Terminal Input
            Args:
                pos[tuple(X, Y)]: Location on Terminal
                max_char_lenth[int]: Maximum Character Limit
                _style[str]: Style Names
            Output:
                User Input
        """
        while True:
            _input = ""
            index = 0
            color_and_pos = (f"\x1b7\x1b[{pos[0]};{pos[1]}f" +
                             f"{style.apply_style_noreset(_style)}")
            while True:
                char = ord(getch.getch())
                py_stds[0].flush()
                if 32 <= char <= 126:
                    if len(_input) <= max_char_lenth:
                        _input = (_input[0: index] + chr(char) +
                                  _input[index: len(_input)])
                        index += 1
                elif char == 13:
                    print(color_and_pos, end='')
                    print(' ' * len(_input), end='')
                    print(color_and_pos, end='')
                    py_stds[0].flush()
                    print(f"\x1b[{index}C", end='')
                    py_stds[0].flush()
                    print(color_and_pos + style.other['RESET_ALL'], end='')
                    if _input != '':
                        return _input
                    else:
                        raise KeyboardInterrupt
                elif char == 8:
                    if index != 0:
                        _input = (_input[0: index - 1] + chr(char) +
                                  _input[index: len(_input) - 1])
                        index -= 1
                elif char == 0:
                    next = ord(getch.getch())
                    if next == 77:
                        if index != len(_input):
                            index += 1
                    elif next == 75:
                        if index != 0:
                            index -= 1
                    py_stds[0].flush()
                elif char == 3:
                    print(color_and_pos, end='')
                    print(' ' * len(_input), end='')
                    print(color_and_pos, end='')
                    py_stds[0].flush()
                    print(f"\x1b[{index}C", end='')
                    py_stds[0].flush()
                    print(color_and_pos + style.other['RESET_ALL'], end='')
                    raise KeyboardInterrupt
                else:
                    return _input
                print(color_and_pos, end='')
                print(' ' * len(_input), end='')
                print(color_and_pos, end='')
                print(_style + _input + style.other['RESET_ALL'], end='')
                print(color_and_pos, end='')
                py_stds[0].flush()
                print(f"\x1b[{index}C" + style.other['RESET_ALL'], end='')
                py_stds[0].flush()

    def error_to_terminal(self, text: str = "", end: str = "\n"):
        """
        Sends a String to Main Terminal Error Output
            Args:
                text[str]: the String To Output
                end[str]="\\n": the String That Adds to Text
        """
        print('', end='')
        return py_stds[2].write(text + end)

    def clear(self):
        """Clears The Terminal"""
        sys.stdout.texts = ''
        print('\033[H\033[2J\033[3J\033[H' if self.tui_mode is True else
              '\033[H\033[2J\033[H', end='')

    def remove_line(self):
        """Remove Current Line"""
        print('\033[K', end='')

    def set_title(self, title: str):
        """
        Changes The Terminal Title
            Args:
                title[str]: New Title
        """
        print(f'\x1b]2;{title}\x07', end='')

    def move_to(self, x_pos, y_pos):
        """
        Move Cursor To another Location
            Args:
                x: X Location
                y: Y Location
        """
        print(f"\x1b7\x1b[{x_pos};{y_pos}f", end='')

    def print_at(self, text: str = "", x_pos: str = None,
                 y_pos: str = None):
        """
        Sends a String to Main Terminal Output at a Certain Location
            Args:
                text[str]: the String To Output
                x: X Location
                y: Y Location
        """

        print(text if (x_pos is None and y_pos is None) else
              f"\x1b7\x1b[{x_pos};{y_pos}f{text}\x1b8\r",
              end='')

    def __del__(self):
        sys.stdout = py_stds[0]
        sys.stdin = py_stds[1]
        sys.stderr = py_stds[2]


Terminal.isRunning = False
