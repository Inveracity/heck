import json
from typing import NoReturn

conffile = "heck.conf"


def write_config(config: dict) -> NoReturn:

    try:
        with open(conffile, "w") as f:
            f.write(json.dumps(config))
        f.close()

    except PermissionError:
        print("Could not write file to disk: Permission denied")
        exit(1)


def read_config() -> dict:
    with open(conffile, "r") as f:
        config = f.read()
    f.close()

    return json.loads(config)
