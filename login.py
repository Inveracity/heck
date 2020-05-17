import argparse
import traceback
from termcolor import cprint

from game.database import state_change
from game.utils import dot_animation
from game.utils import host_check


def ls(t: dict, _):
    folders = t['files']

    for f in folders:
        folder = list(f.keys())[0]
        files = f[folder]
        for file in files:
            cprint(f"  /{folder}/{file['name']}", "cyan")


def cat(t: dict, args: list):
    folders = t['files']

    # TODO: this is awful
    if len(args) == 1:
        a = args[0].split("/")[1:][0]
        b = args[0].split("/")[1:][1]
        for f in folders:
            files = f.get(a, None)
            if files:
                for file in files:
                    if file['name'] == b:
                        cprint(f"{file['content']}", "cyan")


def whoami(t: dict, _):
    cprint(f"admin@{t['hostname']}.local")


def quit(t, _):
    exit()


def shutdown(t: dict, _):
    cprint('Shutdown initiated by admin', "yellow")
    state_change(t['hostname'], "online", 0)
    cprint("lost connection to host", "red")
    exit()


switch = {
    'ls': ls,
    'whoami': whoami,
    'quit': quit,
    'shutdown': shutdown,
    'cat': cat,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('target')
    parser.add_argument('port')
    args = parser.parse_args()

    tgt    = host_check(args.target, args.port)
    hacked = tgt["hacked"]

    if not hacked:
        cprint("Unrecognised access credentials", "yellow")
        exit()

    dot_animation()

    # TODO: all of this is also pretty awful
    while True:
        try:
            userinput = input(f"{args.target}: ")

            if userinput == 'help':
                cprint(', '.join(switch.keys()), "cyan")

            else:
                try:
                    userargs = userinput.split()
                    switch[userargs[0]](tgt, userargs[1:])

                except Exception as e:
                    cprint(traceback.format_exc(e), "red")
                    cprint("invalid command", "yellow")

        except KeyboardInterrupt:
            exit()

        except Exception as e:
            cprint(traceback.format_exc(e), "red")
            print()
