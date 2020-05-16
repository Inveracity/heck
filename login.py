import argparse
import traceback

from game.database import state_change
from game.database import target_details
from game.utils import game_wait

parser = argparse.ArgumentParser()
parser.add_argument('target')
args = parser.parse_args()


def login(target):
    tgt = target_details(target)

    online  = tgt["online"]
    hacked  = tgt["hacked"]
    blocked = tgt["blocked"]

    if not online:
        print("ERROR: unreachable")
        exit()

    if blocked:
        print("WARNING: Blocked from accessing server")
        exit()

    if not hacked:
        print("INFO: unrecognised access credentials")
        exit()

    return tgt

def ls(t, args):
    folders = t['files']

    for f in folders:
        folder = list(f.keys())[0]
        files = f[folder]
        for file in files:
            print(f"  /{folder}/{file['name']}")

def cat(t: dict, args: list):
    folders = t['files']

    if len(args) == 1:
        a = args[0].split("/")[1:][0]
        b = args[0].split("/")[1:][1]
        for f in folders:
            files = f.get(a, None)
            if files:
                for file in files:
                    if file['name'] == b:
                        print(f"  file['content']")


def whoami(t, args):
    print(f"admin@{t['hostname']}.local")


def quit(t, args):
    exit()


def shutdown(t, args):
    print(f' Shutdown initiated by admin')
    state_change(target, "online", 0)
    print("lost connection to host")
    exit()

switch = {
    'ls'      : ls,
    'whoami'  : whoami,
    'quit'    : quit,
    'shutdown': shutdown,
    'cat'     : cat,
}

print("INFO: connecting")
game_wait()

while True:
    try:
        tgt = login(args.target)
        userinput = input(f"{args.target}: ")

        if userinput == 'help':
            print(', '.join(switch.keys()))

        else:
            try:
                userargs = userinput.split()
                switch[userargs[0]](tgt, userargs[1:])

            except Exception as e:
                print(traceback.format_exc(e))
                print("invalid command")

    except KeyboardInterrupt:
        exit()

    except Exception as e:
        print(traceback.format_exc(e))
        print()

