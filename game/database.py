from rethinkdb import r

DATABASE = 'hack'


def connect() -> r.connection_type:
    ''' connect to instance without database '''
    return r.connect(host="10.0.0.2", password="johnny5")


def _connect_hack() -> r.connection_type:
    ''' connect to instance with hardcoded database '''
    return r.connect(host="10.0.0.2", password="johnny5", db=DATABASE)


def get_targets() -> dict:
    ''' return all target information '''
    conn = _connect_hack()
    targets = r.table('targets').run(conn)

    return targets


def get_targets_live():
    conn = _connect_hack()
    return r.table('targets').changes(include_initial=True).run(conn)


def target_details(target: str, port: int = 0) -> dict:
    ''' return significant target details '''
    conn = _connect_hack()
    tgt  = r.table('targets').get(target).run(conn)

    meta               = {}
    meta["hostname"]   = tgt.get('id')
    meta["password"]   = tgt.get('password', '')
    meta["online"]     = tgt.get('states', {})['online']
    meta["hacked"]     = tgt.get('states', {})['hacked']
    meta["files"]      = tgt.get('files', {})
    meta["ports"]      = tgt.get('ports')
    meta["vuln"]       = meta['ports'].get(port, {}).get('vuln', 0)
    meta["port_state"] = meta['ports'].get(port, {}).get('state', 'closed')

    return meta


def state_change(target: str, key: str, value: int) -> dict:
    ''' change target state '''
    conn = _connect_hack()
    r.table('targets').get(target).update({"states": {key: value}}).run(conn)


def port_state_change(target: str, port: int, value: str):
    ''' change the state of target port '''
    if value == "open" or value == "closed":
        conn = _connect_hack()
        r.table('targets').get(target).update({"ports": {port: {"state": value}}}).run(conn)

    else:
        raise Exception("Unexpected value for port state change")
        exit(1)
