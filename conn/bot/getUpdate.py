"""
长链接请求,后期处理
"""

import requests

from conn.gheaders.conn import read_yaml


class GetUpdate:
    def __init__(self):
        yml = read_yaml()
        self.url = ("https://api.telegram.org" if yml['TG_API_HOST'] == "" else yml['TG_API_HOST']) + "/bot" + yml['Token']
        self.headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }
        self.data = {
            "offset": None,
            "timeout": 100
        }

    def get_long_link(self):
        """
        长链接
        :return: 失败返回 {"ok": False,"result": []}
        """
        try:
            tg_me = requests.get(url=self.url + "/getUpdates", params=self.data, headers=self.headers)
            if tg_me.status_code == 200:
                return tg_me.json()
            else:
                return {"ok": False, "result": [tg_me.json()]}
        except Exception as e:
            return {"ok": False, "result": [e]}
