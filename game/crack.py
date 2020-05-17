import argparse
from termcolor import cprint
from game.database import state_change
from game.database import port_state_change
from game.utils import dot_animation
from game.utils import host_check
from game.guess import password


def crack(target, port):
    if dot_animation():
        exit()

    tgt    = host_check(target, port)
    hacked = tgt["hacked"]
    vuln   = tgt["vuln"]

    if hacked:
        cprint("target already cracked", "green")
        return

    if not vuln or "crack" not in vuln:
        port_state_change(target, port, "closed")
        cprint("cracking attempt detected", "yellow")
        return

    if password(target):
        cprint("Access Granted", "green")
        state_change(target, "hacked", 1)
        return

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    parser.add_argument("port")
    args = parser.parse_args()

    crack(args.target, args.port)
