# -*- coding: utf-8 -*-
# !/usr/bin/env python

__author__ = 'bernie'

from flask import Flask, jsonify, request
from data import DataCore
from data_display import DataDisplay
import re
from util import traffic_decimal, parse_limit, parse_requests, data_after_argument


app = Flask(__name__)


api_list = {
    '/show_url_traffic_data': u'''show all url's traffic''',
}


@app.route('/')
def index():
    return jsonify(api_list)


@app.route('/total_data', methods=['GET'])
def show_log_data():
    error, kind, limit, use_index, is_show, dis_tick, ip, referer = parse_requests(request)
    if error:
        return error

    status_code = request.args.get('status_code', '')
    url = request.args.get('url', '')
    data, orient = get_data('get_data_by_factor', limit, status_code=status_code, url=url, ip=ip, referer=referer)
    return data.to_json(orient=orient)


@app.route('/url_traffic_graphic', methods=['GET'])
def show_url_traffic_graphic():
    error, kind, limit, use_index, is_show, dis_tick, ip, referer = parse_requests(request)
    if error:
        return error
    return get_data_and_show(kind, limit, use_index, is_show, dis_tick,
                             data_kind='get_url_traffic_data', xlabel='xlabel', ylabel='ylabel',
                             line_color='r', fig_color='b', funciton=traffic_decimal,
                             x_str='xxxxx', y_str='yyyy', title='C D N', figsize=(12, 7))


@app.route('/url_count_graphic', methods=['GET'])
def url_count_graphic():
    error, kind, limit, use_index, is_show, dis_tick, ip, referer = parse_requests(request)
    if error:
        return error

    return get_data_and_show(kind, limit, use_index, is_show, dis_tick,
                             data_kind='get_url_count_data', xlabel='xlabel', ylabel='ylabel',
                             line_color='r', fig_color='b', funciton=traffic_decimal,
                             x_str='xxxxx', y_str='yyyy', title='C D N', figsize=(12, 7))


@app.route('/ip_traffic_graphic', methods=['GET'])
def ip_traffic_graphic():
    error, kind, limit, use_index, is_show, dis_tick, ip, referer = parse_requests(request)
    if error:
        return error

    return get_data_and_show(kind, limit, use_index, is_show, dis_tick,
                             data_kind='get_ip_traffic_data', xlabel='xlabel', ylabel='ylabel',
                             line_color='r', fig_color='b', funciton=traffic_decimal,
                             x_str='xxxxx', y_str='yyyy', title='C D N', figsize=(12, 7))


@app.route('/ip_count_graphic', methods=['GET'])
def ip_count_graphic():
    error, kind, limit, use_index, is_show, dis_tick, ip, referer = parse_requests(request)
    if error:
        return error

    return get_data_and_show(kind, limit, use_index, is_show, dis_tick,
                             data_kind='get_ip_count_data', xlabel='xlabel', ylabel='ylabel',
                             line_color='r', fig_color='b', funciton=traffic_decimal,
                             x_str='xxxxx', y_str='yyyy', title='C D N', figsize=(12, 7))


@app.route('/total_status_code_count_graphic', methods=['GET'])
def total_status_code_count_graphic():
    error, kind, limit, use_index, is_show, dis_tick, ip, referer = parse_requests(request)
    if error:
        return error

    return get_data_and_show(kind, limit, use_index, is_show, dis_tick,
                             data_kind='get_total_status_code_count', xlabel='xlabel', ylabel='ylabel',
                             line_color='r', fig_color='b', funciton=traffic_decimal,
                             x_str='xxxxx', y_str='yyyy', title='C D N', figsize=(12, 7))


@app.route('/ip_url_status_code_count_graphic', methods=['GET'])
def ip_url_status_code_count_graphic():
    error, kind, limit, use_index, is_show, dis_tick, ip, referer = parse_requests(request)
    if error:
        return error

    return get_data_and_show(kind, limit, use_index, is_show, dis_tick,
                             data_kind='get_ip_url_status_code_count', xlabel='xlabel', ylabel='ylabel',
                             line_color='r', fig_color='b', funciton=traffic_decimal,
                             x_str='xxxxx', y_str='yyyy', title='C D N', figsize=(12, 7))


@app.route('/url_status_code_count_graphic', methods=['GET'])
def url_status_code_count_graphic():
    error, kind, limit, use_index, is_show, dis_tick, ip, referer = parse_requests(request)
    if error:
        return error

    return get_data_and_show(kind, limit, use_index, is_show, dis_tick,
                             data_kind='get_url_status_code_count', xlabel='xlabel', ylabel='ylabel',
                             line_color='r', fig_color='b', funciton=traffic_decimal,
                             x_str='xxxxx', y_str='yyyy', title='C D N', figsize=(12, 7))

@app.route('/ip_status_code_count_graphic', methods=['GET'])
def ip_status_code_count_graphic():
    error, kind, limit, use_index, is_show, dis_tick, ip, referer = parse_requests(request)
    if error:
        return error

    return get_data_and_show(kind, limit, use_index, is_show, dis_tick,
                             data_kind='get_ip_status_code_count', xlabel='xlabel', ylabel='ylabel',
                             line_color='r', fig_color='b', funciton=traffic_decimal,
                             x_str='xxxxx', y_str='yyyy', title='C D N', figsize=(12, 7))


@app.route('/time_traffic_count', methods=['GET'])
def time_traffic_count_graphic():
    error, kind, limit, use_index, is_show, dis_tick, ip, referer =parse_requests(request)
    if error:
        return error
    return get_data_and_show(kind, limit, use_index, is_show, dis_tick,
                             data_kind='get_time_traffic_count', xlabel='xlabel', ylabel='ylabel',
                             line_color='r', fig_color='b', funciton=traffic_decimal,
                             x_str='xxxxx', y_str='yyyy', title='C D N', figsize=(12, 7))


def get_data_and_show(kind, limit, use_index, is_show, dis_tick, data_kind,
                      xlabel, ylabel, line_color, fig_color, funciton,
                      x_str, y_str, title, figsize
                      ):
    data, orient = get_data(data_kind, limit)

    if is_show and data.any():
        dd = DataDisplay()
        dd.show_graphic(data, kind, use_index, xlabel=xlabel, ylabel=ylabel,
                        line_color=line_color, fig_color=fig_color, funciton=funciton,
                        x_str=x_str, y_str=y_str, title=title, figsize=figsize, dis_tick=dis_tick)
    return data.to_json(orient=orient)


def get_data(data_kind, limit, *args, **kwargs):
    d = DataCore()
    d.generate_data()
    data = eval('d.{}(limit=parse_limit({}), *args, **kwargs)'.format(data_kind, 'limit'))
    orient = 'table' if data_kind == 'get_time_traffic_count' else 'index'
    return data, orient



if __name__ == '__main__':
    app.run()

