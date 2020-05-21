#!/bin/sh
pyinstaller --specpath bin \
            --distpath bin/dist \
            --workpath bin/build \
            --log-level ERROR \
            --icon icon.ico \
            --onefile \
            --clean \
            heck.py
