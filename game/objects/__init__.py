gameobjects = [
    {
        "id": "venus",
        "type": "server",
        "states": {
            "hacked": 0,
            "online": 1
        },
        "password": "racehorse",
        "ports": {
            "3306": {
                "vuln": ["crack"],
                "info": "database server",
                "state": "open"
            }
        },
        "files": [{
            "data": [{
                "name": "sentinel.dat",
                "content": "encryption key: r25KjzgbsKiOUdD7"
            }, {
                "name": "users.dat",
                "content": "John\nGrace\nMildred\n"
            }]
        }, {
            "trashbin": [{
                "name": "email.txt",
                "content": "\n  From: Mildred\n  To  : Grace\n  We keep getting hacked, it's awful! I QUIT!\n"
            }]
        }]
    },
    {
        "id": "mars",
        "type": "server",
        "sentinel": "warrior",
        "states": {
            "hacked": 0,
            "online": 1
        },
        "ports": {
            "80": {
                "vuln": ["ddos"],
                "info": "web server",
                "state": "open"
            },
            "443": {
                "vuln": ["ddos"],
                "info": "secure web server",
                "state": "open"
            }
        }
    },
    {
        "id": "warrior",
        "type": "sentinel",
        "states": {
            "online": 1,
            "detected": 0
        },
        "key": "r25KjzgbsKiOUdD7",
        "killswitch": "raspberries",
        "ports": {
            "16660": {
                "vuln": ["deflect"],
                "info": "sentinel service",
                "state": "open"
            }
        }
    }
]
