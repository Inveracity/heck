import time
import random
import sys
import argparse

from game.database import target_details
from game.database import state_change
from game.utils import dot_animation
from termcolor import cprint

parser = argparse.ArgumentParser()
parser.add_argument('target')
parser.add_argument('port')
args = parser.parse_args()

def ddos(target: dict, port: int):
    cprint("sending overload packets", "cyan")

    tgt = target_details(target, port)

    online  = tgt["online"]
    blocked = tgt["blocked"]
    vuln    = tgt["vuln"]

    if not online:
        cprint("target unreachable", "red")
        exit()

    if blocked:
        cprint("connection blocked by target", "red")
        exit()

    if not vuln or 'ddos' not in vuln:
        cprint("DDoS attempted detected", "red")
        state_change(target, "blocked", 1)
        return

    cprint("DDoS in progress", "cyan")
    state_change(target, "online", 0)

def ddos_end(target):
    state_change(target, "online", 1)


ddos(args.target, args.port)

while True:
    if dot_animation():
        break

ddos_end(args.target)
