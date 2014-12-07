__author__ = 'oleg'
#coding:utf-8

from os import path
from City import City

file = 'app/data/db.markdown'

def unicode_file(fname):
    if not path.exists(fname):
        return unicode("Файл не найден.", 'utf-8')
    with open(fname, 'r') as fin:
        output = unicode(fin.read(), 'utf-8')
    return output

def is_header(line):
    return line.startswith('# ')

def is_list(line):
    return line.startswith('- ')

def get_city(city):
    f = open(file)
    found = False
    goods = []
    line = f.readline()
    while line:
        if is_header(line):
            if found:
                    break
            if line == ('# ' + city + "\n"):
                found = True
        if found and is_list(line):
            goods.append(line.replace('- ', '').replace("\n", ''))
        line = f.readline()

    f.close()
    return City(city, goods)

def read_cities():
    f = open(file)
    cities = []
    cityname = None
    citygoods = []
    line = f.readline()
    while line:
        if is_header(line):
            if cityname:
                cities.append(City(cityname, citygoods))
            citygoods = []
            cityname = line.replace('# ', '')
        if is_list(line):
            citygoods.append(line.replace('- ', ''))

        line = f.readline()

    if cityname:
        cities.append(City(cityname, citygoods))

    f.close()
    return cities