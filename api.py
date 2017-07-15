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


def generate_datacore():
    return DataCore()


@app.route('/')
def index():
    return jsonify(api_list)


@app.route('/show_url_traffic_data')
def show_url_traffic_data():
    d = generate_datacore()
    d.generate_data()
    d.get_url_traffic_data(ascending=False)
    return d.url_traffic_data.to_json(orient='split')


@app.route('/show_url_traffic_graphic_barh')
def show_url_traffic_graphic_barh():
    d = generate_datacore()
    print(id(d))
    d.generate_data()
    d.get_url_traffic_data()
    dd = DataDisplay(d)
    dd.show_url_traffic_graphic_barh()
    return "look python graphic"


@app.route('/show_url_traffic_graphic', methods=['GET'])
def show_url_traffic_graphic():
    graphic_kinds = ['kde', 'bar', 'barh']
    kind = request.args.get('kind', 'bar')
    if kind not in graphic_kinds:
        return "you must have a choice among 'kde', 'bar' or 'barh' "
    d = generate_datacore()
    print(id(d))
    d.generate_data()
    d.get_url_traffic_data()
    dd = DataDisplay(d)
    dd.show_url_traffic_graphic(kind)
    return d.get_url_traffic_data().to_frame().to_json(orient='index')


if __name__ == '__main__':
    app.run()

