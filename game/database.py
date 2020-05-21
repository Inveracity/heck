from sys import exit
from typing import NoReturn

from rethinkdb import r
from rethinkdb.errors import ReqlAuthError

from game.config import read_config

DATABASE = 'hack'
TABLES = ['targets']


def connect(db: str = None) -> r.connection_type:
    ''' connect to instance with hardcoded database '''
    server = read_config()
    conn = None

    try:
        conn = r.connect(host=server['host'], password=server['password'], db=db)
    except ReqlAuthError:
        print("Error: Wrong password. If you are using docker-compose, check the password there!")
        exit(1)

    return conn


def get_targets() -> dict:
    ''' return all target information '''
    conn = connect(DATABASE)
    targets = r.table('targets').run(conn)

    return targets


def target_details(target: str, port: int = 0) -> dict:
    ''' return significant target details '''
    conn = connect(DATABASE)
    tgt  = r.table('targets').get(target).run(conn)

    meta               = {}
    meta["hostname"]   = tgt.get('id')
    meta["type"]       = tgt.get('type')
    meta["password"]   = tgt.get('password', '')
    meta["online"]     = tgt.get('states', {}).get('online', {})
    meta["hacked"]     = tgt.get('states', {}).get('hacked', {})
    meta["files"]      = tgt.get('files', {})
    meta["ports"]      = tgt.get('ports')
    meta["vuln"]       = meta['ports'].get(port, {}).get('vuln', 0)
    meta["port_state"] = meta['ports'].get(port, {}).get('state', 'closed')
    meta["key"]        = tgt.get('key', '')
    meta["killswitch"] = tgt.get('killswitch', '')
    meta["sentinel"]   = tgt.get('sentinel', {})

    return meta


def state_change(target: str, key: str, value: int) -> dict:
    ''' change target state '''
    conn = connect(DATABASE)
    r.table('targets').get(target).update({"states": {key: value}}).run(conn)


def port_state_change(target: str, port: int, value: str) -> NoReturn:
    ''' change the state of target port '''
    if value == "open" or value == "closed":
        conn = connect(DATABASE)
        r.table('targets').get(target).update({"ports": {port: {"state": value}}}).run(conn)

    else:
        raise Exception("Unexpected value for port state change")
        exit(1)
