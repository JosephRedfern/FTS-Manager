#!/bin/sh
echo Starting Gunicorn.
cd FTSManager
exec gunicorn FTSManager.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4
