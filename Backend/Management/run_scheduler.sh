#!/bin/sh

while true
do
    echo "Checking overdue requests..."

    python manage.py check_overdue_requests

    echo "Next check in 1 hour..."

    sleep 3600
done