import json

conffile = "heck.conf"

def write_config(config: dict):

    with open(conffile, "w") as f:
        f.write(json.dumps(config))
    f.close()

def read_config():
    with open(conffile, "r") as f:
        config = f.read()
    f.close()

    return json.loads(config)
