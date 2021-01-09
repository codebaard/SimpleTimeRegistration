#!/bin/sh

FILE=/instance/config.py
if test -f "$FILE"; then
    echo "$FILE already exists."
else
    echo "Creating Secret..."
    echo $(python -c 'import os; print(os.urandom(16))') > ./instance/config.py
fi

echo "Startig webserver..."
echo $(waitress-serve --call 'app:create_app')

