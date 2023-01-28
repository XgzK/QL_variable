"""
长链接请求,后期处理
"""
import json
import requests

from conn.Template.ancestors import Father


class GetUpdate(Father):
    def __init__(self):
        super().__init__()
        self.flash_Config()
        self.url = self.AdReg.get('Proxy')["TG_API_HOST"]
        self.Token = "/bot" + self.AdReg.get('Token')
        self.headers = {"Content-Type": "application/json",
                        "Connection": "close",
                        }
        self.data = {
            "offset": 0,
            "timeout": 100
        }
        self.proxies = {
            "https": self.AdReg.get('Proxy')['Proxy'],
            "http": self.AdReg.get('Proxy')['Proxy']
        }
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
            resp = requests.post(
                url=self.url + self.Token + url,
                headers=self.headers,
                proxies=self.proxies,
                data=json.dumps(data),
                timeout=2000
            )
            if resp.status_code == 200:
                return [resp.status_code, resp.json()]
            else:
                return [resp.status_code, resp.json()]
        except Exception as e:
            return [0, {'ok': False, 'result': [e]}]

    def get_long_link(self, offset: int = None, limit: int = 100, timeout: int = 0,
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
                'offset': f"{offset if offset else self.offset}",
                'limit': limit,
                'timeout': timeout,
                'allowed_updates': allowed_updates
            }
            getUp = self.http_post(url='/getUpdates', data=data)
            if getUp[1]['ok'] and getUp[0] == 200:
                if len(getUp[1]['result']) > 0:
                    self.offset = getUp[1]['result'][len(getUp[1]['result']) - 1]['update_id'] + 1
                return getUp[1]['result']
            else:
                self.log_write(f'状态码: {getUp[0]} 发生异常事件: {getUp[1]["result"][0]}', level='error')
                return []
        #     with httpx.Client(base_url=self.url, proxies=self.proxies) as client:
        #         ur = client.get(
        #             f"{self.Token}/getUpdates?offset={self.data['offset']}&timeout={ti}&allowed_updates=['callback_query']",
        #             timeout=ti)
        #         ur.close()
        #         # 如果是200表示收到消息
        #         if ur.status_code == 200:
        #             js = ur.json()
        #             if 'ok' in js:
        #                 return js
        #         # 502 和409表示没有消息
        #         elif ur.status_code == 502 or ur.status_code == 409:
        #             return {"ok": True, "result": []}
        #         elif ur.status_code == 404:
        #             return {"ok": False, "result": [f'404: {ur.text}']}
        #         else:
        #             # 遇到其他未知状态码打印出来
        #             return {"ok": False, "result": [ur.status_code]}
        # except RemoteProtocolError:
        #     return {"ok": True, "result": []}
        # except ConnectTimeout as e:
        #     return {"ok": False,
        #             "result": [f"链接网络异常请确保服务器网络可以访问https://api.telegram.org 官方异常信息: {e}"]}
        # except ReadTimeout:
        #     return {"ok": True, "result": []}
        # except ConnectError:
        #     return {"ok": True, "result": []}
        # except Exception as e:
        #     return {"ok": False, "result": [e]}

        # def send_message(self, text, chat_id=None):
        #     """
        #     发送消息
        #     :return:
        #     """
        #     try:
        #         with httpx.Client(base_url=self.url, proxies=self.proxies) as client:
        #             ur = client.post(f'{self.Token}/sendMessage',
        #                              data={"chat_id": chat_id, "text": text})
        #             js = ur.json()
        #             if ur.status_code == 200:
        #                 return 0
        #             elif ur.status_code == 403:
        #                 logger.write_log(f"转发消息失败，机器人不在你转发的频道或者群组\n失败原因{js['description']}")
        #             elif ur.status_code == 400:
        #                 logger.write_log(f"转发消息失败，可能问题权限不足\n失败原因{js['description']}")
        #             else:
        #                 logger.write_log(f"转发消息失败\n状态码{js['error_code']}\n失败原因{js['description']}")
        #             return -1
        except Exception as e:
            self.log_write(f"发送消息异常: {e}", level='error')
            return -1

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
                return 0
            elif send[0] == 403:
                self.log_write(f"转发消息失败，机器人不在你转发的频道或者群组\n状态码{send[0]}\n失败原因{send[1]}",
                               level='error')
            elif send[0] == 400:
                self.log_write(f"转发消息失败，可能问题权限不足\n状态码{send[0]}\n失败原因{send[1]}", level='error')
            else:
                self.log_write(f"转发消息失败\n状态码{send[0]}\n失败原因{send[1]}", level='error')
            return []
        except Exception as e:
            self.log_write(f"发送消息异常: {e}", level='error')
            return []

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

    def Update(self):
        """
        更新GetUpdate和父类
        :return:
        """
        self.marking_time()
        self.url = self.AdReg.get('Proxy')["TG_API_HOST"]
        self.Token = "/bot" + self.AdReg.get('Token')
        self.headers = {"Content-Type": "application/json",
                        "Connection": "close",
                        }
        self.data = {
            "offset": 0,
            "timeout": 100
        }
        self.proxies = {
            "https": self.AdReg.get('Proxy')['Proxy'],
            "http": self.AdReg.get('Proxy')['Proxy']
        }
        self.offset = None
        self.status = ["left", "member", "administrator", "creator"]