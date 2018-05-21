# -*- coding: utf-8 -*-
# !/usr/bin/env python

from flask import Flask, jsonify, request
from data import DataCore
from data_display import DataDisplay
import pandas as pd
from util import traffic_decimal, parse_limit, parse_requests, data_after_argument, save_data
from json import dumps

__author__ = 'bernie'

app = Flask(__name__)


api_list = {
    'hello ': u'''Thanks for using''',
}

# 列表中的数据json格式用table
orient_format = ['get_time_traffic_count', 'get_url_status_code_count', 'get_ip_status_code_count']
d = DataCore()
data_io = False


@app.route('/')
def index():
    return jsonify(api_list)


@app.route('/total_data', methods=['GET'])
def show_log_data():
    error, kind, limit, use_index, is_show, dis_tick, ip, referer, start_time, end_time, is_qiniu = parse_requests(request)
    if error:
        return dumps(error)

    status_code = request.args.get('code', '')
    url = request.args.get('url', '')
    data, orient = get_data('get_data_by_factor', limit, status_code=status_code,
                            url=url, ip=ip, referer=referer, start_time=start_time,
                            end_time=end_time, is_qiniu=is_qiniu)
    if request.args.get('save'):
        save_data(data, 'get_data_by_factor', request.args.get('save'), request.args.get('pt'))
    return data.to_json(orient=orient)


@app.route('/url_traffic', methods=['GET'])
def show_url_traffic():
    error, kind, limit, use_index, is_show, dis_tick, ip, referer, start_time, end_time, is_qiniu = parse_requests(request)
    if error:
        return dumps(error)
    return get_data_and_show(kind, limit, use_index, is_show, dis_tick,
                             data_kind='get_url_traffic', xlabel='URL', ylabel='Traffic',
                             line_color='r', fig_color='b', funciton=traffic_decimal,
                             x_str='x', y_str='y', title='URL&Traffic', figsize=(12, 7), is_qiniu=is_qiniu)


@app.route('/url_count', methods=['GET'])
def show_url_count():
    error, kind, limit, use_index, is_show, dis_tick, ip, referer, start_time, end_time, is_qiniu = parse_requests(request)
    if error:
        return dumps(error)

    return get_data_and_show(kind, limit, use_index, is_show, dis_tick,
                             data_kind='get_url_count', xlabel='URL', ylabel='Count',
                             line_color='r', fig_color='b', funciton=traffic_decimal,
                             x_str='x', y_str='y', title='URL&Count', figsize=(12, 7), is_qiniu=is_qiniu)


@app.route('/get_ip_traffic', methods=['GET'])
def show_ip_traffic():
    error, kind, limit, use_index, is_show, dis_tick, ip, referer, start_time, end_time, is_qiniu = parse_requests(request)
    if error:
        return dumps(error)

    return get_data_and_show(kind, limit, use_index, is_show, dis_tick,
                             data_kind='get_ip_traffic', xlabel='IP', ylabel='Traffic',
                             line_color='r', fig_color='b', funciton=traffic_decimal,
                             x_str='x', y_str='y', title='IP&Traffic', figsize=(12, 7), is_qiniu=is_qiniu)


@app.route('/ip_count', methods=['GET'])
def show_ip_count():
    error, kind, limit, use_index, is_show, dis_tick, ip, referer, start_time, end_time, is_qiniu = parse_requests(request)
    if error:
        return dumps(error)

    return get_data_and_show(kind, limit, use_index, is_show, dis_tick,
                             data_kind='get_ip_count', xlabel='IP', ylabel='Count',
                             line_color='r', fig_color='b', funciton=traffic_decimal,
                             x_str='x', y_str='x', title='IP&Count', figsize=(12, 7), is_qiniu=is_qiniu)


@app.route('/get_code_count', methods=['GET'])
def show_code_count():
    error, kind, limit, use_index, is_show, dis_tick, ip, referer, start_time, end_time, is_qiniu = parse_requests(request)
    if error:
        return dumps(error)

    return get_data_and_show(kind, limit, use_index, is_show, dis_tick,
                             data_kind='get_code_count', xlabel='Code', ylabel='Count',
                             line_color='r', fig_color='b', funciton=traffic_decimal,
                             x_str='x', y_str='y', title='Code&Count', figsize=(12, 7), is_qiniu=is_qiniu)


