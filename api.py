# -*- coding: utf-8 -*-
# !/usr/bin/env python

__author__ = 'bernie'

from flask import Flask, jsonify, request
from data import DataCore
from data_display import DataDisplay
from util import traffic_decimal


app = Flask(__name__)

api_list = {
    '/show_url_traffic_data': u'''show all url's traffic''',
}


@app.route('/')
def index():
    return jsonify(api_list)


@app.route('/show_url_traffic_graphic', methods=['GET'])
def show_url_traffic_graphic():
    graphic_kinds = ['kde', 'bar', 'barh']
    kind = request.args.get('kind', 'bar')
    if kind not in graphic_kinds:
        return "you must have a choice among 'kde', 'bar' or 'barh' "
    use_index=request.args.get('use_index', True)

    d = DataCore()
    d.generate_data()
    data = d.get_url_traffic_data()
    dd = DataDisplay(d)
    dd.show_url_traffic_graphic(data, kind, use_index)
    return data.to_frame().to_json(orient='index')


@app.route('/show_url_count_graphic', methods=['GET'])
def show_url_count_graphic():
    graphic_kinds = ['line', 'hist', 'area']
    kind = request.args.get('kind', 'line')
    if kind not in graphic_kinds:
        return "you must have a choice among 'line','hist' or 'area'"
    use_index=request.args.get('use_index', True)

    d = DataCore()
    d.generate_data()
    data = d.get_url_count_data()
    dd = DataDisplay(d)
    dd.show_url_count_graphic(data, kind, use_index)
    return data.to_frame().to_json(orient='index')


@app.route('/show_ip_traffic_graphic', methods=['GET'])
def show_ip_traffic_graphic():
    graphic_kinds = ['line', 'hist', 'area', 'bar', 'barh']
    kind = request.args.get('kind', 'line')
    if kind not in graphic_kinds:
        return "you must have a choice among 'line','hist', 'bar', 'barh' or 'area'"
    use_index=request.args.get('use_index', True)
    if use_index == ('False' or 'false'):
        use_index = False

    d = DataCore()
    d.generate_data()
    data = d.get_ip_traffic_data()
    dd = DataDisplay(d)
    dd.show_ip_traffic_graphic(data, kind, use_index)
    return data.to_frame().to_json(orient='index')


@app.route('/show_ip_count_graphic', methods=['GET'])
def show_ip_count_graphic():
    graphic_kinds = ['line', 'hist', 'area', 'bar', 'barh', 'kde']
    kind = request.args.get('kind', 'line')
    if kind not in graphic_kinds:
        return "you must have a choice among 'line','hist', 'bar', 'barh', 'kde' or 'area'"
    use_index=request.args.get('use_index', True)
    if use_index == ('False' or 'false'):
        use_index = False

    d = DataCore()
    d.generate_data()
    data = d.get_ip_count_data()
    dd = DataDisplay(d)
    dd.show_ip_count_graphic(data, kind, use_index)
    return data.to_frame().to_json(orient='index')


if __name__ == '__main__':
    app.run()

