# -*- coding: utf-8 -*-
# !/usr/bin/env python

__author__ = 'berniey'


class DataAnalysisMethod(object):

    @staticmethod
    def url_traffic(datacore, *args, **kwargs):
        if kwargs.get('limit'):
            limit = kwargs.get('limit')
        return datacore.groupby('url').sum()['TrafficSize'].sort_values(*args, **kwargs)[0:10]

    @staticmethod
    def url_count(datacore, *args, **kwargs):
        return datacore['url'].value_counts(*args, **kwargs).rename('count')

    @staticmethod
    def ip_traffic(datacore, *args, **kwargs):
        return datacore.groupby('ip').sum()['TrafficSize'].sort_values(*args, **kwargs)[0:100]

    @staticmethod
    def ip_count(datacore, *args, **kwargs):
        return datacore['ip'].value_counts(*args, **kwargs)[0:100]

    @staticmethod
    def total_status_code_count(datacore, *args, **kwargs):
        return datacore['StatusCode'].value_counts(*args, **kwargs)[0:100]

    @staticmethod
    def ip_url_status_code_count(datacore, *args, **kwargs):
        return datacore.groupby(['ip', 'url'])['StatusCode'].value_counts(*args, **kwargs)[0:100]

    @staticmethod
    def url_status_code_count(datacore, *args, **kwargs):
        return datacore.groupby('url')['StatusCode'].value_counts(*args, **kwargs)[0:100]

    @staticmethod
    def ip_status_code_count(datacore, *args, **kwargs):
        return datacore.groupby('ip')['StatusCode'].value_counts(*args, **kwargs)[0:100]











