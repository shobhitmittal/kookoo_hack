#!/bin/bash

nohup /usr/bin/python cron.py >/dev/null 2>&1 &
cd kookoo/
nohup /usr/bin/python manage.py runserver 0.0.0.0:80 >/dev/null 2>&1 &