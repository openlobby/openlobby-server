#!/bin/sh

# migrate
python manage.py migrate

# Create log dirs and files
mkdir -p $( dirname $(cat /etc/supervisor/conf.d/supervisor.conf | grep logfile= | grep "\.log" | sed s/.*logfile=// ) )
touch $( cat /etc/supervisor/conf.d/supervisor.conf | grep logfile= | grep "\.log" | sed s/.*logfile=// )
mkdir /run/nginx

exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisor.conf --nodaemon
