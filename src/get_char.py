## 
# @file getchar.py
# @author Jack Duignan (JackpDuignan@gmail.com)
# @date 2024-06-28
# @brief This file contains the definitions for a getchar like function implemented in python
# 
# @see https://stackoverflow.com/questions/48820375/is-there-a-built-in-function-in-python-3-like-getchar-in-c

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()
    
getch = _Getch()

def getchar() -> str:
    """
    Get a single character from the stdin without echo
    """
    return getch()

if __name__ == "__main__":
    while (1):
        char = getchar()

        if (char == "\r"):
            print("\nreturn")
        elif (char == "\n"):
            print("\nnewline")
        elif (char == "\x03"):
            print("\ncontrol c")
        else:
            print(char.encode("UTF-8"), end="")