@app.route('/ip_url_code_count', methods=['GET'])
def show_ip_url_code_count():
    error, kind, limit, use_index, is_show, dis_tick, ip, referer, start_time, end_time, is_qiniu = parse_requests(request)
    if error:
        return dumps(error)

    return get_data_and_show(kind, limit, use_index, is_show, dis_tick,
                             data_kind='get_ip_url_code_count', xlabel='Ip_Url_Code', ylabel='Count',
                             line_color='r', fig_color='b', funciton=traffic_decimal,
                             x_str='x', y_str='y', title='Ip_Url_Code&Count', figsize=(12, 7), is_qiniu=is_qiniu)


@app.route('/url_code_count', methods=['GET'])
def show_url_code_count():
    error, kind, limit, use_index, is_show, dis_tick, ip, referer, start_time, end_time, is_qiniu = parse_requests(request)
    if error:
        return dumps(error)

    return get_data_and_show(kind, limit, use_index, is_show, dis_tick,
                             data_kind='get_url_code_count', xlabel='URL_Code', ylabel='Count',
                             line_color='r', fig_color='b', funciton=traffic_decimal,
                             x_str='x', y_str='y', title='URL_Code&Count', figsize=(12, 7), is_qiniu=is_qiniu)


@app.route('/ip_code_count', methods=['GET'])
def show_ip_code_count():
    error, kind, limit, use_index, is_show, dis_tick, ip, referer, start_time, end_time, is_qiniu = parse_requests(request)
    if error:
        return dumps(error)

    return get_data_and_show(kind, limit, use_index, is_show, dis_tick,
                             data_kind='get_ip_code_count', xlabel='IP&Code', ylabel='Count',
                             line_color='r', fig_color='b', funciton=traffic_decimal,
                             x_str='x', y_str='y', title='IP&Code_Count', figsize=(12, 7), is_qiniu=is_qiniu)


@app.route('/time_traffic', methods=['GET'])
def show_time_traffic():
    error, kind, limit, use_index, is_show, dis_tick, ip, referer, start_time, end_time, is_qiniu = parse_requests(request)
    if error:
        return dumps(error)
    return get_data_and_show(kind, limit, use_index, is_show, dis_tick,
                             data_kind='get_time_traffic', xlabel='Time', ylabel='Traffic',
                             line_color='r', fig_color='b', funciton=traffic_decimal,
                             x_str='x', y_str='y', title='Time&Traffic', figsize=(12, 7),
                             start_time=start_time, end_time=end_time, is_qiniu=is_qiniu)


@app.route('/time_count', methods=['GET'])
def show_time_count():
    error, kind, limit, use_index, is_show, dis_tick, ip, referer, start_time, end_time, is_qiniu = parse_requests(request)
    if error:
        return dumps(error)
    return get_data_and_show(kind, limit, use_index, is_show, dis_tick,
                             data_kind='get_time_count', xlabel='Time', ylabel='Count',
                             line_color='r', fig_color='b', funciton=traffic_decimal,
                             x_str='x', y_str='y', title='Time&Count', figsize=(12, 7),
                             start_time=start_time, end_time=end_time, is_qiniu=is_qiniu)


def get_data_and_show(kind, limit, use_index, is_show, dis_tick, data_kind,
                      xlabel, ylabel, line_color, fig_color, funciton,
                      x_str, y_str, title, figsize, *args, **kwargs
                      ):
    data, orient = get_data(data_kind, limit, *args, **kwargs)
    if is_show and not data.empty:
        dd = DataDisplay()
        if kind == 'pie' and isinstance(data, pd.core.frame.DataFrame):
            return dumps({'error_kind': "DataFrame don't support pie"})
        dd.show_graphic(data, kind, use_index, xlabel=xlabel, ylabel=ylabel,
                        line_color=line_color, fig_color=fig_color, funciton=funciton,
                        x_str=x_str, y_str=y_str, title=title, figsize=figsize, dis_tick=dis_tick)
    if request.args.get('save'):
        save_data(data, data_kind, request.args.get('save'), request.args.get('pt'))
    return data.to_json(orient=orient)


def get_data(data_kind, limit, *args, **kwargs):
    global data_io
    if not data_io:
        if kwargs.get('is_qiniu'):
            d.generate_data(kwargs.get('is_qiniu'))
            data_io = True
        else:
            d.generate_data()
            data_io = True
    data = eval('d.{}(limit=parse_limit({}), *args, **kwargs)'.format(data_kind, 'limit'))
    orient = 'table' if data_kind in orient_format else 'index'
    return data, orient


if __name__ == '__main__':
    app.run()
