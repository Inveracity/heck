from sys import exit
from typing import NoReturn

from termcolor import cprint

from game.database import port_state_change
from game.database import state_change
from game.database import target_details
from game.utils import dot_animation
from game.utils import host_check


def _ddos(target: dict, port: int) -> NoReturn:
    tgt  = host_check(target, port)
    vuln = tgt["vuln"]
    sentinel_target = tgt.get("sentinel")

    if not vuln or 'ddos' not in vuln:
        cprint("Target not vulnerable to DDoS attacks", "yellow")
        exit()

    if sentinel_target:
        sentinel = target_details(sentinel_target)
        sentinel_online = sentinel.get("online", {})
        if sentinel_online:
            cprint("DDoS attempt detected by sentinel", "red")
            port_state_change(target, port, "closed")
            exit()

    cprint("DDoS in progress", "cyan")
    state_change(target, "online", 0)
    state_change(target, "hacked", 1)


def _ddos_end(target: dict) -> NoReturn:
    state_change(target, "online", 1)


def ddos(target: dict, port: int) -> NoReturn:
    _ddos(target, port)

    while True:
        if dot_animation():
            break

    _ddos_end(target)
