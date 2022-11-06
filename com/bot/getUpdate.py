"""
长链接请求,后期处理
"""

import httpx
from httpx import RemoteProtocolError

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
        self.proxies = yml['Proxy'] if yml['Proxy'] else None
        self.Send_IDs = yml['Send_IDs']  # 要转发到群或者频道ID

    def get_long_link(self):
        """
        长链接
        :return: 失败返回 {"ok": False,"result": []}
        """
        try:
            ur = httpx.post(f"{self.url}/getUpdates?offset={self.data['offset']}&timeout=100",
                            headers=self.headers, timeout=100, proxies=self.proxies)
            # 如果是200表示收到消息
            if ur.status_code == 200:
                js = ur.json()
                if 'ok' in js:
                    return js
            # 502 和409表示没有消息
            elif ur.status_code == 502 or ur.status_code == 409:
                return {"ok": True, "result": []}
            else:
                # 遇到其他未知状态码打印出来
                return {"ok": False, "result": [ur.status_code]}
        except RemoteProtocolError:
            return {"ok": True, "result": []}
        except Exception as e:
            return {"ok": False, "result": [e]}

    def send_message(self, tx, chat_id=None):
        """
        发送消息
        :return:
        """
        try:
            ur = httpx.get(f"{self.url}/sendMessage?chat_id={chat_id if chat_id else self.Send_IDs}&text={tx}",
                            headers=self.headers, proxies=self.proxies)
            print(ur.url)
            # 如果是200表示收到消息
            if ur.status_code == 200:
                js = ur.json()
            else:
                pass
        except Exception as e:
            pass
