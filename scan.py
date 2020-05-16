from game.database import get_targets
from tabulate import tabulate
from termcolor import colored
from termcolor import cprint
targets = get_targets()

output = ''
for target in targets:
    ports = target['ports']

    target_ports = []

    for port in ports:

        target_ports.append([port, colored("open", "green"), ports[port]['info']])

    if target['states']['online']:
        cprint("-"*50, "cyan")
        cprint(target['id'], "cyan")
        headers = ["port", "status", "info"]
        print(tabulate(target_ports, headers, tablefmt="plain"))
        print()

    if target['states']['']

