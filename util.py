# -*- coding: utf-8 -*-
# !/usr/bin/env python

import re


__author__ = 'berniey'


re_limit = re.compile(r"^[0-9]*:[0-9]*")


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
    if 1000000 < x <= 1000000000:
        return '{:1.1f}M'.format(x*1e-6)
    elif 1000000000 <= x < 1000000000000:
        return '{:1.2f}G'.format(x*1e-9)
    elif x <= 1000000000000:
        return '{:1.3f}P'.format(x * 1e-12)
    return '{:1.0f}K'.format(x*1e-3)


def data_after_argument(aim_data, *args, **kwargs):
    l1 = kwargs.get('limit')[0]
    l2 = kwargs.get('limit')[1]
    if l1 and l2:
        return aim_data[l1:l2]
    if l1 and not l2:
        return aim_data[l1:]
    if not l1 and l2:
        return aim_data[:l2]
    else:
        return aim_data


def parse_limit(limit):
    if not re_limit.match(limit):
        return '', ''
    a = limit.split(':')
    a1 = int(a[0]) if a[0] != '' else None
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
    return error, kind, limit, use_index
