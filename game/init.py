import traceback

from sys import exit

from typing import NoReturn

from rethinkdb import r
from game.database import connect
from game.objects import gameobjects
from game.config import write_config

DATABASE = 'hack'
TABLES = ['players', 'targets']


def init(host: str, password: str) -> NoReturn:
    """ Initialise game with a config and inserting game objects into database """

    write_config({"host": host, "password": password})

    conn = connect()

    print("creating database")
    r.db_drop(DATABASE).run(conn)
    if DATABASE not in r.db_list().run(conn):
        r.db_create(DATABASE).run(conn)

    print("creating tables")
    for table in TABLES:
        if table not in r.db(DATABASE).table_list().run(conn):
            r.db(DATABASE).table_create(table).run(conn)

    db = r.db(DATABASE)

    players = db.table('players')
    players.insert({"id": 1, "player": "john"}).run(conn)

    print("inserting game objects")
    targets = db.table('targets')

    for game_object in gameobjects:
        print(f"game object: {game_object.get('id', '')}")
        targets.insert(game_object, conflict="replace").run(conn)
