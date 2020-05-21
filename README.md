# heck

hacking mini game Written in Python 3.8

## Prototype screenshot

![](docs/images/prototype.png)

## Install development environment

Start database

```bash
docker-compose up -d
```

Install dependencies

```bash
# Install pipenv
pip install pipenv

# Install dependencies
pipenv sync

# Set up game data
pipenv run heck init

# show help text
pipenv run heck -h
```

## Build binary

```bash
pipenv sync --dev
sh bin/build.sh

bin/dist/heck -h
# or windows
bin/dist/heck.exe -h
```

_to be continued_
