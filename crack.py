import argparse
from termcolor import cprint

from game.database import target_details
from game.database import state_change
from game.utils import game_wait
from game.guess import password

parser = argparse.ArgumentParser()
parser.add_argument("target")
parser.add_argument("port")
args = parser.parse_args()

def crack(target, port):
    if dot_animation():
        exit()

    tgt     = target_details(target, port)
    online  = tgt["online"]
    hacked  = tgt["hacked"]
    blocked = tgt["blocked"]
    vuln    = tgt["vuln"]
    ports   = tgt["ports"]

    if port not in ports:
        cprint("port or service unavailable", "yellow")
        exit()

    if hacked:
        cprint("target already cracked", "green")
        return

    if blocked:
        cprint("target blocked your attempts at connecting", "yellow")
        return


    if not vuln or "crack" not in vuln:
        state_change(target, "blocked", 1)
        cprint("cracking attempt detected", "yellow")
        return

    if not online:
        cprint("target unreachable", "red")
        return

    if password(target):
        cprint("Access Granted", "green")
        state_change(target, "hacked", 1)
        return

    return

crack(args.target, args.port)
