# coding:utf-8

from flask import Flask
from flask import request
from Routine import r_render
from Parser import read_cities
from Parser import get_city

app = Flask(__name__)

@app.route("/")
def map():
    return r_render('map.html')

@app.route("/cities", methods=['GET'])
def cities():
    return r_render('cities.html', { 'cities': Parser.read_cities() })

@app.route("/city", methods=['GET'])
def city():
    __city = get_city(request.args.get('city'))
    return r_render('city.html', {'city': __city})

if __name__ == "__main__":
    app.run()
