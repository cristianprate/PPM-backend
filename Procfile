web: python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn ems.wsgi --log-file -
python manage.py migrate && \
python manage.py loaddata db.json && \
gunicorn ems.wsgi