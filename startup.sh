#!/bin/bash

echo "Starting up..."

echo "Checking variables:"
echo "Package directory: $(pwd)/$FLASK_APP" 
echo "Environment: $FLASK_ENV"

echo "Checking config.py..."

FILE=./instance/config.py
if [ -f "$FILE" ]; then
    echo "$FILE already exists."
else
    echo "Creating Secret..."
    echo $(python -c 'import os; print(os.urandom(16))') >> ./instance/config.py
fi

echo "Checking database..."
DATABASE=./instance/app.sqlite
if [ -f "$DATABASE" ]; then
    echo "$DATABASE already exists."
else
    echo "Creating Database..."
    echo $(flask init-db)
fi

echo "Startig webserver..."
echo $(waitress-serve --call 'app:create_app')

