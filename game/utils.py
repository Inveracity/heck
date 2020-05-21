import time
import sys

from datetime import datetime
from os import system
from os import name

from termcolor import cprint
from termcolor import colored

from game.database import target_details

GAME_SPEED = 10  # larger number = slower game speed


def dot_animation() -> bool:
    """ give player a feeling of stuff happening """

    try:
        for x in range(GAME_SPEED):
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

    online     = tgt.get("online")
    port_state = tgt.get("port_state")
    ports      = tgt.get("ports")

    if not online:
        cprint("target network unreachable", "red")
        sys.exit()

    if port not in ports:
        cprint("port or service unavailable", "yellow")
        sys.exit()

    if port_state == "closed":
        cprint("target port blocked", "red")
        sys.exit()

    return tgt


def clear_console():

    if name == 'nt':
        system('cls')

    else:
        system('clear')


def current_time() -> str:
    """ return current time of day """
    now = datetime.now()

    clock = now.strftime("%H:%M:%S")
    return clock

