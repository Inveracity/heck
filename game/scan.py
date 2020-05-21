import asyncio
import time

from game.database import get_targets
from game.database import connect_hack as connect
from game.utils import clear_console

from rethinkdb import r

from tabulate import tabulate
from termcolor import colored
from termcolor import cprint


from datetime import datetime

def current_time() -> str:
    """ return current time of day """
    now = datetime.now()

    clock = now.strftime("%H:%M:%S")
    return clock

async def close():
    exit()

# When compiling to an executable this unfortunately doesn't work due to a bug in the rethinkdb library
async def changefeed():
    """ Continuously receive updates as they occur """
    r.set_loop_type('asyncio')

    conn    = await connect()
    targets = r.table('targets')
    cursor  = await targets.changes(include_initial=True).run(conn)

    async for target in cursor:
        new = target.get("new_val", {})
        print_target(new)


def scan(live: bool) -> None:
    """ Output stuff live """

    # if live:
    #     loop = asyncio.get_event_loop()
    #     try:
    #         loop.run_until_complete(changefeed())
    #     except KeyboardInterrupt:
    #         loop.run_until_complete(close())

    if live:
        while True:
            try:
                clear_console()
                targets = get_targets()

                for target in targets:
                    print_target(target)
                time.sleep(2)
            except KeyboardInterrupt:
                exit()

    else:
        targets = get_targets()

        for target in targets:
            print_target(target)


def print_target(target: dict):
    ports = target['ports']
    port_state = ""
    state = ""

    target_ports = []

    for port in ports:
        port_state = ports[port]['state']

        if port_state == "open":
            color = "green"
        else:
            color = "red"

        target_ports.append([port, colored(port_state, color), ports[port]['info']])



    if target['states']['hacked']:
        state = colored("(hacked)", "yellow")

    if not target["states"]["online"]:
        state = colored("(offline)", "red")

    clock = current_time()
    lines = "-" * 50
    cprint(f"{clock}{lines}", "cyan")
    print(f"{target['id']} {state}")

    if target["states"]["online"]:
        headers = ["port", "status", "info"]
        print(tabulate(target_ports, headers, tablefmt="plain"))
        print()
