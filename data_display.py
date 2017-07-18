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

    def __init__(self, datacare):
        self.datacare = datacare

    def _construct_figure_for_url_traffic_for_example(self, figsize=(12,7), *args, **kwargs):
        self.fig, self.ax0= plt.subplots(figsize=figsize)
        plt.subplots_adjust(*args, **kwargs)

    def _construct_axes_for_url_traffic_barh_example(self):
        # 坐标轴
        self.ax0.set_xlim([0, 10 ** len(str(self.datacare.get_url_traffic_data().max()))])

        # 设置title和label
        self.ax0.set(title='QiNiu CDN', xlabel='CDN Traffic', ylabel='U R L')

        # 添加一条显示平均数的辅助线
        avg = self.datacare.get_url_traffic_data().mean()
        self.ax0.axvline(x=avg, color='c', label='Average', linestyle='--', linewidth=1)

        # 函数，改变x轴的单位
        formatter = FuncFormatter(traffic_decimal)
        self.ax0.xaxis.set_major_formatter(formatter)
        self.datacare.get_url_traffic_data().plot(kind='barh', y="Traffic", x="URL", ax=self.ax0)

    def _drawing(self, data, use_index, x_str, y_str, title, kind, figsize, xlabel, ylabel, line_color='r', fig_color='b', funciton=None, *args, **kwargs):
        self._construct_figure(figsize, *args, **kwargs)
        self._construct_guideline_avg(data, color=line_color)
        self._construct_axe(data, funciton)
        self._chose_graphic_kind(data, kind, use_index, xlabel=xlabel, ylabel=ylabel, color=fig_color, x_str=x_str, y_str=y_str, title=title)
        plt.show()

    def _construct_figure(self, figsize, *args, **kwargs):
        self.fig, self.ax0 = plt.subplots(figsize=figsize)
        plt.subplots_adjust(*args, **kwargs)

    def _construct_guideline_avg(self, data, color):
        # 添加一条显示平均数的辅助线
        avg = data.mean()
        self.ax0.axvline(x=avg, color=color, label='Average', linestyle='--', linewidth=1)

    def _construct_axe(self, data, funciton):
        # 坐标轴的长度
        self.ax0.set_xlim([0, 10 ** len(str(data.max()))])
        # 设置title和label

        # 函数，改变x轴的单位
        if funciton:
            # formatter = FuncFormatter(traffic_decimal)
            formatter = FuncFormatter(funciton)
            self.ax0.xaxis.set_major_formatter(formatter)

    def _chose_graphic_kind(self, data, use_index, kind, xlabel, ylabel, color, x_str, y_str, title):
        self.ax0.set(title=title, xlabel=xlabel, ylabel=ylabel)
        data.plot(kind=kind, color=color, ax=self.ax0, use_index=use_index, fontsize=10, secondary_y=False)

    def show_url_traffic_graphic_barh(self):
        self._construct_figure_for_url_traffic_for_example(left=0.4)
        self._construct_axes_for_url_traffic_barh_example()
        plt.show()

    def show_graphic(self, data, use_index, kind='line', x_str='aaa', y_str='Traffic', title='QiNiu CDN',
                                 figsize=(12, 7), *args, **kwargs):
        self._drawing(data, use_index, x_str, y_str, title, kind, figsize, xlabel='CDN Traffic', ylabel='url',
                      line_color='r', fig_color='b', *args, **kwargs)



if __name__ == '__main__':
    d = DataCore()
    d.generate_data()
    d.get_url_traffic_data()
    dd = DataDisplay(d)
