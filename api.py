# -*- coding: utf-8 -*-
# !/usr/bin/env python

__author__ = 'bernie'

from flask import Flask, jsonify, request
from data import DataCore
from data_display import DataDisplay
import re
from util import traffic_decimal, parse_limit, parse_requests


app = Flask(__name__)


api_list = {
    '/show_url_traffic_data': u'''show all url's traffic''',
}


@app.route('/')
def index():
    return jsonify(api_list)


@app.route('/url_traffic_graphic', methods=['GET'])
def show_url_traffic_graphic():
    error, kind, limit, use_index = parse_requests(request)
    if error:
        return error
    d = DataCore()
    d.generate_data()
    data = d.get_url_traffic_data(limit=parse_limit(limit))
    if request.args.get('show') and data.any():
        dd = DataDisplay()
        dd.show_graphic(data, kind, use_index, xlabel='xlabel', ylabel='ylabel',
                        line_color='r', fig_color='b', funciton=traffic_decimal,
                        x_str='xxxxx', y_str='yyyy', title='QiNiu CDN', figsize=(12, 7)
                        )
    return data.to_frame().to_json(orient='index')


@app.route('/url_count_graphic', methods=['GET'])
def url_count_graphic():
    error, kind, limit, use_index = parse_requests(request)
    if error:
        return error

    d = DataCore()
    d.generate_data()
    data = d.get_url_count_data(limit=parse_limit(limit))
    if request.args.get('show') and data.any():
        dd = DataDisplay()
        dd.show_graphic(data, kind, use_index)
    return data.to_frame().to_json(orient='index')


@app.route('/ip_traffic_graphic', methods=['GET'])
def ip_traffic_graphic():
    error, kind, limit, use_index = parse_requests(request)
    if error:
        return error

    d = DataCore()
    d.generate_data()
    data = d.get_ip_traffic_data(limit=parse_limit(limit))
    if request.args.get('show') and data.any():
        dd = DataDisplay()
        dd.show_graphic(data, kind, use_index)
    return data.to_frame().to_json(orient='index')


@app.route('/ip_count_graphic', methods=['GET'])
def ip_count_graphic():
    error, kind, limit, use_index = parse_requests(request)
    if error:
        return error

    d = DataCore()
    d.generate_data()
    data = d.get_ip_count_data(limit=parse_limit(limit))
    if request.args.get('show') and data.any():
        dd = DataDisplay()
        dd.show_graphic(data, kind, use_index)
    return data.to_frame().to_json(orient='index')


@app.route('/total_status_code_count_graphic', methods=['GET'])
def total_status_code_count_graphic():
    error, kind, limit, use_index = parse_requests(request)
    if error:
        return error

    d = DataCore()
    d.generate_data()
    data = d.get_total_status_code_count(limit=parse_limit(limit))
    if request.args.get('show') and data.any():
        dd = DataDisplay()
        dd.show_graphic(data, kind, use_index)
    return data.to_frame().to_json(orient='index')


@app.route('/ip_url_status_code_count_graphic', methods=['GET'])
def ip_url_status_code_count_graphic():
    error, kind, limit, use_index = parse_requests(request)
    if error:
        return error

    d = DataCore()
    d.generate_data()
    data = d.get_ip_url_status_code_count(limit=parse_limit(limit))
    if request.args.get('show') and data.any():
        dd = DataDisplay()
        dd.show_graphic(data, kind, use_index)
    return data.to_frame().to_json(orient='index')


@app.route('/url_status_code_count_graphic', methods=['GET'])
def url_status_code_count_graphic():
    error, kind, limit, use_index = parse_requests(request)
    if error:
        return error

    d = DataCore()
    d.generate_data()
    data = d.get_url_status_code_count(limit=parse_limit(limit))
    if request.args.get('show') and data.any():
        dd = DataDisplay()
        dd.show_graphic(data, kind, use_index)
    return data.to_frame().to_json(orient='index')


@app.route('/ip_status_code_count_graphic', methods=['GET'])
def ip_status_code_count_graphic():
    error, kind, limit, use_index = parse_requests(request)
    if error:
        return error

    d = DataCore()
    d.generate_data()
    data = d.get_ip_status_code_count(limit=parse_limit(limit))
    if request.args.get('show') and data.any():
        dd = DataDisplay()
        dd.show_graphic(data, kind, use_index)
    return data.to_frame().to_json(orient='index')


if __name__ == '__main__':
    app.run()

