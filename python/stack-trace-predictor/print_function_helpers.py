from __future__ import print_function
import sys


__DEBUG_MODE__ = False


def setDebugMode(debug_mode: bool):
    global __DEBUG_MODE__
    __DEBUG_MODE__ = debug_mode


def getDebugMode() -> bool:
    return __DEBUG_MODE__


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def dprint(*args, **kwargs):
    if __DEBUG_MODE__:
        print(*args, file=sys.stdout, **kwargs)
