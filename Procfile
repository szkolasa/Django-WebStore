web: python manage.py runserver
web: gunicorn WebStore.wsgi:application --log-file -
heroku ps:scale web=1
