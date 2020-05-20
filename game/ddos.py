from typing import NoReturn

from game.database import state_change
from game.database import port_state_change
from game.utils import dot_animation
from game.utils import host_check
from termcolor import cprint


def _ddos(target: dict, port: int) -> NoReturn:
    tgt  = host_check(target, port)
    vuln = tgt["vuln"]

    if not vuln or 'ddos' not in vuln:
        cprint("DDoS attempted detected", "red")
        port_state_change(target, port, "closed")
        return

    cprint("DDoS in progress", "cyan")
    state_change(target, "online", 0)


def _ddos_end(target: dict) -> NoReturn:
    state_change(target, "online", 1)


def ddos(target: dict, port: int) -> NoReturn:
    _ddos(target, port)

    while True:
        if dot_animation():
            break

    _ddos_end(target)
