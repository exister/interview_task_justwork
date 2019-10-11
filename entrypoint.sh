#!/usr/bin/env bash

set -e

/app/wait-for-it.sh db:5432 -t 0

if [ "$1" == 'runserver' ]; then
    su-exec web python manage.py migrate
    su-exec web python manage.py loaddata --app pages --format=yaml auth pages
    exec su-exec web python manage.py runserver 0.0.0.0:8000
fi

exec "$@"
