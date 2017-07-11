# -*- coding: utf-8 -*-
# !/usr/bin/env python

__author__ = 'berniey'


class DataAnalysisMethod(object):

    @staticmethod
    def url_traffic(datacore):
        return datacore.groupby('url').sum()['TrafficSize']

    @staticmethod
    def url_count(datacore):
        return datacore['url'].value_counts()

