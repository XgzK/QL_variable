"""
用于处理用户一些指令的
"""
import re

from . import tg_mes
from ..gheaders.conn import read_yaml, revise_yaml

yml = read_yaml()


class Interact:
    def __init__(self):
        pass

    def get_id(self, result):
        """
        用户如果转发频道消息给机器人返回频道ID
        :return:
        """
        try:
            # forward_from_chat 只有转发的消息才携带
            if 'forward_from_chat' in result['message']:
                tx = f"{'你的个人ID是: '+str(result['message']['from']['id'])}\n" \
                     f"{'用户名: '+result['message']['from']['first_name'] if 'first_name' in result['message']['from'] else ''} {result['message']['from']['last_name'] if 'last_name' in result['message']['from'] else ' '}\n" \
                     f"个人链接: @{result['message']['from']['username'] if 'username' in result['message']['from'] else ''}\n" \
                     f"{'转发频道名称: '+result['message']['forward_from_chat']['title'] if 'title' in result['message']['forward_from_chat'] else ''}\n" \
                     f"{'转发频道ID: '+str(result['message']['forward_from_chat']['id']) if 'id' in result['message']['forward_from_chat'] else ''}\n" \
                     f"{'频道链接: @' + result['message']['forward_from_chat']['username'] if 'username' in result['message']['forward_from_chat'] else ''}"
                for i in range(4):
                    tgid = tg_mes.send_message(tx, result['message']['from']['id'])
                    if tgid == 0:
                        return
            else:
                idfor = re.findall('/forward ([0-9-]+)', result['message']['text'])
                if idfor:
                    revise_yaml(f'Send_IDs: {idfor[0]}', yml['Record']['Send_IDs'])
                    return
                add_js = re.findall('/prohibit ([0-9a-zA-Z_\.]+)', result['message']['text'])
                if add_js:
                    ym = read_yaml()
                    revise_yaml(f'prohibit: {ym["prohibit"] + add_js}', ym['Record']['prohibit'])
                    return


        except Exception as e:
            print('私聊方法异常',e)

    def distribute(self, result,ids):
        """
        用于分配执行方法
        :param result:
        :return:
        """
        for i in range(4):
            tgid = tg_mes.send_message(result, ids)
            if tgid == 0:
                return

    def group_id(self, result):
        """
        获取群聊ID
        :param result:
        :return:
        """
        if result['message']['text'] == '/id':
            tx = f"群组名称: {result['message']['chat']['title']}\n" \
                 f"群组ID: {result['message']['chat']['id']}"
            for i in range(4):
                tgid = tg_mes.send_message(tx, result['message']['from']['id'])
                if tgid == 0:
                    return