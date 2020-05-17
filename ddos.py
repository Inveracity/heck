import argparse

from game.database import state_change
from game.database import port_state_change
from game.utils import dot_animation
from game.utils import host_check
from termcolor import cprint


def ddos(target: dict, port: int):
    tgt  = host_check(target, port)
    vuln = tgt["vuln"]

    if not vuln or 'ddos' not in vuln:
        cprint("DDoS attempted detected", "red")
        port_state_change(target, port, "closed")
        return

    cprint("DDoS in progress", "cyan")
    state_change(target, "online", 0)


def ddos_end(target):
    state_change(target, "online", 1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('target')
    parser.add_argument('port')
    args = parser.parse_args()

    ddos(args.target, args.port)

    while True:
        if dot_animation():
            break

    ddos_end(args.target)
