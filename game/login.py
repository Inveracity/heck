from os import linesep
from sys import exit
from typing import Any
from typing import NoReturn

from termcolor import cprint

from game.database import state_change
from game.utils import dot_animation
from game.utils import host_check


def ls(t: dict, _: Any) -> NoReturn:
    ''' list full folder and file paths '''

    folders = t.get('files', None)
    if folders:
        for f in folders:
            folder = list(f.keys())[0]
            files = f[folder]
            for file in files:
                cprint(f"  /{folder}/{file['name']}", "cyan")


def cat(t: dict, args: list) -> NoReturn:
    ''' a valid arg is a path to a file like: ['/data/secret.dat'] '''

    folders = t['files']

    # TODO: this is still awful
    if len(args) == 1:
        paths = args[0].split("/")[1:]
        if paths:
            for f in folders:
                files = f.get(paths[0], None)
                if files:
                    for file in files:
                        if file['name'] == paths[1]:
                            cprint(f"{file['content']}", "cyan")
                            return

    cprint("no such file or directory", "yellow")


def whoami(t: dict, _: Any) -> NoReturn:
    cprint(f"admin@{t['hostname']}.local", "cyan")


def quit(t: dict, _: Any) -> NoReturn:
    cprint("disconnected", "yellow")
    exit()


def shutdown(t: dict, _: Any) -> NoReturn:
    cprint('Shutdown initiated by admin', "yellow")
    state_change(t['hostname'], "online", 0)
    cprint("lost connection to host", "red")
    exit()


def show_cmds(t: dict, _: Any) -> NoReturn:
    cmds = linesep.join(switch.keys())
    cprint(cmds, "cyan")


def login(target: dict, port: int) -> NoReturn:
    tgt    = host_check(target, port)
    hacked = tgt["hacked"]

    if not hacked:
        cprint("No shell available", "yellow")
        exit()

    dot_animation()

    while True:
        try:

            userinput = input(f"{tgt['hostname']}> ")
            userargs = userinput.split()

            if userinput == '':
                cprint("for a list of commands type: help", "yellow")
                continue

            elif userargs[0] in switch.keys():
                switch[userargs[0]](tgt, userargs[1:])

            else:
                cprint("Unrecognised command", "yellow")

        except KeyboardInterrupt:
            exit()


switch = {
    'ls': ls,
    'whoami': whoami,
    'quit': quit,
    'shutdown': shutdown,
    'cat': cat,
    'help': show_cmds,
}
