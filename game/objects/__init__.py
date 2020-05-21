gameobjects = [
    {
        "id": "server1",
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
                "name": "secret.dat",
                "content": "very secret data\n"
            }, {
                "name": "users.dat",
                "content": "John\nGrace\nMildred\n"
            }]
        }, {
            "trashbin": [{
                "name": "email.txt",
                "content": "to my stupid boss: I quit!!\n"
            }]
        }]
    },
    {
        "id": "server2",
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
    }
]
