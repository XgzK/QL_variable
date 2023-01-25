"""
督查用来检测环境是否正常
"""
import os
import re

import requests

from com import father
from com.sql import Sql

sql = Sql()


class Check:
    def __init__(self):
        pass

    def cpath(self):
        """
        检测环境是否存在，不存在返回-1
        :return: -1 or 0
        """
        # 检测目录是否存在
        pa = re.findall('(.*?)/', father.AdReg.get('json'))
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
                sql.exe_sql(jd.text)
                return 0
            return -1
        except Exception as e:
            return -1
