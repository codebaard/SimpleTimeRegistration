echo "Creating Secret..."
echo $(python -c 'import os; print(os.urandom(16))') > config.py

echo "Startig webserver..."
waitress-serve --call 'app:create_app'

