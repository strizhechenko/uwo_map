# coding:utf-8

__author__ = 'oleg'

from flask import render_template

def r_render(tmplt, env=None):
    if not env:
        env = {}
    return render_template(tmplt, env=env)