# -*- coding: utf-8 -*-
# !/usr/bin/env python

import re
import time
from sqlalchemy import create_engine
import pandas as pd

__author__ = 'berniey'


re_limit = re.compile(r"^[0-9]*:[0-9]*")
re_ip = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")


engine_mysql = create_engine("mysql+pymysql://work:123@localhost:3306/cdn")

engine_pg = create_engine("postgresql://work:123@localhost:5432/cdn")

series_to_frame_by_kind = {
                           'get_ip_traffic_data': (['ip'], 'traffic'),
                           'get_ip_count_data': (['ip'], 'count'),
                           'get_url_traffic_data': (['url'], 'traffic'),
                           'get_url_count_data': (['url'], 'count'),
                           'get_total_status_code_count': (['code'], 'traffic'),
                           'get_url_status_code_count': (['url', 'code'], 'count'),
                           'get_ip_status_code_count': (['ip', 'code'], 'count'),
                           'get_ip_url_status_code_count': (['ip', 'code'], 'count'),
                           'get_time_traffic_count': (['time'], 'traffic'),
                           }



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

    __metaclass__ = SingletonMetaclass

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

    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    return error, kind, limit, use_index, show, dis_tick, ip, referer, start_time, end_time


def convert_time_format(request_time):
    struct_time = time.strptime(request_time, "[%d/%b/%Y:%X+0800]")
    timestamp = time.mktime(struct_time) + 28800
    time_array = time.localtime(timestamp)
    time_date = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    # return time_date, timestamp
    return time_date


def save_data(data, data_kind, save_kind, path_or_table='.'):
    if save_kind == ('mysql' or 'pg' or 'postgres'):
        return save_database()
    if save_kind == 'txt':
        pass
    if save_kind == 'csv':
        pass
    if save_kind == 'md':
        pass



def save_database(data, data_kind, save_kind, table_name):
    # 确定index转换为clomuns的名称
    columns_value = series_to_frame_by_kind.get(data_kind)
    #选择数据库引擎
    engine = engine_mysql if save_kind == 'mysql' else engine_pg

    _save_database_act(data, engine, table_name, columns_value[0], columns_value[1])


def _save_database_act(data, engine, table_name, columns, values_name):
    df = pd.DataFrame([i for i in data.index], columns=columns)
    df[values_name] = data.values
    df.to_sql(table_name, engine, if_exists='replace')


