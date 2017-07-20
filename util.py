# -*- coding: utf-8 -*-
# !/usr/bin/env python

import re
import time

__author__ = 'berniey'


re_limit = re.compile(r"^[0-9]*:[0-9]*")
re_ip = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

def singleton(cls, *args, **kw):
    '''
    @singleton
    def fun()
    '''
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


class SingletonMetaclass(type):
    """
    Singleton Metaclass

    @singleton
    class someclass(object):

    """

    _inst = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._inst:
            cls._inst[cls] = super(SingletonMetaclass, cls).__call__(*args)
        return cls._inst[cls]


def traffic_decimal(x, pos):
    if x <= 1000000:
        return '{:1.0f}'.format(x)
    if 1000000 < x <= 1000000000:
        return '{:1.1f}M'.format(x*1e-6)
    elif 1000000000 <= x < 1000000000000:
        return '{:1.2f}G'.format(x*1e-9)
    elif x <= 1000000000000:
        return '{:1.3f}P'.format(x * 1e-12)
    return '{:1.0f}WTF'.format(x*1e-3)


def data_after_argument(aim_data, *args, **kwargs):

    l1 = kwargs.get('limit')[0]
    l2 = kwargs.get('limit')[1]
    if l1 >= 0 and l2:
        return aim_data[l1:l2]
    if l1 >= 0 and not l2:
        return aim_data[l1:]
    if not l1 and l2 >= 0:
        return aim_data[:l2]
    else:
        return aim_data


def parse_limit(limit):
    if not re_limit.match(limit):
        return 0, 0
    a = limit.split(':')
    a1 = int(a[0]) if a[0] != '' else 0
    a2 = int(a[1]) if a[1] != '' else None
    return a1, a2


def parse_requests(request):
    error = ''
    graphic_kinds = ['line', 'hist', 'area', 'bar', 'barh', 'kde']
    kind = request.args.get('kind', 'line')
    limit = request.args.get('limit', ':')
    if kind not in graphic_kinds:
        error = "you must have a choice among 'line','hist', 'bar', 'barh', 'kde' or 'area'"
    use_index = request.args.get('use_index', True)
    if use_index in ['False', 'false', 'FALSE']:
        use_index = False
    show = request.args.get('show', None)
    dis_tick = request.args.get('dis_tick', '')
    if dis_tick:
        if kind == 'barh':
            dis_tick = 'y'
        else:
            dis_tick = 'x'
    ip = request.args.get('ip', '')
    if ip and not re_ip.match(ip):
        error = "Please fill a Correct ip"
    referer = request.args.get('referer', '')
    return error, kind, limit, use_index, show, dis_tick, ip, referer


def convert_time_format(request_time):
    struct_time = time.strptime(request_time, "[%d/%b/%Y:%X+0800]")
    timestamp = time.mktime(struct_time) + 28800
    time_array = time.localtime(timestamp)
    time_date = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return time_date, timestamp


