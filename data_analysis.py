# -*- coding: utf-8 -*-
# !/usr/bin/env python

__author__ = 'berniey'

from util import data_after_argument

class DataAnalysisMethod(object):

    @staticmethod
    def url_traffic(datacore, *args, **kwargs):
        aim_data = datacore.groupby('url').sum()['TrafficSize'].sort_values(ascending=False)
        return data_after_argument(aim_data, *args, **kwargs)

    @staticmethod
    def url_count(datacore, *args, **kwargs):
        aim_data = datacore['url'].value_counts().rename('count')
        return data_after_argument(aim_data, *args, **kwargs)

    @staticmethod
    def ip_traffic(datacore, *args, **kwargs):
        aim_data = datacore.groupby('ip').sum()['TrafficSize'].sort_values()
        return data_after_argument(aim_data, *args, **kwargs)

    @staticmethod
    def ip_count(datacore, *args, **kwargs):
        aim_data = datacore['ip'].value_counts()
        return data_after_argument(aim_data, *args, **kwargs)

    @staticmethod
    def total_status_code_count(datacore, *args, **kwargs):
        aim_data = datacore['StatusCode'].value_counts()
        return data_after_argument(aim_data, *args, **kwargs)

    @staticmethod
    def ip_url_status_code_count(datacore, *args, **kwargs):
        aim_data = datacore.groupby(['ip', 'url'])['StatusCode'].value_counts()
        return data_after_argument(aim_data, *args, **kwargs)

    @staticmethod
    def url_status_code_count(datacore, *args, **kwargs):
        aim_data = datacore.groupby('url')['StatusCode'].value_counts()
        return data_after_argument(aim_data, *args, **kwargs)

    @staticmethod
    def ip_status_code_count(datacore, *args, **kwargs):
        aim_data = datacore.groupby('ip')['StatusCode'].value_counts()
        return data_after_argument(aim_data, *args, **kwargs)











