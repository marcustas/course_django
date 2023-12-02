#!/usr/bin/env bash

python3 manage.py migrate
python3 manage.py collectstatic --no-input
python3 manage.py compilemessages

# Запуск Django сервера
python3 manage.py runserver 0.0.0.0:8000
