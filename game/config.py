import json
from pathlib import Path
from typing import NoReturn

conffile = "heck.conf"


def write_config(config: dict) -> NoReturn:
    try:
        Path(conffile).write_text(json.dumps(config))

    except PermissionError:
        print("Could not write file to disk: Permission denied")
        exit(1)


def read_config() -> dict:
    return json.loads(Path(conffile).read_text())
