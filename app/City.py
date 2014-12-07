#coding:utf-8

__author__ = 'oleg'

class City:

    def __init__(self, name, goods):
        self.name = name
        self.goods = goods

    def __repr__(self):
        return self.name