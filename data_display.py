# -*- coding: utf-8 -*-
# !/usr/bin/env python

__author__ = 'berniey'


import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from util import traffic_decimal
from data import DataCore

class DataDisplay(object):

    def __init__(self, data):
        self.data = data

    def _construct_figure_for_url_traffic(self, figsize=(12,7), *args, **kwargs):
        self.fig, self.ax0= plt.subplots(figsize=figsize)
        print(self.ax0)
        plt.subplots_adjust(*args, **kwargs)

    def _construct_axes_for_url_traffic(self):
        # 坐标轴
        self.ax0.set_xlim([0, 10 ** len(str(self.data.url_traffic_data.max()))])

        # 设置title和label
        self.ax0.set(title='QiNiu CDN', xlabel='CDN Traffic', ylabel='U R L')

        # 添加一条显示平均数的辅助线
        avg = self.data.url_traffic_data.mean()
        self.ax0.axvline(x=avg, color='c', label='Average', linestyle='--', linewidth=1)

        # 函数，改变x轴的单位
        formatter = FuncFormatter(traffic_decimal)
        self.ax0.xaxis.set_major_formatter(formatter)
        self.data.url_traffic_data.plot(kind='barh', y="Traffic", x="URL", ax=self.ax0)

    def show_url_traffic_graphic(self):
        self._construct_figure_for_url_traffic(left=0.4)
        self._construct_axes_for_url_traffic()
        plt.show()


if __name__ == '__main__':
    d = DataCore()
    d.generate_data()
    d.get_url_traffic_data()
    a= (d.url_traffic_data)
    print(a.to_json(orient='split'))

    dd = DataDisplay(d)

    dd.show_url_traffic_graphic()


    import requests