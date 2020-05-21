import time
import random
import sys
from os import system, name
from termcolor import cprint
from termcolor import colored

from game.database import target_details

GAME_SPEED = 10  # larger number = slower game speed


def dot_animation() -> bool:
    """ give player a feeling of stuff happening """

    try:
        for x in range(random.randint(1*2, GAME_SPEED*2)):
            dot = colored(".", "cyan")
            sys.stdout.write(dot)
            sys.stdout.flush()
            time.sleep(0.1)

        print("")
        return False

    except KeyboardInterrupt:
        print("")
        cprint("interrupted", "yellow")
        return True


def host_check(target: str, port: int) -> dict:
    tgt = target_details(target, port)

    online     = tgt["online"]
    port_state = tgt["port_state"]
    ports      = tgt["ports"]

    if not online:
        cprint("target network unreachable", "red")
        exit()

    if port not in ports:
        cprint("port or service unavailable", "yellow")
        exit()

    if port_state == "closed":
        cprint("target port blocked", "red")
        exit()

    return tgt


def clear_console():

    if name == 'nt':
        system('cls')

    else:
        system('clear')
