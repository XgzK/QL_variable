"""
TG机器人
"""
import time

from conn.bots.getUpdate import GetUpdate
from conn.bots.json.channel_post import Channel_post
from conn.bots.json.message import Message
from conn.tools import util


class Filter:

    def __init__(self):
        self.getdata = GetUpdate()
        self.message = Message()
        self.channel = Channel_post()

    def _points(self, tg_list: list):
        """
        对TG消息进行分类处理
        :param tg_list: 接收到的TG小时数组
        :return:
        """
        for i in tg_list:
            if i[list(i.keys())[-1]]['date'] < int(time.time()) - 3600:
                continue
            if type(i) == int:
                continue
            elif type(i) == dict:
                if 'message' in i:
                    # print('文本消息  ', i)
                    self.message.filter_message(i['message'])
                    continue
                elif 'channel_post' in i:
                    # print('频道帖子  ', i)
                    self.channel.channel_main(i['channel_post'])
                # elif 'chat_member' in i:
                #     print('加入请求', i)
                    # return chatmember.filter_chatmessage(i['chat_member']
                # elif 'edited_message' in i:
                #     print('消息被编辑  ', i)
                # elif 'edited_channel_post' in i:
                #     print('频道帖子被编辑  ', i)
                # elif 'inline_query' in i:
                #     print('内联查询  ', i)
                # elif 'chosen_inline_result' in i:
                #     print('选择的内联结果  ', i)
                # elif 'callback_query' in i:
                #     print('回调查询  ', i)
                # elif 'shipping_query' in i:
                #     print('运费查询  ', i)
                # elif 'pre_checkout_query' in i:
                #     print('结帐前查询  ', i)
                # elif 'poll' in i:
                #     print('投票  ', i)
                # elif 'poll_answer' in i:
                #     print('投票答案  ', i)
                # elif 'my_chat_member' in i:
                #     print('我的聊天会员  ', i)
                # elif 'chat_member' in i:
                #     print('聊天会员  ', i)
                # elif 'chat_join_request' in i:
                #     print('聊天加入请求  ', i)
                # else:
                #     print(i)

    def main_bots(self):
        """
        循环请求TG获取消息
        :return:
        """
        tf = True
        while tf:
            self.getdata.marking_time()
            if self.getdata.AdReg.get('Token'):
                self.getdata.Update()
                tf = False
            else:
                print('没有填写到机器人Token')
                time.sleep(15)
        while True:
            self.getdata.marking_time()
            tg_list = self.getdata.get_long_link(allowed_updates=util.update_types, timeout=100)
            self._points(tg_list)
