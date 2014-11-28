#coding:utf-8

db = '/opt/reductor_web/app/db/reductor.db'

import sqlite3
from os import system
from os import path
from os import readlink
import subprocess
import netifaces
import time

def unicode_file(fname):
    if not path.exists(fname):
        return unicode("Файл не найден.", 'utf-8')
    with open(fname, 'r') as fin:
        out = fin.read()
        output = unicode(out, 'utf-8')
    return output

def show_stdout(binary):
    system('/opt/reductor_web/scripts/' + binary)
    return unicode_file('/tmp/reductor/' + binary.split(' ')[0])

def get_mirror_devices():
    list = []
    for dev in netifaces.interfaces():
        if dev.startswith('eth'):
             bridge_file = '/sys/class/net/' + dev + '/brport/bridge'
             if path.islink(bridge_file):
                 bridge = readlink(bridge_file)
                 list.append(dev)
    return list

def timing2groupby(date):
    # month - день, week - 4 часа, day - час, hour - 5 минут
    timings = { 'month': 24*60*60, 'week': 4*60*60, 'day': 60*60, 'hour': 5*60 }
    return timings[date]

def timing2format(timing):
    timings = { 'month': "%d.%m.%Y", 'week': "%d.%m.%Y %H:00", 'day': "%H:%M", 'hour': "%H:%M" }
    return timings[timing]

def timing2start_time(timing):
    timings = { 'month': 60*60*24*7*30, 'week': 60*60*24*7, 'day': 60*60*24, 'hour': 60*60 }
    return int(time.time()) - timings[timing]

def __graphic(timing, name, title, sql, header):
    start_time = timing2start_time(timing)
    groupby_seconds = timing2groupby(timing)
    graphic = {}
    graphic['name'] = str(timing) + name
    graphic['title'] = unicode(title, 'utf8')
    graphic['timing'] = timing
    sql = sql + " date > " + str(start_time) + " group by date / " + str(groupby_seconds)
    conn = sqlite3.connect(db)
    c = conn.cursor()
    raw_data = [ header ]
    format = timing2format(timing)
    for row in conn.cursor().execute(sql):
        l = list(row)
        l[0] = time.strftime(format, time.localtime(row[0]))
        for i in range(1, len(l)):
            l[i] = int(l[i])
        raw_data.append(l)
    conn.commit()
    conn.close()
    graphic['raw_data'] = raw_data
    return graphic

def usedcpu(timing):
    return __graphic(timing, "usedcpu", "Нагрузка на процессор, %", "SELECT date, avg(used) FROM usedcpu WHERE", [ 'date', 'percent' ])

def usedmem(timing):
    return __graphic(timing, "usedmem", "Потребление памяти, %", "SELECT date, avg(used) FROM usedmem WHERE", [ 'date', 'percent' ])

def list_actuality(timing):
    return __graphic(timing, "list_actuality", "Устаревание списков (больше 6 - плохо)", "SELECT date, avg(delta/60/60) FROM list_actuality WHERE list = 'register.zip' and", [ 'date', 'hours' ])

def packets(device, timing):
    sql = "SELECT date, avg(count), avg(bytes/1000) FROM rxtx WHERE x = 'rx' and dev = '" + device + "' and"
    return __graphic(timing, "packets" + str(device), "Пакетов/сек, " + str(device), sql, [ 'date', 'packets', 'kbytes' ])

def packets_checked(timing):
    sql = "SELECT date, avg(checked) FROM packets_checked WHERE"
    return __graphic(timing, "check", "Проверенно пакетов/мин (http)", sql, [ 'date', 'checked' ])

def packets_matched(timing):
    sql = "SELECT date, avg(matched) FROM packets_checked WHERE"
    return __graphic(timing, "match", "Сайтов заблокировано/мин (http)", sql, [ 'date', 'matched' ])

def graphics_data():
    data = []
    for timing in [ 'month', 'day' ]:
        for device in get_mirror_devices():
            data.append(packets(device, timing))
        data.append(packets_checked(timing))
        data.append(packets_matched(timing))
        data.append(usedcpu(timing))
        data.append(usedmem(timing))
        if timing == 'hour':
            continue
        data.append(list_actuality(timing))
    return data
