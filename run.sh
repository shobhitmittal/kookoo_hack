#!/bin/bash

nohup /usr/bin/python cron.py >/dev/null 2>&1 &

if [ `ps aux |grep -v grep | grep -c cron.py` -gt 0 ]; then

echo 'Success in Running cron script'

cd kookoo_hack/
nohup /usr/bin/python manage.py runserver 0.0.0.0:80 >/dev/null 2>&1 &

if [ `ps aux | grep -v grep| grep -c manage.py` -gt 0 ]; then

echo 'The Server is running succesfully.You can logout now.'