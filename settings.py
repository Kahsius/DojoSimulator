import sys

def init(argv):
    global VERBOSE, DEBUG_PRODIGES, TOLERANCE_COLOR, BASE_HP, N_TEST
    global P_COUNTER_OPP_MASTERY
    global COLOR_RED, COLOR_BLUE, COLOR_BLACK

    DEBUG_PRODIGES = ['Faine']
    TOLERANCE_COLOR = 0.05
    BASE_HP = 12
    P_COUNTER_OPP_MASTERY = .3

    if sys.platform == 'linux2':
        COLOR_RED = '\033[31m'
        COLOR_BLUE = '\033[32m'
        COLOR_BLACK = '\033[0m'
    else:
        COLOR_RED = ''
        COLOR_BLUE = ''
        COLOR_BLACK = ''

    # Options
    N_TEST = 10000
    VERBOSE = False

    for i in range(len(argv)):
        s = argv[i]
        if s == '-v':
            VERBOSE = True
        elif s == '-n':
            N_TEST = int(argv[i+1])
