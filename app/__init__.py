#coding:utf-8

from flask import Flask
from flask import render_template
from flask import make_response
from flask import request

import sys
import json
import socket
import time

from reductor import unicode_file
from reductor import show_stdout
from reductor import get_mirror_devices
from reductor import graphics_data

app = Flask(__name__)
host = socket.gethostname()

def r_render(tmplt, env):
    return render_template(tmplt, env=env)

@app.route("/")
@app.route("/people")
def graphics():
    env = { }
    return r_render('people.html', env)

if __name__ == "__main__":
    app.run()
