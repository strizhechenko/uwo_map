#!/bin/bash

uwsgi -s 127.0.0.1:8085 --chdir=/opt/lastfm --pidfile=/run/lastfm.pid  --protocol=http -w WSGI:app
