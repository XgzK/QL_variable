"""
长链接请求,后期处理
"""

import httpx
from httpx import RemoteProtocolError, ConnectTimeout, ReadTimeout, ConnectError

from com.gheaders import logger
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

    def get_long_link(self, ti=100):
        """
        长链接
        :param ti: 最大请求时间
        :return: 失败返回 {"ok": False,"result": []}
        """
        try:
            client = httpx.Client(proxies=self.proxies, headers=self.headers)
            ur = client.post(f"{self.url}/getUpdates?offset={self.data['offset']}&timeout={ti}",
                             timeout=ti)
            ur.close()
            # 如果是200表示收到消息
            if ur.status_code == 200:
                js = ur.json()
                if 'ok' in js:
                    return js
            # 502 和409表示没有消息
            elif ur.status_code == 502 or ur.status_code == 409:
                return {"ok": True, "result": []}
            elif ur.status_code == 404:
                return {"ok": False, "result": [f'404: {ur.text}']}
            else:
                # 遇到其他未知状态码打印出来
                return {"ok": False, "result": [ur.status_code]}
        except RemoteProtocolError or ConnectTimeout or ReadTimeout:
            return {"ok": True, "result": []}
        except ConnectError as e:
            return {"ok": False, "result": [f'链接网络异常可能没有外网环境: {e}']}
        except Exception as e:
            return {"ok": False, "result": [e]}

    def send_message(self, tx, chat_id=None):
        """
        发送消息
        :return:
        """
        try:
            client = httpx.Client(proxies=self.proxies, headers=self.headers)
            ur = client.get(f"{self.url}/sendMessage?chat_id={chat_id if chat_id else self.Send_IDs}&text={tx}")
            js = ur.json()
            client.close()
            if ur.status_code == 200:
                return 0
            elif ur.status_code == 403:
                logger.write_log(f"转发消息失败，机器人不在你转发的频道或者群组\n失败原因{js['description']}")
            elif ur.status_code == 400:
                logger.write_log(f"转发消息失败，可能问题权限不足\n失败原因{js['description']}")
            else:
                logger.write_log(f"转发消息失败\n状态码{js['error_code']}\n失败原因{js['description']}")
            return -1
        except Exception as e:
            logger.write_log(f"发送消息异常: {e}")
            return -1
