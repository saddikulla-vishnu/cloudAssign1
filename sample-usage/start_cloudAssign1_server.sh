cd <path-to-django-project> && gunicorn -w 2 -b 0.0.0.0:8080 --chdir <path-to-directory-of-wsgi.py> wsgi:application --daemon
