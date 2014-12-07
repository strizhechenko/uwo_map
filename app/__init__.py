#coding:utf-8

from flask import Flask
from flask import render_template
from flask import make_response
from flask import request

from lastfm import user_artists

import sys
import json
import socket
import time

app = Flask(__name__)
host = socket.gethostname()

def r_render(tmplt, env):
    return render_template(tmplt, env=env)

def get_artists(username):
    if not username or username == '':
	return []
    return user_artists(username)

@app.route("/")
@app.route("/people", methods=['GET', 'POST'])
def people():
    user1, user2 = request.args.get('user1'), request.args.get('user2')
    user1artists = get_artists(user1)
    if not user1:
        user1 = ''
    user2artists = get_artists(user2)
    if not user2:
        user2 = ''
    diff = set(user1artists) & set(user2artists)
    env = {'user1': user1, 'user2': user2, 'user1artists': user1artists, 'user2artists': user2artists, 'diff': diff}
    return r_render('people.html', env)

@app.route("/three", methods=['GET', 'POST'])
def three():
    user1, user2, user3 = request.args.get('user1'), request.args.get('user2'), request.args.get('user3')
    user1artists = get_artists(user1)
    if not user1:
        user1 = ''
    user2artists = get_artists(user2)
    if not user2:
        user2 = ''
    user3artists = get_artists(user3)
    if not user3:
        user3 = ''
    diff = set(user1artists) & set(user2artists) & set(user3artists)
    env = {'diff': diff}
    return r_render('people.html', env)


@app.route("/first", methods=['GET', 'POST'])
def first():
    user1, user2 = request.args.get('user1'), request.args.get('user2')
    user1artists = get_artists(user1)
    if not user1:
        user1 = ''
    user2artists = get_artists(user2)
    if not user2:
        user2 = ''
    diff = set(user1artists) - (set(user1artists) & set(user2artists))
    env = {'user1': user1, 'user2': user2, 'user1artists': user1artists, 'user2artists': user2artists, 'diff': diff}
    return r_render('people.html', env)

@app.route("/eval", methods=['GET', 'POST'])
def eval():
    user1, user2 = request.args.get('user1'), request.args.get('user2')
    user1artists = get_artists(user1)
    if not user1:
        user1 = ''
    user2artists = get_artists(user2)
    if not user2:
        user2 = ''
    diff = set(user1artists) - (set(user1artists) & set(user2artists))
    env = {'user1': user1, 'user2': user2, 'user1artists': user1artists, 'user2artists': user2artists, 'diff': diff}
    return r_render('eval.html', env)

if __name__ == "__main__":
    app.run()
