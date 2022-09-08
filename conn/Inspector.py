"""
督查用来检测环境是否正常
"""
import os

from conn.gheaders.conn import read_yaml

yml = read_yaml()


class Check:
    def __int__(self):
        pass

    def cpath(self):
        """
        检测环境是否存在，不存在返回-1
        :return: -1 or 0
        """
        tf = 0
        qlpath = os.path.isfile(yml['qlpath'])
        db = os.path.isfile(yml['db'])

        if not qlpath:
            print("青龙配置文件填写错误")
            tf = -1
        if not db:
            print("请填写正确的数据库文件")
            tf = -1
        return tf


