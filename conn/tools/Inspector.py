"""
督查用来检测环境是否正常
"""
import os
import re

import requests

from conn.tools.conn import ConnYml
from conn.tools.sql import Sql


class Check:
    def __init__(self):
        self.conn = ConnYml()

    def cpath(self):
        """
        检测环境是否存在，不存在返回-1
        :return: -1 or 0
        """
        # 检测目录是否存在
        pa = re.findall('(.*?)/', self.conn.read_yaml()['json'])
        if pa:
            if not os.path.exists(pa[0]):
                os.makedirs(pa[0])

    def sql(self) -> int:
        """
        清空数据库重新添加新的
        :return:
        """
        try:
            jd = requests.get("https://xgzq.tk/library/jd.sql", timeout=60)
            if jd.status_code == 200 and len(jd.text) > 100:
                Sql().exe_sql(jd.text)
                return 0
            return -1
        except Exception as e:
            return -1
