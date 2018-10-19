import sys

def init():
    global VERBOSE, DEBUG_PRODIGES, TOLERANCE_COLOR, BASE_HP
    global COLOR_RED, COLOR_BLUE, COLOR_BLACK

    VERBOSE = False
    DEBUG_PRODIGES = []
    TOLERANCE_COLOR = 0.05
    BASE_HP = 10

    if sys.platform == 'linux2':
        COLOR_RED = '\033[31m'
        COLOR_BLUE = '\033[32m'
        COLOR_BLACK = '\033[0m'
    else:
        COLOR_RED = ''
        COLOR_BLUE = ''
        COLOR_BLACK = ''
