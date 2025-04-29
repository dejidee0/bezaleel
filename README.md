gunicorn property.wsgi:application
--workers 3 --bind 0.0.0.0:8000

gunicorn property.wsgi.app:application
