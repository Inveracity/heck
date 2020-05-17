import argparse

from game.scan import scan

parser = argparse.ArgumentParser(description="Heck the plenet")
subparsers = parser.add_subparsers(dest="cmd")

# --------- Scan Args ---------
scan_p = subparsers.add_parser('scan', help="blabla")

scan_p.add_argument(
    "--live",
    dest='live',
    default=False,
    help="output events as they occur",
    action="store_true"
)

args = parser.parse_args()

if args.cmd == "scan":
    scan(args.live)
