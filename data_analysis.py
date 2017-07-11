# -*- coding: utf-8 -*-
# !/usr/bin/env python

__author__ = 'berniey'


class DataAnalysisMethod(object):

    @staticmethod
    def url_traffic(datacore, *args, **kwargs):
        return datacore.groupby('url').sum()['TrafficSize'].sort_values(*args, **kwargs)

    @staticmethod
    def url_count(datacore, ascending):
        return datacore['url'].value_counts(ascending)

