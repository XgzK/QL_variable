"""
用于处理用户一些指令的
"""
import re

from . import tg_mes
from ..gheaders import logger
from ..gheaders.conn import read_yaml, revise_yaml
from ..ql.ql_timing import Timing
from ..sql import conn


class Interact:
    def __init__(self):
        self.conn = conn
        self.yml = read_yaml()
        self.timing =  Timing()

    def get_id(self, result):
        """
        用户如果转发频道消息给机器人返回频道ID
        :return:
        """
        try:
            if len(str(self.yml['Administrator'])) == 0 or int(self.yml['Administrator']) != int(
                    result['message']['from']['id']):
                logger.write_log(f"没有设置 Administrator 或 不是机器人主人无法交互 ID: {result['message']['from']['id']}")
                return
            # forward_from_chat 只有转发的消息才携带
            if 'forward_from_chat' in result['message']:
                tx = f"{'你的个人ID是: ' + str(result['message']['from']['id'])}\n" \
                     f"{'用户名: ' + result['message']['from']['first_name'] if 'first_name' in result['message']['from'] else ''} {result['message']['from']['last_name'] if 'last_name' in result['message']['from'] else ' '}\n" \
                     f"个人链接: @{result['message']['from']['username'] if 'username' in result['message']['from'] else ''}\n" \
                     f"{'转发频道名称: ' + result['message']['forward_from_chat']['title'] if 'title' in result['message']['forward_from_chat'] else ''}\n" \
                     f"{'转发频道ID: ' + str(result['message']['forward_from_chat']['id']) if 'id' in result['message']['forward_from_chat'] else ''}\n" \
                     f"{'频道链接: @' + result['message']['forward_from_chat']['username'] if 'username' in result['message']['forward_from_chat'] else ''}"
                for i in range(4):
                    tg_mes.send_message(tx, result['message']['from']['id'])
                    return
            else:
                idfor = re.findall('/forward ([0-9-]+)', result['message']['text'])
                if idfor:
                    return revise_yaml(f'Send_IDs: {idfor[0]}', self.yml['Record']['Send_IDs'])
                add_js = re.findall('/prohibit ([0-9a-zA-Z_\.]+)', result['message']['text'])
                if add_js:
                    return revise_yaml(f'prohibit: {read_yaml()["prohibit"] + add_js}', self.yml['Record']['prohibit'])
                quit = re.findall('/quit (.*)', result['message']['text'])
                # 退出群聊
                if quit:
                    return tg_mes.leaveChat(quit[0])
                putk = re.findall("/putk (.*)", result['message']['text'])
                if putk:
                    puts = putk[0].split("@")
                    st = re.findall('^(http.*:\d+)', puts[1]) if len(puts) == 4 else False
                    if st:
                        inst = self.conn.insert(table=conn.surface[3], name=f"{puts[0]}", ip=f"{st[0]}",
                                                Client_ID=f"{puts[2]}", Client_Secret=f"{puts[3]}", Authorization="",
                                                json=f"{self.yml['json']}{puts[0]}.json", state=1)
                        if inst > 0:
                            return tg_mes.send_message(f"提交 {puts[0]} 成功", self.yml['Administrator'])
                        elif inst == -1:
                            return tg_mes.send_message(f"提交 {puts[0]} 失败,提交的内容和之前提交的内容冲突",
                                                       self.yml['Administrator'])
                        else:
                            return tg_mes.send_message(f"提交 {puts[0]} 失败,失败原因: {inst}",
                                                       self.yml['Administrator'])
                    else:
                        return tg_mes.send_message(f"提交{puts[0]}失败", self.yml['Administrator'])
                start = re.findall("/start", result['message']['text'])
                # 启动青龙
                if start:
                    lis1 = self.timing.check_ct(1)
                    list2 = self.timing.clear_list()
                    tg_mes.send_message(f"{lis1}\n{list2}\n执行异常已经被删除", self.yml['Administrator']) if lis1 else ""
        except Exception as e:
            print('私聊方法异常', e)

    def distribute(self, result, ids):
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
