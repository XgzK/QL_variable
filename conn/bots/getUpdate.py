"""
长链接请求,后期处理
"""
import json
import re

import requests
from requests import ConnectTimeout

from conn.Template.ancestors import Father


class GetUpdate(Father):
    def __init__(self):
        super().__init__()
        self.flash_Config()
        self.url = self.AdReg.get('Proxy')["TG_API_HOST"]
        self.Token = "/bot" + self.AdReg.get('Token')
        self.headers = {"Content-Type": "application/json",
                        "Connection": "close",
                        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
                        }
        self.data = {
            "offset": 0,
            "timeout": 100
        }
        self.proxies = self.AdReg.get('Proxy')['Proxy'] if self.AdReg.get('Proxy')['Proxy'] else None
        self.offset = None
        self.status = ["left", "member", "administrator", "creator"]

    def http_post(self, url, data):
        """
        发送请求
        :param url: /xxx
        :param data:
        :return:
        """
        try:
            if not re.findall('(/bot\w+)', self.Token):
                self.Update()
            resp = requests.post(url=self.url + self.Token + url, data=json.dumps(data), timeout=200, headers=self.headers, proxies={"https": self.proxies, "http": self.proxies})
            code = resp.status_code
            # 502 和409表示没有消息
            if code in [502, 409]:
                return [200, {"ok": True, "result": []}]
            elif code == 404:
                return [code, {"ok": False, "result": [f'404: {resp.text}']}]
            resp_js = resp.json()
            resp.close()
            if code == 200:
                return [code, resp_js]
            else:
                return [code, resp_js]
        except Exception as e:
            return [0, {'ok': False, 'result': [e]}]

    async def get_long_link(self, offset: int = None, limit: int = 100, timeout: int = 0,
                            allowed_updates: list = None):
        """
        长链接
        :param offset: Identifier of the first update to be returned. Must be greater by one than the highest among the identifiers of previously received updates. By default, updates starting with the earliest unconfirmed update are returned. An update is considered confirmed as soon as getUpdates is called with an offset higher than its update_id. The negative offset can be specified to retrieve updates starting from -offset update from the end of the updates queue. All previous updates will forgotten.
        :param limit: Limits the number of updates to be retrieved. Values between 1-100 are accepted. Defaults to 100.
        :param timeout: Timeout in seconds for long polling. Defaults to 0, i.e. usual short polling. Should be positive, short polling should be used for testing purposes only.
        :param allowed_updates: A JSON-serialized list of the update types you want your bot to receive. For example, specify [“message”, “edited_channel_post”, “callback_query”] to only receive updates of these types. See Update for a complete list of available update types. Specify an empty list to receive all update types except chat_member (default). If not specified, the previous setting will be used.

                Please note that this parameter doesn't affect updates created before the call to the getUpdates, so unwanted updates may be received for a short period of time.
        :return:
        """
        try:
            data = {
                'offset': self.offset,
                'limit': limit,
                'timeout': timeout,
                'allowed_updates': allowed_updates
            }
            resp = requests.post(url=self.url + self.Token + '/getUpdates', data=json.dumps(data),
                                 proxies={"https": self.proxies, "http": self.proxies}, headers=self.headers)
            code = resp.status_code
            # 502 和409表示没有消息
            if code in [502, 409]:
                return [200, {"ok": True, "result": []}]
            elif code == 404:
                return [code, {"ok": False, "result": [f'404: {resp.text}']}]
            resp_js = resp.json()
            resp.close()
            if code == 200:
                # return [code, resp_js]
                if resp_js['ok']:
                    if len(resp_js['result']) > 0:
                        self.offset = resp_js['result'][len(resp_js['result']) - 1]['update_id'] + 1
                    return resp_js['result']
                else:
                    self.log_write(
                        f'conn.bots.getUpdate.GetUpdate.get_long_link状态码: {code} 发生异常事件: {resp_js["result"][0]}',
                        level='error')
                    return []
            else:
                return []
        except ConnectTimeout as e:
            self.log_write(
                f"conn.bots.getUpdate.GetUpdate.get_long_link 异常: {e}, 连接超时请确保能使用代理或者反代或直连 进行使用",
                level='error')
            return []
        except Exception as e:
            self.log_write(f"conn.bots.getUpdate.GetUpdate.get_long_link 异常: {e}", level='error')
            return []

    def send_message(self, chat_id: str, text: str):
        """
        发送消息
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :param text: Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
        :return:
        """
        try:
            send = self.http_post('/sendMessage', {"chat_id": chat_id, "text": text})
            if send[0] == 200:
                return send[0]
            elif send[0] == 403:
                self.log_write(
                    f"conn.bots.getUpdate.GetUpdate.send_message转发消息失败，机器人不在你转发的频道或者群组\n状态码{send[0]}\n失败原因{send[1]}",
                    level='error')
                return send[0]
            elif send[0] == 400:
                self.log_write(
                    f"conn.bots.getUpdate.GetUpdate.send_message转发消息失败，可能问题权限不足\n状态码{send[0]}\n失败原因{send[1]}",
                    level='error')
                return send[0]
            else:
                self.log_write(
                    f"conn.bots.getUpdate.GetUpdate.send_message转发消息失败\n状态码{send[0]}\n失败原因{send[1]}",
                    level='error')
                return send[0]
        except Exception as e:
            self.log_write(f"conn.bots.getUpdate.GetUpdate.send_message发送消息异常: {e}", level='error')
            return [0]

    def banChatMember(self, chat_id, user_id):
        """
        踢出群聊
        :param chat_id: 群标识
        :param user_id: 踢出标识
        :return:
        """
        try:
            send = self.http_post('/banChatMember', {"chat_id": chat_id, "user_id": user_id})
            if send[0] == 200:
                return 0
            elif send[0] == 403:
                self.log_write(f"踢出群聊{send[0]}", level='error')
            elif send[0] == 400:
                self.log_write(f"踢出群聊失败，可能问题权限不足\n状态码{send[0]}\n失败原因{send[1]}", level='error')
            else:
                self.log_write(f"踢出群聊失败\n状态码{send[0]}\n失败原因{send[1]}", level='error')
            return []
        except Exception as e:
            self.log_write(f"踢出群聊异常: {e}", level='error')

    def getChatMember(self, chat_id, user_id):
        """
        获取用户是否再群组
        :param chat_id: 群标识
        :param user_id: 成员
        :return: json
        """
        try:
            send = self.http_post('/getChatMember', {"chat_id": chat_id, "user_id": user_id})
            if send[0] == 200:
                return send[1]['result']
            elif send[0] == 403:
                self.log_write(f"获取用户是否再群组 {send[0]} ", level='error')
            elif send[0] == 400:
                self.log_write(f"获取ID {user_id} 失败 状态码 {send[0]} \n失败原因 {send[1]}", level='error')
            else:
                self.log_write(f"获取ID {user_id} 失败 状态码 {send[0]} \n失败原因 {send[1]}", level='error')
            return []
        except Exception as e:
            self.log_write(f"获取用户是否再群组异常: {e}", level='error')

    def leaveChat(self, chat_id):
        """
        使用此方法让您的机器人离开组、超级组或频道。成功返回True
        :return:
        """
        try:
            ur = self.http_post(url='/leaveChat', data={"chat_id": chat_id})
            if ur[0] == 200:
                self.send_message(f"退出 {chat_id} 群聊成功", self.AdReg.get('Administrator'))
                return 0
            else:
                self.send_message(f"退出 {chat_id} 失败 失败原因 {ur[1]}", self.AdReg.get('Administrator'))
                return 400
        except Exception as e:
            return -1

    def getChat(self, chat_id) -> dict:
        """
        使用此方法根据ID获取群信息
        :return:
        """
        try:
            ur = self.http_post(url='/getChat', data={"chat_id": chat_id})
            if ur[0] == 200 and ur[0]['ok']:
                return ur[0]
            else:
                return ur[0]
        except Exception as e:
            return {
                "ok": False,
                "error_code": 500,
                "description": e
            }

    def Update(self):
        """
        更新GetUpdate和父类
        :return:
        """
        self.flash_Config()
        self.url = self.AdReg.get('Proxy')["TG_API_HOST"]
        self.Token = "/bot" + self.AdReg.get('Token')
        self.proxies = self.AdReg.get('Proxy')['Proxy'] if self.AdReg.get('Proxy')['Proxy'] else None
