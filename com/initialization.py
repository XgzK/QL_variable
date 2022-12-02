"""
初始化
"""
import requests

from com.sql import Sql


class Implement:

    def __init__(self):
        self.conn = Sql()

    def sql(self) -> int:
        """
        清空数据库重新添加新的
        :return:
        """
        try:
            # jd = requests.get("", timeout=60)
            # if jd.status_code == 200 and len(jd.text) > 100:
            #     self.conn.exe_sql(jd.text)
            #     return 0
            return -1
        except Exception as e:
            return -1