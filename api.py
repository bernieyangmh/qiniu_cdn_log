# -*- coding: utf-8 -*-
# !/usr/bin/env python

__author__ = 'bernie'

from flask import Flask, jsonify, request
from data import DataCore
from data_display import DataDisplay

app = Flask(__name__)

api_list = {
    '/show_url_traffic_data': u'''show all url's traffic''',
}


def generate_datacore():
    return DataCore().generate_data()


@app.route('/')
def index():
    return jsonify(api_list)


@app.route('/show_url_traffic_data')
def show_url_traffic_data():
    d = generate_datacore()
    d.generate_data()
    d.get_url_traffic_data(ascending=False)
    return d.url_traffic_data.to_json(orient='split')


@app.route('/show_url_traffic_graphic')
def show_url_traffic_graphic():
    d = generate_datacore()
    d.get_url_traffic_data()
    dd = DataDisplay(d)
    dd.show_url_traffic_graphic()
    return "look python graphic"


if __name__ == '__main__':
    app.run()

