# coding:utf-8

from flask import Flask
from Routine import r_render
import Parser

app = Flask(__name__)

@app.route("/")
def map():
    return r_render('map.html')

@app.route("/people", methods=['GET'])
def cities():
    return r_render('cities.html', { 'cities': Parser.read_cities() })

if __name__ == "__main__":
    app.run()
