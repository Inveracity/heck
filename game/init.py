import os
import inspect
import yaml

from rethinkdb import r
from game.database import connect

DATABASE = 'hack'
TABLES = ['players', 'targets']


def init():
    conn = connect()

    print("creating database")
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
    targets      = db.table('targets')
    filename     = inspect.getframeinfo(inspect.currentframe()).filename
    path         = os.path.dirname(os.path.abspath(filename))
    filepath     = os.path.join(path, "objects")
    game_objects = [f for f in os.listdir(filepath) if os.path.isfile(os.path.join(filepath, f))]

    for game_object in game_objects:
        file = os.path.join(filepath, game_object)
        with open(file) as f:
            game_object_data = f.read()

        loaded_game_object = yaml.safe_load(game_object_data)
        print(f"game object: {loaded_game_object.get('id', '')}")
        res = targets.insert(loaded_game_object, conflict="replace").run(conn)

if __name__ == "__main__":
    init()
