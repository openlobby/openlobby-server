#!/bin/bash

# migrate
python manage.py migrate

# Create log dirs and files
mkdir -p $( dirname $(cat /etc/supervisor/supervisord.conf  | grep logfile= | grep "\.log" | sed s/.*logfile=// ) )
touch $( cat /etc/supervisor/supervisord.conf  | grep logfile= | grep "\.log" | sed s/.*logfile=// )
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisor.conf --nodaemon