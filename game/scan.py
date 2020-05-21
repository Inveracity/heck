# import asyncio
import time

from typing import NoReturn

from sys import exit

from game.database import get_targets
from game.database import connect
from game.utils import clear_console
from game.utils import current_time

from rethinkdb import r

from tabulate import tabulate
from termcolor import colored
from termcolor import cprint


async def close() -> NoReturn:
    exit()


async def changefeed() -> NoReturn:
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

    # compiling to a binary for some reason breaks this with

    # bin\dist\heck.exe scan --live

    # Traceback (most recent call last):
    #   File "heck.py", line 112, in <module>
    #     scan(args.live)
    #   File "game\scan.py", line 41, in scan
    #     loop.run_until_complete(changefeed())
    #   File "asyncio\base_events.py", line 616, in run_until_complete
    #   File "game\scan.py", line 26, in changefeed
    #     conn    = await connect()
    #   File "game\database.py", line 20, in connect
    #     r.set_loop_type('asyncio')
    #   File "site-packages\rethinkdb\__init__.py", line 69, in set_loop_type
    #   File "site-packages\pkg_resources\__init__.py", line 1134, in resource_exists
    #   File "site-packages\pkg_resources\__init__.py", line 1404, in has_resource
    #   File "site-packages\pkg_resources\__init__.py", line 1472, in _has
    # NotImplementedError: Can't perform this operation for unregistered loader type

    # if live:
    #     loop = asyncio.get_event_loop()
    #     try:
    #         loop.run_until_complete(changefeed())
    #     except KeyboardInterrupt:
    #         loop.run_until_complete(close())

    # Instead do this, which is kinda sad
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


def print_target(target: dict) -> NoReturn:
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
