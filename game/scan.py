import asyncio
import time

from sys import exit

from game.database import get_targets
from game.database import connect_hack as connect
from game.utils import clear_console
from game.utils import current_time

from rethinkdb import r

from tabulate import tabulate
from termcolor import colored
from termcolor import cprint

from datetime import datetime


async def close():
    exit()


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

    if live:
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(print_target(changefeed()))
        except KeyboardInterrupt:
            loop.run_until_complete(close())

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
        port_state = ports.get(port, {}).get('state')
        color = "red"

        if port_state == "open":
            color = "green"

        target_ports.append([port, colored(port_state, color), ports.get(port, {}).get('info', '')])

    if target.get('states', {}).get('hacked'):
        state = colored("(hacked)", "yellow")

    if not target.get('states', {}).get("online"):
        state = colored("(offline)", "red")

    cprint(f"{current_time()}{'-' * 50}", "cyan")

    print(f"{target['id']} {state}")

    if target.get('states', {}).get("online"):
        headers = ["port", "status", "info"]
        print(tabulate(target_ports, headers, tablefmt="plain"))
        print()
