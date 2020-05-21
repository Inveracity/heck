from game.database import state_change
from game.utils import host_check
from game.password import encrypt
from termcolor import cprint


def killswitch(target: str, port: str, killswitch: str = "") -> str:
    tgt = host_check(target, port)

    if tgt['type'] != "sentinel":
        cprint("Unexpected response from target", "red")
        return ''

    if killswitch == tgt.get('killswitch', False):
        cprint("Sentinel is offline", "green")
        state_change(target, "online", 0)

    else:
        # This outputs a base64 encoded and XOR encrypted killswitch code.
        # The key should be found on another server that needs to be cracked.
        cprint(encrypt(tgt['killswitch'], tgt['key']), "yellow")
