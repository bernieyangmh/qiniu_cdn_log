# -*- coding: utf-8 -*-
# !/usr/bin/env python

__author__ = 'berniey'

import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from util import traffic_decimal, singleton
from data import DataCore


@singleton
class DataDisplay(object):

    def __init__(self):
        pass

    def show_graphic(self, data, kind, use_index, xlabel, ylabel, line_color,
                     fig_color, funciton, x_str, y_str, title, figsize, dis_tick):
        self._drawing(data, kind, use_index, xlabel, ylabel, line_color,
                      fig_color, funciton, x_str, y_str, title, figsize, dis_tick)

    def _drawing(self, data, kind, use_index, xlabel, ylabel, line_color,
                 fig_color, funciton, x_str, y_str, title, figsize, dis_tick):
        self._construct_figure(kind, figsize=figsize)
        if kind in ['bar', 'barh'] and isinstance(data, pd.core.frame.Series):
            self._construct_guideline_avg(data, color=line_color)
        self._construct_axe(data, funciton, kind)

        self._chose_graphic_kind(data, kind=kind, use_index=use_index, xlabel=xlabel,
                                 ylabel=ylabel, color=fig_color,
                                 x_str=x_str, y_str=y_str, title=title
                                 )
        self._ticks(dis_tick)
        plt.show()

    def _construct_figure(self, kind, figsize):
        # 创建一个figure 和一个ax
        self.fig, self.ax0 = plt.subplots(figsize=figsize)
        if kind == 'pie':
            plt.subplots_adjust(left=0.45)
        plt.subplots_adjust()

    def _construct_axe(self, data, funciton, kind):
        # 坐标轴的长度
        # 对于dateFrame，max返回的是series，值为第二个
        if isinstance(data, pd.core.frame.DataFrame):
            self.ax0.set_xlim([0, int(1.2 * (data.max().values[1]))])
        else:
            self.ax0.set_xlim([0, int(1.2 * (data.max()))])

        # 函数，改变x轴的单位
        if funciton:
            formatter = FuncFormatter(funciton)
            if kind == 'barh':
                self.ax0.xaxis.set_major_formatter(formatter)
            else:
                self.ax0.yaxis.set_major_formatter(formatter)

    def _chose_graphic_kind(self, data, kind, use_index, xlabel, ylabel, color, x_str, y_str, title):
        self.ax0.set(title=title, xlabel=xlabel, ylabel=ylabel)
        if kind == 'pie':
            data.plot(kind=kind, ax=self.ax0, use_index=use_index, fontsize=10, secondary_y=False)
        else:
            data.plot(kind=kind, color=color, ax=self.ax0, use_index=use_index, fontsize=10, secondary_y=False)

    @staticmethod
    def _ticks(dis_tick):
        # 刻度相关的操作
        if dis_tick:
            eval('plt.{}ticks([])'.format(dis_tick))

    def _construct_guideline_avg(self, data, color):
        # 添加一条显示平均数的辅助线
        avg = data.mean()
        self.ax0.axvline(x=avg, color=color, label='Average', linestyle='--', linewidth=1)



if __name__ == '__main__':
    d = DataCore()
    d.generate_data()
    d.get_url_traffic_data()
    dd = DataDisplay(d)
