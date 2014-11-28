#!/bin/bash

uwsgi -s 0.0.0.0:80 --chdir=/opt/reductor_web --pidfile=/run/reductor_web.pid  --protocol=http -w WSGI:app
