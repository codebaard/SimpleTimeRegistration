#!/bin/sh

echo "Creating Secret..."
echo $(python -c 'import os; print(os.urandom(16))') > ./instance/config.py

echo "Startig webserver..."
waitress-serve --call 'app:create_app'

