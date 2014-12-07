#!/bin/bash

uwsgi -s 127.0.0.1:8085 --chdir=/opt/uwo --pidfile=/run/uwo.pid  --protocol=http -w WSGI:app
