import argparse
from sys import exit
from game.init import init
from game.scan import scan
from game.crack import crack
from game.ddos import ddos
from game.login import login
from game.killswitch import killswitch
from game.password import decrypt
from game.mission import level_one
from game.version import version

parser = argparse.ArgumentParser(description="Heck the plenet")

parser.add_argument(
    "--version",
    dest="show_version",
    default=False,
    help="show version",
    action="store_true"
)

subparsers = parser.add_subparsers(dest="cmd")

# --------- Init Args ---------
init_p = subparsers.add_parser('init', help="init ip or host and password to generate a config and insert game objects into database")
init_p.add_argument("host")
init_p.add_argument("password")

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

# --------- Killswitch Args ---------
killswitch_p = subparsers.add_parser('killswitch', help="Killswitch will turn off off a sentinel when provided with the correct key")
killswitch_p.add_argument('target')
killswitch_p.add_argument('port')
killswitch_p.add_argument(
    "--killswitch",
    metavar='KEY',
    dest='killswitch',
    type=str,
    default="",
    help="send a killswitch key to a sentinel to take it offline",
    action="store"
)

# --------- Decrypt Args ---------
decrypt_p = subparsers.add_parser('decrypt', help="decrypt a secret using a key")
decrypt_p.add_argument(
    "--cipher",
    metavar='CIPHER',
    dest='cipher',
    type=str,
    default="",
    help="insert the encrypted value",
    action="store"
)
decrypt_p.add_argument(
    "--key",
    metavar='KEY',
    dest='key',
    type=str,
    default="",
    help="insert decryption key",
    action="store"
)

# --------- Mission Args ---------
mission_p = subparsers.add_parser('mission', help="Get mission briefing or check mission status")
mission_p.add_argument(
    "--status",
    dest='status',
    default=False,
    help="check if mission was successful",
    action="store_true"
)

if __name__ == "__main__":
    args = parser.parse_args()
    print()

    if args.show_version:
        print(version)
        exit()

    if args.cmd == "init":
        init(args.host, args.password)

    if args.cmd == "scan":
        scan(args.live)

    if args.cmd == "crack":
        crack(args.target, args.port)

    if args.cmd == "ddos":
        ddos(args.target, args.port)

    if args.cmd == "login":
        login(args.target, args.port)

    if args.cmd == "killswitch":
        killswitch(args.target, args.port, args.killswitch)

    if args.cmd == "decrypt":
        decrypt(args.cipher, args.key)

    if args.cmd == "mission":
        level_one(args.status)

    if not args.cmd:
        parser.print_help()
