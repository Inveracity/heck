#!/bin/sh
pyinstaller --specpath bin/ \
            --distpath bin/dist \
            --workpath bin/build \
            --log-level ERROR \
            --icon icon.ico \
            --onefile \
            --hidden-import pkg_resources.py2_warn \
            heck.py
