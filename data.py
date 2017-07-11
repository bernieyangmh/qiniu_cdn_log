# -*- coding: utf-8 -*-
# !/usr/bin/env python

__author__ = 'berniey'

from config import GetConfig
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from util import SingletonMetaclass,singleton
from data_analysis import DataAnalysisMethod
from util import traffic_decimal

@singleton
class DataCore(object):

    def __init__(self, chunksize=10000000):
        # one size of chunk
        self.chunk_size = chunksize
        self.chunks = []
        self.data = None
        self.files = self._get_files()



    def generate_data(self):
        self._get_chunks()
        if self.chunks:
            self.data = self._aggregate_data(self.chunks)
            self._change_data(self.data)
            self.chunks = None
            return self.data

    def get_url_traffic_data(self, *args, **kwargs):
        return self._set_url_traffic_data(*args, **kwargs)

    def get_url_count_data(self, *args, **kwargs):
        return self._set_url_count_data(*args, **kwargs)

    def get_ip_traffic_data(self, *args, **kwargs):
        return self._set_ip_traffic_data(*args, **kwargs)

    def get_ip_count_data(self, *args, **kwargs):
        return self._set_ip_count_data(*args, **kwargs)

    def get_ip_url_traffic_count(self, *args, **kwargs):
        return self._set_ip_url_traffic_count(*args, **kwargs)

    def get_total_status_code_count(self, *args, **kwargs):
        return self._set_total_status_code_count(*args, **kwargs)

    def get_ip_url_status_code_count(self, *args, **kwargs):
        return self._set_ip_url_status_code_count(*args, **kwargs)

    def get_url_status_code_count(self, *args, **kwargs):
        return self._set_url_status_code_count(*args, **kwargs)

    def get_ip_status_code_count(self, *args, **kwargs):
        return self._set_ip_status_code_count(*args, **kwargs)

    def _set_url_traffic_data(self, *args, **kwargs):
        self.url_traffic_data = DataAnalysisMethod.url_traffic(self.data, *args, **kwargs)
        return self.url_traffic_data

    def _set_url_count_data(self, *args, **kwargs):
        self.url_count_data = DataAnalysisMethod.url_count(self.data, *args, **kwargs)
        return self.url_count_data

    def _set_ip_traffic_data(self, *args, **kwargs):
        self.ip_traffic_data = DataAnalysisMethod.ip_traffic(self.data, *args, **kwargs)
        return self.ip_traffic_data

    def _set_ip_count_data(self, *args, **kwargs):
        self.ip_count_data = DataAnalysisMethod.ip_count(self.data, *args, **kwargs)
        return self.ip_count_data

    def _set_ip_url_traffic_count(self, *args, **kwargs):
        self.ip_url_traffic_count = DataAnalysisMethod.ip_url_traffic_count(self.data, *args, **kwargs)
        return self.ip_url_traffic_count

    def _set_total_status_code_count(self, *args, **kwargs):
        self.total_status_code_count = DataAnalysisMethod.total_status_code_count(self.data, *args, **kwargs)
        return self.total_status_code_count

    def _set_ip_url_status_code_count(self, *args, **kwargs):
        self.ip_url_status_code_count = DataAnalysisMethod.ip_url_status_code_count(self.data, *args, **kwargs)
        return self.ip_url_status_code_count

    def _set_url_status_code_count(self, *args, **kwargs):
        self.url_status_code_count = DataAnalysisMethod.url_status_code_count(self.data, *args, **kwargs)
        return self.url_status_code_count

    def _set_ip_status_code_count(self, *args, **kwargs):
        self.ip_status_code_count = DataAnalysisMethod.ip_status_code_count(self.data, *args, **kwargs)
        return self.ip_status_code_count

    def _get_files(self):
        return GetConfig().get_log()

    def _get_chunks(self):
        for file in self.files:
            self._get_chunk_from_log(file)

    def _get_chunk_from_log(self, log):
        reader = pd.read_csv(log, sep='\s+', names=[i for i in range(10)], iterator=True)
        loop = True
        while loop:
            try:
                chunk = reader.get_chunk(self.chunk_size)
                self.chunks.append(chunk)
            except StopIteration:
                # Iteration is stopped.
                loop = False

    def _aggregate_data(self, chunks):
        return pd.concat(chunks, ignore_index=True)

    def _change_data(self, df):
        df[3] = df[3] + df[4]
        dx = pd.DataFrame(df[5].str.split(' ').tolist())
        df.drop([4, 5], axis=1, inplace=True)

        df.insert(4, 'z', dx[0])
        df.insert(5, 'y', dx[1])
        df.insert(6, 'x', dx[2])
        dd = pd.DataFrame(df)

        dd.rename(columns={0: "ip", 1: "hit", 2: 'response_time', 3: 'request_time', 'z': 'method', 'y': 'url',
                           'x': 'Protocol', 6: 'StatusCode', 7: 'TrafficSize', 8: 'referer', 9: 'UserAgent'
                           }, inplace=True)
        self.data = dd


if __name__ == '__main__':
    d = DataCore()
    d.generate_data()
    d.get_url_traffic_data()
    print(d.url_traffic_data)

