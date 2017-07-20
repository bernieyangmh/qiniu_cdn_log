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

    @staticmethod
    def time_traffic_count(datacore, *args, **kwargs):
        aim_data = datacore.groupby('request_time')['TrafficSize'].sum()
        return data_after_argument(aim_data, *args, **kwargs)


    @staticmethod
    def data_by_factor(datacore, *args, **kwargs):
        aim_data = datacore
        print(kwargs)
        if kwargs.get('status_code'):
            if str(kwargs['status_code'])[1:] == 'xx':
                aim_data = aim_data[(int(kwargs.get('status_code')[0])*100 <= aim_data.StatusCode)
                                    & (aim_data.StatusCode < (int(kwargs.get('status_code')[0])+1)*100)]
            else:
                aim_data = aim_data[aim_data.StatusCode == int(kwargs['status_code'])]
        if kwargs.get('url'):
            aim_data = aim_data[aim_data.url == kwargs.get('url')]
        if kwargs.get('ip'):
            aim_data = aim_data[aim_data.ip == kwargs.get('ip')]
        if kwargs.get('referer'):
            aim_data = aim_data[aim_data.referer == kwargs.get('referer')]
        return data_after_argument(aim_data, *args, **kwargs)








