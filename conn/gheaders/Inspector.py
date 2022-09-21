"""
督查用来检测环境是否正常
"""
import os
import re

from conn.gheaders.conn import read_yaml
from conn.sql.addsql import create_db, create_table

yml = read_yaml()


class Check:
    def __int__(self):
        pass

    def cpath(self):
        """
        检测环境是否存在，不存在返回-1
        :return: -1 or 0
        """
        # 检测目录是否存在
        pa = re.findall('(.*?)/\w+\.\w+', yml['json'])
        if pa:
            if not os.path.exists(pa[0]):
                os.makedirs(pa[0])
        db = os.path.isfile(yml['repeat'])
        if not db:
            create_db()
            create_table()


