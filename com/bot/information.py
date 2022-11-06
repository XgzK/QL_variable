"""
用于处理用户一些指令的
"""
from . import tg_mes


class Interact:
    def __init__(self):
        pass

    def get_id(self, result):
        """
        用户如果转发频道消息给机器人返回频道ID
        :return:
        """
        # forward_from_chat 只有转发的消息才携带
        if 'forward_from_chat' in result:
            tx = f"你的个人ID是: {result['from']['id']}\n" \
                 f"用户名: {result['from']['first_name']} {result['from']['last_name']}\n" \
                 f"个人链接: @{result['from']['username']}\n" \
                 f"下面是转发频道消息\n" \
                 f"转发频道名称: {result['forward_from_chat']['title']}\n" \
                 f"转发频道ID: {result['forward_from_chat']['id']}\n" \
                 f"频道链接: @{result['forward_from_chat']['username']}"
            tg_mes.send_message(tx, result['from']['id'])

    def distribute(self, result):
        """
        用于分配执行方法
        :param result:
        :return:
        """

    def group_id(self, result):
        """
        获取群聊ID
        :param result:
        :return:
        """
        print('ttttttttttttt')
        if result['message']['text'] == '/id':
            tx = f"群组名称: {result['message']['chat']['title']}\n" \
                 f"群组ID: {result['message']['chat']['id']}"
            print(result['message']['from'])
            tg_mes.send_message(tx, result['message']['from']['id'])
