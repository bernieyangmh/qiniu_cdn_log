# -*- coding: utf-8 -*-
# !/usr/bin/env python

import re
import time
import os

from sqlalchemy import create_engine
import pandas as pd
import requests

__author__ = 'berniey'


re_limit = re.compile(r"^[0-9]*:[0-9]*")
re_ip = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
re_time = re.compile(r"^\d{4}\-\d{2}\-\d{2}\s\d{2}\:\d{2}\:\d{2}$")


engine_mysql = create_engine("mysql+pymysql://{}:{}@localhost:3306/cdnlog".format
                             (os.environ.get('mysql_role'), os.environ.get('mysql_password')))

engine_pg = create_engine("postgresql://{}:{}@localhost:5432/cdnlog".format(
                            os.environ.get('pg_role'), os.environ.get('pg_password')))

series_to_frame_by_kind = {
                           'get_ip_traffic': (['ip'], 'traffic'),
                           'get_ip_count': (['ip'], 'count'),
                           'get_url_traffic': (['url'], 'traffic'),
                           'get_url_count': (['url'], 'count'),
                           'get_code_count': (['code'], 'count'),
                           'get_url_code_count': (['url', 'code'], 'count'),
                           'get_ip_code_count': (['ip', 'code'], 'count'),
                           'get_ip_url_code_count': (['ip', 'url', 'code'], 'count'),
                           'get_time_traffic_count': (['time'], 'traffic'),
                           }


def singleton(cls, *args, **kw):
    """
    @singleton
    def fun():
    """
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
    """
    :param x: value
    :param pos: placeholder

    :return: diff unit abbreviation
    """
    if x <= 1000:
        return '{:1.0f}'.format(x)
    elif 1000 < x <= 1000000:
        return '{:1.0f}K'.format(x*1e-3)
    elif 1000000 < x <= 1000000000:
        return '{:1.1f}M'.format(x*1e-6)
    elif 1000000000 <= x < 1000000000000:
        return '{:1.2f}G'.format(x*1e-9)
    elif x <= 1000000000000:
        return '{:1.3f}P'.format(x * 1e-12)
    return '{:1.0f}WTF'.format(x)


def data_after_argument(aim_data, *args, **kwargs):
    """
    if limit doesn't match re,return all
    if only :x return top x
    if only x: return last x
    if x:y return x to y
    """
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
    error = {}
    graphic_kinds = ['line', 'hist', 'area', 'bar', 'barh', 'kde', 'area', 'pie']
    kind = request.args.get('kind', 'line')
    limit = request.args.get('limit', ':')
    referer = request.args.get('referer', '')
    use_index = request.args.get('use_index', True)
    is_show = request.args.get('is_show', None)
    dis_tick = request.args.get('dis_tick', '')
    ip = request.args.get('ip', '')
    start_time = request.args.get('start_time', '')
    end_time = request.args.get('end_time', '')
    is_qiniu = request.args.get('is_qiniu', 'True')

    if kind not in graphic_kinds:
        error['error_kind'] = "you must have a choice among 'line','hist', 'bar', 'barh', 'kde', 'pie' or 'area'"

    if use_index in ['False', 'false', 'FALSE']:
        use_index = False

    if dis_tick:
        if kind == 'barh':
            dis_tick = 'y'
        else:
            dis_tick = 'x'

    if ip and not re_ip.match(ip):
        error['error_ip'] = "Please fill a Correct ip"

    if start_time and not re_time.match(start_time):
        error['error_start_time'] = "please fill a CORRECT start_time"

    if end_time and not re_time.match(end_time):
        error['error_end_time'] = "please fill a CORRECT end_time"

    return error, kind, limit, use_index, is_show, dis_tick, ip, referer, start_time, end_time, is_qiniu


def convert_time_format(request_time):
    """
    GMT convert to Beijing time
    :return time
    """
    struct_time = time.strptime(request_time, "[%d/%b/%Y:%X+0800]")
    timestamp = time.mktime(struct_time) + 28800
    time_array = time.localtime(timestamp)
    time_date = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    # 如果需要时间戳并且不需要时间的绘图，可以加上timestamp
    # return time_date, timestamp
    return time_date


