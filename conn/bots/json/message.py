import datetime

from conn.Template.ancestors import Father
from conn.bots.interaction import Interaction
from conn.mission.sorting import Sorting


class Message(Father):
    """
    接收到的消息
    """

    def __init__(self):
        super().__init__()
        self.sorting = Sorting()
        self.inter = Interaction()

    def filter_message(self, message):
        """
        获取发送的消息
        :param message:
        :return:
        """
        # 判断消息来源
        if message['chat']['type'] == 'private':
            # 私聊消息
            print(
                f"{datetime.datetime.now()} ID: {message['chat']['id']} {'用户: @' + message['chat']['username'] if 'username' in message['chat'] else ''} 用户名: {message['chat']['first_name'] if 'first_name' in message['chat'] else ''} {message['chat']['last_name'] if 'last_name' in message['chat'] else ''} 发送内容: {message['text']}")
            if message['text'].startswith('/'):
                if message['chat']['id'] == self.AdReg.get('Administrator'):
                    self.inter.main_white(message['text'])
                return
            else:
                self.sorting.dispatch(message['text'])

        else:
            self.sorting.dispatch(message['text'])
            # 群聊用户
            return print('这是个超级群聊或者私有群消息 ', message)
