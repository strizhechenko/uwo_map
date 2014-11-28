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
version_file = '/usr/local/Reductor/etc/version'
version = unicode_file(version_file) 

def r_render(tmplt, env):
    env['devices'] = get_mirror_devices()
    env['host'] = host
    env['version'] = version
    env['rkndate'] = show_stdout('rkn_info.sh')
    return render_template(tmplt, env=env)

@app.route("/info")
def info():
    env = { 'output': show_stdout('show_stat.sh'), 'sidebar': 'info_sidebar.html', 'markdown': 1 }
    return r_render('default.html', env)

@app.route("/info/reports/<report>")
def reports(report):
    do_print = 1
    if request.args.get('print') != '1':
        do_print = 0
    print do_print
    env = { 'output': show_stdout('report_update.sh'), 'sidebar': 'info_sidebar.html', 'markdown': 1, 'print': do_print }
    print env
    return r_render('report.html', env)

@app.route("/info/log_full")
def log_full():
    env = { 'output': show_stdout('log4human.sh'), 'sidebar': 'info_sidebar.html', 'markdown': 1, 'sidebar_calendar': 1 }
    return r_render('log.html', env)

@app.route("/info/log")
def log():
    env = { 'output': show_stdout('log4human.sh update'), 'sidebar': 'info_sidebar.html', 'markdown': 1, 'sidebar_calendar': 1  }
    return r_render('log.html', env)

@app.route("/info/log_diag")
def log_diag():
    env = { 'output': show_stdout('log4human.sh diag'), 'sidebar': 'info_sidebar.html', 'markdown': 1, 'sidebar_calendar': 1 }
    return r_render('log.html', env)

@app.route("/info/diag")
def diag():
    env = { 'sidebar': 'info_sidebar.html' }
    return r_render('diag.html', env) 

@app.route("/info/diagnostic")
def diagnostic():
    output = show_stdout('diagnostic.sh')
    env = { 'output': output, 'sidebar': 'info_sidebar.html', 'markdown': 1 }
    return r_render('diag.html', env) 

@app.route("/lists/<list>")
def show_list(list):
    listdir = '/usr/local/Reductor/lists/'
    fname = listdir + list
    env = { 'sidebar': 'lists_sidebar.html', 'output': show_stdout('urldecode.sh ' + list), 'list': list }
    return r_render('lists.html', env)

@app.route("/machine_lists/<list>")
def show_machine_list(list):
    listdir = '/usr/local/Reductor/lists/'
    fname = listdir + list
    env = { 'sidebar': 'lists_sidebar.html', 'output': unicode_file(fname), 'list': list }
    return r_render('lists.html', env)

@app.route("/")
@app.route("/graphics")
def graphics():
    data = graphics_data()
    env = { 'data': data, 'sidebar': 'graphics_sidebar.html' }
    return r_render('graphics.html', env)

if __name__ == "__main__":
    app.run()
