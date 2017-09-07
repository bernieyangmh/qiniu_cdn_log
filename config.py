# -*- coding: utf-8 -*-
# !/usr/bin/env python


import os
from configparser import ConfigParser

__author__ = 'berniey'


class LazyProperty(object):
    """
    LazyProperty
    explain: http://www.spiderpy.cn/blog/5/
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value


class ConfigParse(ConfigParser):
    """
    rewrite ConfigParser, for support upper option
    """

    def __init__(self):
        ConfigParser.__init__(self)

    def optionxform(self, optionstr):
        return optionstr


class GetConfig(object):
    """
    to get config like log's files or log's path from config.ini
    """

    def __init__(self, path=None):

        # self.config_path = os.path.join(os.path.split(self.pwd)[0], 'Config.ini')
        self._pwd = os.path.split(os.path.realpath(__file__))[0]
        if not path:
            self._config_path = self._pwd + '/Config.ini'
        else:
            self._config_path = path
        self._config_file = ConfigParse()
        self._config_file.read(self._config_path)

    @LazyProperty
    def _get_files(self):
        return list(self._config_file.get('log_files', 'file_path').split(','))

    @LazyProperty
    def _get_files_path(self):
        path = self._config_file.get('log_Path', 'log_path')
        if path:
            files_list = []
            for i in os.listdir(path):
                files_list.append(path+os.sep+i)
            return files_list

    def get_log(self):
        if self._get_files_path and self._get_files[0]:
            return self._get_files+self._get_files_path
        if self._get_files[0]:
            return self._get_files
        if self._get_files_path:
            return self._get_files_path


if __name__ == '__main__':
    g = GetConfig()
    print(g.get_log())
