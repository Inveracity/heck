import time
import random
import sys
from termcolor import cprint
from termcolor import colored

GAME_SPEED = 10  # larger number = slower game speed


def dot_animation():
    try:
        for x in range(random.randint(1*2, GAME_SPEED*2)):
            dot = colored('.', 'cyan')
            sys.stdout.write(dot)
            sys.stdout.flush()
            time.sleep(0.1)

        print("")
        return False

    except KeyboardInterrupt:
        print("")
        cprint("interrupted", "yellow")
        return True
