#!/bin/sh

FILE=/instance/config.py
if test -f "$FILE"; then
    echo "$FILE already exists."
else
    echo "Creating Secret..."
    echo $(python -c 'import os; print(os.urandom(16))') > ./instance/config.py
fi

DATABASE=/instance/app.sqlite
if test -f "$DATABASE"; then
    echo "$DATABSE already exists."
else
    echo "Creating Database..."
    echo $(app init-db)

echo "Startig webserver..."
echo $(waitress-serve --call 'app:create_app')

