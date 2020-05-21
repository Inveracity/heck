from typing import NoReturn
from sys import exit
from termcolor import cprint

from game.database import state_change
from game.database import port_state_change

from game.utils import dot_animation
from game.utils import host_check
from game.password import password


def crack(target: str, port: str) -> NoReturn:
    if dot_animation():
        exit()

    tgt    = host_check(target, port)
    hacked = tgt["hacked"]
    vuln   = tgt["vuln"]

    if hacked:
        cprint("Shell is ready, use login to connect", "green")
        return

    if not vuln or "crack" not in vuln:
        port_state_change(target, port, "closed")
        cprint("cracking attempt detected", "yellow")
        return

    if password(target):
        cprint("Access Granted", "green")
        cprint("Injecting reverse shell", "cyan")

        if dot_animation():
            exit()

        cprint("Injection complete", "green")

        state_change(target, "hacked", 1)

        return

    return