def save_data(data, data_kind, save_kind, path_or_table):
    """
    Store data by arg
    """
    if save_kind in ['mysql', 'pg', 'postgresql']:
        if not path_or_table:
            path_or_table = data_kind+'_'+str(time.time())
        _save_database(data, data_kind, save_kind, path_or_table)
    if save_kind == 'excel':
        _save_file(data, data_kind, path_or_table, file_kinds='excel')
    if save_kind == 'csv':
        _save_file(data, data_kind, path_or_table, file_kinds='csv')


def print_summary_information(d, num=20):
    dict = d.get_code_count(limit=parse_limit(':{}'.format(num))).to_dict()
    print("\n打印日志汇总信息")
    print('*'*50+'\n')
    print("每个状态码所对应的访问次数\n")
    print("状态码      访问次数")
    for key, value in dict.items():
        print("{:<4} : {:10}".format(key, value))
    print("\n" + '*'*50 + "\n")
    print("流量排名前{}的url\n".format(num))
    print("{:<20}{}".format("流量(b)", "url", width=20))
    dict = d.get_url_traffic(limit=parse_limit(':{}'.format(num))).to_dict()
    for key, value in dict.items():
        print("{:<20} : {:10}".format(value, key))

    print("\n" + '*'*50 + "\n")

    print("访问次数排名前{}的url\n".format(num))
    print("{:<20}{}".format("访问次数", "url", width=20))
    dict = d.get_url_count(limit=parse_limit(':{}'.format(num))).to_dict()
    for key, value in dict.items():
        print("{:<20} : {:10}".format(value, key))

    print("\n" + '*'*50 + "\n")

    print("流量排名前{}的IP\n".format(num))
    print("{:<20}{}".format("流量", "IP", width=20))
    dict = d.get_ip_traffic(limit=parse_limit(':{}'.format(num))).to_dict()
    for key, value in dict.items():
        print("{:<20} : {:10}".format(value, key))

    print("\n" + '*'*50 + "\n")

    print("访问次数排名前{}的IP\n".format(num))
    print("{:<20}{}".format("访问次数", "IP", width=20))
    dict = d.get_ip_count(limit=parse_limit(':{}'.format(num))).to_dict()
    for key, value in dict.items():
        print("{:<20} : {:10}".format(value, key))


def _save_file(data, data_kind, path, file_kinds):
    columns_value = series_to_frame_by_kind.get(data_kind)
    if columns_value:
        data = series_to_dataframe(data, columns_value)
    path = _path_and_mkdir(path)
    if file_kinds == 'excel':
        from openpyxl import load_workbook
        if os.path.isfile(path):
            with pd.ExcelWriter(path, engine='openpyxl') as writer:
                writer.book = load_workbook(path)
                data.to_excel(writer, data_kind)
        else:
            out = pd.ExcelWriter(path)
            data.to_excel(out, data_kind)
            out.save()
    if file_kinds == 'csv':
        data.to_csv(path)


def _save_database(data, data_kind, save_kind, table_name):
    columns_value = series_to_frame_by_kind.get(data_kind)
    #选择数据库引擎
    engine = engine_mysql if save_kind == 'mysql' else engine_pg
    if columns_value:
        data = series_to_dataframe(data, columns_value)
    data.to_sql(table_name, engine, if_exists='replace')


def series_to_dataframe(data, columns_value):
    df = pd.DataFrame([i for i in data.index], columns=columns_value[0])
    df[columns_value[1]] = data.values
    return df


def _path_and_mkdir(path):
    """
    if dir not exist, make one
    """
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    return path


def ip_address(ip):
    """
    从淘宝和新浪获取ip的所在地
    """
    sina_data = {"ip": ip,
                 "type": "sina"
                 }

    sina_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    sina_r = requests.post("https://www.ipip.net/ip/ajax/", data=sina_data, headers=sina_headers)

    sina_district = (eval(sina_r.content.decode()))

    taobao_data = {"ip": ip,
                   "type": "taobao"
                   }

    taobao_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    taobao_r = requests.post("https://www.ipip.net/ip/ajax/", data=taobao_data, headers=taobao_headers)
    taobao_district = (eval(taobao_r.content.decode()))

    return {"taobao": taobao_district, "sina": sina_district}
