from sys import exit
from typing import NoReturn

from rethinkdb import r

DATABASE = 'hack'


def connect() -> r.connection_type:
    ''' connect to instance without database '''
    return r.connect(host="10.0.0.2", password="johnny5")


def connect_hack() -> r.connection_type:
    ''' connect to instance with hardcoded database '''
    return r.connect(host="10.0.0.2", password="johnny5", db=DATABASE)


def get_targets() -> dict:
    ''' return all target information '''
    conn = connect_hack()
    targets = r.table('targets').run(conn)

    return targets


def target_details(target: str, port: int = 0) -> dict:
    ''' return significant target details '''
    conn = connect_hack()
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


def state_change(target: str, key: str, value: int) -> dict:
    ''' change target state '''
    conn = connect_hack()
    r.table('targets').get(target).update({"states": {key: value}}).run(conn)


def port_state_change(target: str, port: int, value: str) -> NoReturn:
    ''' change the state of target port '''
    if value == "open" or value == "closed":
        conn = connect_hack()
        r.table('targets').get(target).update({"ports": {port: {"state": value}}}).run(conn)

    else:
        raise Exception("Unexpected value for port state change")
        exit(1)
