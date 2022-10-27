"""
长链接请求,后期处理
"""
import json
import re

import http.client
from com.gheaders.conn import read_yaml


class GetUpdate:
    def __init__(self):
        yml = read_yaml()
        self.url = ("https://api.telegram.org" if yml['TG_API_HOST'] == "" else yml['TG_API_HOST']) + "/bot" + yml[
            'Token']
        self.headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }
        self.data = {
            "offset": 0,
            "timeout": 100
        }

    def get_long_link(self):
        """
        长链接
        :return: 失败返回 {"ok": False,"result": []}
        """
        try:
            ur = re.findall("https://(.*?)(/.*)", self.url)
            if len(ur[0]) == 2:
                conn = http.client.HTTPSConnection(ur[0][0])
                conn.request("GET", f"{ur[0][1]}/getUpdates?offset={self.data['offset']}&timeout=100",
                             headers=self.headers)
                res = conn.getresponse()
                if res.status == 200:
                    data = res.read()
                    js = json.loads(data)
                    if 'ok' in js:
                        return js
                elif res.status == 502:
                    return {"ok": True, "result": []}
                else:
                    return {"ok": False, "result": [res.status]}
            return {"ok": False, "result": []}
        except Exception as e:
            return {"ok": False, "result": [e]}
