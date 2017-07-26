# -*- coding: utf-8 -*-
# !/usr/bin/env python

from config import GetConfig

import pandas as pd
from util import singleton, convert_time_format
from data_analysis import DataAnalysisMethod
from util import parse_limit

__author__ = 'berniey'


@singleton
class DataCore(object):

    def __init__(self, chunksize=10000000):
        # one size of chunk
        self.chunk_size = chunksize
        self.chunks = []
        self.data = None
        self.files = self._get_files()

    def generate_data(self, is_qiniu='True'):
        self._get_chunks()
        if (self.chunks or self.data) or isinstance(self.data, pd.core.frame.DataFrame):
            self.data = self._aggregate_data(self.chunks)
            if is_qiniu != 'f':
                self._change_data(self.data)
            self.chunks = []
            return self.data

    def get_url_traffic(self, *args, **kwargs):
        return self._set_url_traffic_data(*args, **kwargs)

    def get_url_count(self, *args, **kwargs):
        return self._set_url_count_data(*args, **kwargs)

    def get_ip_traffic(self, *args, **kwargs):
        return self._set_ip_traffic_data(*args, **kwargs)

    def get_ip_count(self, *args, **kwargs):
        return self._set_ip_count_data(*args, **kwargs)

    def get_code_count(self, *args, **kwargs):
        return self._set_code_count(*args, **kwargs)

    def get_ip_url_code_count(self, *args, **kwargs):
        return self._set_ip_url_code_count(*args, **kwargs)

    def get_url_code_count(self, *args, **kwargs):
        return self._set_url_code_count(*args, **kwargs)

    def get_ip_code_count(self, *args, **kwargs):
        return self._set_ip_code_count(*args, **kwargs)

    def get_time_traffic(self, *args, **kwargs):
        return self._set_time_traffic(*args, **kwargs)

    def get_time_count(self, *args, **kwargs):
        return self._set_time_count(*args, **kwargs)

    def get_data_by_factor(self, *args, **kwargs):
        return self._set_data_by_factor(*args, **kwargs)

    def _set_url_traffic_data(self, *args, **kwargs):
        return DataAnalysisMethod.url_traffic(self.data, *args, **kwargs)

    def _set_url_count_data(self, *args, **kwargs):
        return DataAnalysisMethod.url_count(self.data, *args, **kwargs)

    def _set_ip_traffic_data(self, *args, **kwargs):
        return DataAnalysisMethod.ip_traffic(self.data, *args, **kwargs)

    def _set_ip_count_data(self, *args, **kwargs):
        return DataAnalysisMethod.ip_count(self.data, *args, **kwargs)

    def _set_code_count(self, *args, **kwargs):
        return DataAnalysisMethod.code_count(self.data, *args, **kwargs)

    def _set_ip_url_code_count(self, *args, **kwargs):
        return DataAnalysisMethod.ip_url_code_count(self.data, *args, **kwargs)

    def _set_url_code_count(self, *args, **kwargs):
        return DataAnalysisMethod.url_code_count(self.data, *args, **kwargs)

    def _set_ip_code_count(self, *args, **kwargs):
        return DataAnalysisMethod.ip_code_count(self.data, *args, **kwargs)

    def _set_time_traffic(self, *args, **kwargs):
        return DataAnalysisMethod.time_traffic(self.data, *args, **kwargs)

    def _set_time_count(self, *args, **kwargs):
        return DataAnalysisMethod.time_count(self.data, *args, **kwargs)

    def _set_data_by_factor(self, *args, **kwargs):
        return DataAnalysisMethod.data_by_factor(self.data, *args, **kwargs)

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

        dd.rename(columns={0: "ip", 1: "hit", 2: 'response_time', 3: 'request_time', 'z': 'method',
                           'y': 'url', 'x': 'Protocol', 6: 'StatusCode', 7: 'TrafficSize',
                           8: 'referer', 9: 'UserAgent'}, inplace=True)

        ddd = dd['request_time'].apply(convert_time_format)
        dd['request_time'] = ddd
        self.data = dd


if __name__ == '__main__':
    d = DataCore()
    d.generate_data()
    print(d.get_data_by_factor(limit=parse_limit(':10')))

