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
            elif "forward_from_chat" in message:
                # 转发消息
                self.forward_from_chat(message)
                return
            else:
                self.sorting.dispatch(message['text'])

        elif 'text' in message:
            if message['text'].startswith('/'):
                if message['text'] == "/id":
                    self.group_id(message)
            else:
                self.sorting.dispatch(message['text'])
            # 群聊用户
            return

    def forward_from_chat(self, message):
        """
        处理转发的消息
        :param message:
        :return:
        """
        tx = f"{'你的个人ID是: ' + str(message['from']['id'])}\n" \
             f"{'用户名: ' + message['from']['first_name'] if 'first_name' in message['from'] else ''} {message['from']['last_name'] if 'last_name' in message['from'] else ' '}\n" \
             f"个人链接: @{message['from']['username'] if 'username' in message['from'] else ''}\n" \
             f"{'转发频道名称: ' + message['forward_from_chat']['title'] if 'title' in message['forward_from_chat'] else ''}\n" \
             f"{'转发频道ID: ' + str(message['forward_from_chat']['id']) if 'id' in message['forward_from_chat'] else ''}\n" \
             f"{'频道链接: @' + message['forward_from_chat']['username'] if 'username' in message['forward_from_chat'] else ''}"
        self.inter.for_message(tx, False)

    def group_id(self, message):
        """
        获取群聊ID
        :param message:
        :return:
        """
        tx = f"群组名称: {message['chat']['title']}\n" \
             f"群组ID: {message['chat']['id']}"
        self.inter.for_message(tx, False, message['chat']['id'])
