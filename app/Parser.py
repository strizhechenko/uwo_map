__author__ = 'oleg'
#coding:utf-8

from os import path
from City import City

def unicode_file(fname):
    if not path.exists(fname):
        return unicode("Файл не найден.", 'utf-8')
    with open(fname, 'r') as fin:
        output = unicode(fin.read(), 'utf-8')
    return output

file = 'app/data/db.markdown'

def get_city(city):
    f = open(file)
    found = False
    goods = []
    line = f.readline()
    while line:
        if line == ('# ' + city + "\n"):
            print "found! " + line
            found = True
        if found and line.startswith('- '):
            goods.append(line.replace('- ', '').replace("\n", ''))
        if found and line.startswith('# ') and line != ("# " + city + "\n"):
            break
        line = f.readline()
    return City(city, goods)


def read_cities():
    f = open(file)
    cities = []
    cityname = None
    citygoods = []
    line = f.readline()
    while line:
        if line.startswith("#"):
            if cityname:
                cities.append(City(cityname, citygoods))
            citygoods = []
            cityname = line.replace('# ', '')
        if line.startswith("-"):
            citygoods.append(line.replace('- ', ''))

        line = f.readline()

    if cityname:
        cities.append(City(cityname, citygoods))

    f.close()
    return cities