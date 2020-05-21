from typing import NoReturn

from rethinkdb import r
from game.database import connect
from game.database import DATABASE
from game.database import TABLES
from game.objects import gameobjects
from game.config import write_config


def init(host: str, password: str) -> NoReturn:
    """ Initialise game with a config and inserting game objects into database """

    write_config({"host": host, "password": password})

    conn = connect(DATABASE)

    print("cleaning up old database")
    if DATABASE in r.db_list().run(conn):
        r.db_drop(DATABASE).run(conn)

    print("creating new database")
    if DATABASE not in r.db_list().run(conn):
        r.db_create(DATABASE).run(conn)

    print("creating tables")
    for table in TABLES:
        if table not in r.db(DATABASE).table_list().run(conn):
            r.db(DATABASE).table_create(table).run(conn)

    db = r.db(DATABASE)

    print("inserting game objects")
    targets = db.table('targets')

    for game_object in gameobjects:
        print(f"game object: {game_object.get('id', '')}")
        targets.insert(game_object, conflict="replace").run(conn)
