# -*- coding: utf-8 -*-
# !/usr/bin/env python

__author__ = 'berniey'


class DataAnalysisMethod(object):

    @staticmethod
    def url_traffic(datacore, *args, **kwargs):
        print(datacore.groupby('url').sum()['TrafficSize'].sort_values(*args, **kwargs)[0:10])
        return datacore.groupby('url').sum()['TrafficSize'].sort_values(*args, **kwargs)[0:10]

    @staticmethod
    def url_count(datacore, *args, **kwargs):
        return datacore['url'].value_counts(*args, **kwargs)

    @staticmethod
    def ip_traffic(datacore, *args, **kwargs):
        return datacore.groupby('ip').sum()['TrafficSize'].sort_values(*args, **kwargs)

    @staticmethod
    def ip_count(datacore, *args, **kwargs):
        return datacore['ip'].value_counts()(*args, **kwargs)

    @staticmethod
    def ip_url_traffic_count(datacore, *args, **kwargs):
        return datacore.groupby(['ip', 'url'])['TrafficSize'].value_counts()(*args, **kwargs)

    @staticmethod
    def total_status_code_count(datacore, *args, **kwargs):
        return datacore['StatusCode'].value_counts()(*args, **kwargs)

    @staticmethod
    def ip_url_status_code_count(datacore, *args, **kwargs):
        return datacore.groupby(['ip', 'url'])['StatusCode'].value_counts()(*args, **kwargs)

    @staticmethod
    def url_status_code_count(datacore, *args, **kwargs):
        return datacore.groupby('url')['StatusCode'].value_counts()(*args, **kwargs)

    @staticmethod
    def ip_status_code_count(datacore, *args, **kwargs):
        return datacore.groupby('ip')['StatusCode'].value_counts()(*args, **kwargs)

    @staticmethod
    def url(datacore, *args, **kwargs):
        return datacore.groupby('url')










