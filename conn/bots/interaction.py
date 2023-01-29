import os
import re
import time

from conn.bots.getUpdate import GetUpdate
from conn.ql.ql_timing import Timing
from conn.tools.sql import Sql


class Interaction(GetUpdate):
    def __init__(self):
        """
        机器人交互类
        """
        super().__init__()
        self.sql = Sql()
        self.timing = Timing()

    def main_white(self, text: str):
        """
        根据用户命令不同进行交互
        :return:
        """
        self.marking_time()
        # 把用户指令分为两种一种只有指令
        res = re.findall("^(/\w+)\s+([0-9a-zA-z_@:/.—-]+)", text)
        if res:
            if res[0][0] == "/forward":
                return self.from_forward(res[0][1])
            elif res[0][0] == "/prohibit":
                return self.from_prohibit(res[0][1])
            elif res[0][0] == "/quit":
                return self.from_quit(res[0][1])
            elif res[0][0] == "/putk":
                return self.from_putk(res[0][1])
            else:
                return
        res = re.findall("^(/\w+)$", text)
        if res:
            if res[0] == "/start":
                return self.start()
            else:
                return

    def for_message(self, texts: str, tf: bool = True, chat_id: str = None):
        """
        转发消息
        :param texts:
        :param tf: 默认转发到频道
        :param chat_id:
        :return:
        """
        self.marking_time()
        if chat_id:
            self.send_message(text=texts, chat_id=chat_id)
        elif tf and self.AdReg.get('Send_IDs'):
            self.send_message(text=texts, chat_id=self.AdReg.get('Send_IDs'))
        elif not tf and self.AdReg.get('Administrator'):
            self.send_message(text=texts, chat_id=self.AdReg.get('Administrator'))

    def from_forward(self, param):
        """
        提交转发频道或者群组
        :param param:
        :return:
        """
        self.revise_Config('Send_IDs', param)
        os.environ['marking_time'] = str(int(time.time()))

    def from_prohibit(self, param):
        """
        脚本加入黑名单
        :param param:
        :return:
        """
        self.revise_Config('prohibit', self.AdReg.get("prohibit").append(param))
        os.environ['marking_time'] = str(int(time.time()))

    def from_quit(self, param):
        """
        退出群聊或频道
        :param param:
        :return:
        """
        self.leaveChat(param)

    def from_putk(self, param: str):
        """
        提交青龙 别名@青龙URL@Client_ID@Client_Secre
        :param param:
        :return:
        """
        puts = param.split('@')
        if len(puts) != 4:
            return self.for_message("提交青龙参数不合法", False)
        st = re.findall('^(http.*:\d+)', puts[1])
        if st:
            inst = self.sql.insert(table=self.sql.surface[3], name=f"{puts[0]}", ip=f"{st[0]}",
                                   Client_ID=f"{puts[2]}", Client_Secret=f"{puts[3]}", Authorization="",
                                   json=f"{self.AdReg.get('json')}{puts[0]}.json", state=1)
            if inst > 0:
                return self.for_message(f"提交 {puts[0]} 成功", False)
            elif inst == -1:
                return self.for_message(f"提交 {puts[0]} 失败,提交的内容和之前提交的内容冲突",
                                        False)
            else:
                return self.for_message(f"提交 {puts[0]} 失败,失败原因: {inst}",
                                        False)

    def start(self):
        """
        初始化主动获取列表
        :return:
        """
        self.timing.check_ct(state=1)
        self.timing.clear_list()
