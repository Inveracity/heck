import argparse

from game.init import init
from game.scan import scan
from game.crack import crack
from game.ddos import ddos
from game.login import login

parser = argparse.ArgumentParser(description="Heck the plenet")
subparsers = parser.add_subparsers(dest="cmd")

# --------- Init Args ---------
init_p = subparsers.add_parser('init', help="Insert game objects into database and/or reset the game")


# --------- Scan Args ---------
scan_p = subparsers.add_parser('scan', help="Scan for targets")

scan_p.add_argument(
    "--live",
    dest='live',
    default=False,
    help="output events as they occur",
    action="store_true"
)

# --------- Crack Args ---------
crack_p = subparsers.add_parser('crack', help="Attempt to get access credentials for a target")
crack_p.add_argument("target")
crack_p.add_argument("port")

# --------- DDoS Args ---------
ddos_p = subparsers.add_parser('ddos', help="Overload a target to bring it offline temporarily")
ddos_p.add_argument('target')
ddos_p.add_argument('port')

# --------- Login Args ---------
login_p = subparsers.add_parser('login', help="If the target has been hacked, connect to the target shell")
login_p.add_argument('target')
login_p.add_argument('port')


if __name__ == "__main__":
    args = parser.parse_args()

    if args.cmd == "init":
        init()

    if args.cmd == "scan":
        scan(args.live)

    if args.cmd == "crack":
        crack(args.target, args.port)

    if args.cmd == "ddos":
        ddos(args.target, args.port)

    if args.cmd == "login":
        login(args.target, args.port)

    if not args.cmd:
        parser.print_help()
