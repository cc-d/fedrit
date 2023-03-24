rm -r api/migrations
rm db.sqlite3
python3 manage.py makemigrations api
python3 manage.py migrate
