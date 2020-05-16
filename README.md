# heck

hacking mini game Written in Python 3.8

# Install development environment

Start database

```bash
docker-compose up -d
```

Install dependencies

```bash
pip install pipenv
pipenv sync

# Set up game data
pipenv run python game/init.py

# Try scan.py
pipenv run python scan.py
```

_to be continued_
