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

    def _construct_figure_for_url_traffic_for_example(self, figsize=(12,7), *args, **kwargs):
        self.fig, self.ax0= plt.subplots(figsize=figsize)
        plt.subplots_adjust(*args, **kwargs)

    def _construct_axes_for_url_traffic_barh_example(self):
        # 坐标轴
        self.ax0.set_xlim([0, 10 ** len(str(self.data.get_url_traffic_data().max()))])

        # 设置title和label
        self.ax0.set(title='QiNiu CDN', xlabel='CDN Traffic', ylabel='U R L')

        # 添加一条显示平均数的辅助线
        avg = self.data.get_url_traffic_data().mean()
        self.ax0.axvline(x=avg, color='c', label='Average', linestyle='--', linewidth=1)

        # 函数，改变x轴的单位
        formatter = FuncFormatter(traffic_decimal)
        self.ax0.xaxis.set_major_formatter(formatter)
        self.data.get_url_traffic_data().plot(kind='barh', y="Traffic", x="URL", ax=self.ax0)

    def _drawing(self, figsize=(12,7), *args, **kwargs):
        self._construct_figure(*args, **kwargs)
        self._construct_guideline(*args, **kwargs)
        self._construct_axe(*args, **kwargs)

    def _construct_figure(self, *args, **kwargs):
        self.fig, self.ax0 = plt.subplots()
        plt.subplots_adjust(*args, **kwargs)

    def _construct_guideline(self,  *args, **kwargs):
        # 添加一条显示平均数的辅助线
        avg = self.data.url_traffic_data.mean()
        self.ax0.axvline(x=avg, *args, **kwargs)
        # self.ax0.axvline(x=avg, color='c', label='Average', linestyle='--', linewidth=1)

    def _construct_axe(self, funciton=None, *args, **kwargs):
        # 坐标轴的长度
        self.ax0.set_xlim([0, 10 ** len(str(self.data.url_traffic_data.max()))])

        # 设置title和label
        self.ax0.set(*args, **kwargs)
        # self.ax0.set(title=title, xlabel=xlabel, ylabel=ylabel)

        # 函数，改变x轴的单位
        if funciton:
            # formatter = FuncFormatter(traffic_decimal)
            formatter = FuncFormatter(funciton)
            self.ax0.xaxis.set_major_formatter(formatter)

    def _chose_graphic_kind(self, *args, **kwargs):
        # self.data.url_traffic_data.plot(kind='barh', y="Traffic", x="URL", ax=self.ax0)
        self.data.url_traffic_data.plot(ax=self.ax0, *args, **kwargs)

    def show_url_traffic_graphic_barh(self):
        self._construct_figure_for_url_traffic_for_example(left=0.4)
        self._construct_axes_for_url_traffic_barh_example()
        plt.show()

    def show_url_traffic_graphic_line(self, function=traffic_decimal, title='QiNiu CDN', xlabel='CDN Traffic', ylabel='Customer',
                                      kind='barh', y="Traffic", x="URL", color='c', label='Average', linestyle='--', linewidth=1, *args, **kwargs):
        self._drawing(*args, **kwargs)

    def show_url_traffic_graphic_bar(self):
        pass

    def show_url_traffic_graphic_area(self):
        pass

    def show_url_traffic_graphic_density(self):
        pass


if __name__ == '__main__':
    d = DataCore()
    d.generate_data()
    d.get_url_traffic_data()
    dd = DataDisplay(d)
