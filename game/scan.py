import argparse
from game.database import get_targets
from game.database import get_targets_live
from tabulate import tabulate
from termcolor import colored
from termcolor import cprint

def scan(live: bool):

    if live:
        try:
            targets = get_targets_live()
        except KeyboardInterrupt:
            exit()
    else:
        targets = get_targets()

    output = ''
    for target in targets:
        if live:
            target = target.get('new_val')
        ports = target['ports']

        target_ports = []

        for port in ports:
            port_state = ports[port]['state']

            if port_state == "open":
                color = "green"
            else:
                color = "red"

            target_ports.append([port, colored(port_state, color), ports[port]['info']])

        if target['states']['online']:
            cprint("-"*50, "cyan")
            cprint(target['id'], "cyan")
            headers = ["port", "status", "info"]
            print(tabulate(target_ports, headers, tablefmt="plain"))
            print()
