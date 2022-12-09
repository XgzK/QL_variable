import time

from com.bot import tg_mes
from com.bot.information import Interact
from com.gheaders.conn import read_yaml
from com.gheaders.log import LoggerClass
from com.txt.txt_zli import tx_revise

yml = read_yaml()


class WhileLong:
    """
    执行机器人循环和分类
    """

    def __init__(self):
        self.tg_mes = tg_mes
        self.logger = LoggerClass("error")
        self.interact = Interact()

    def old_message(self):
        """
        旧消息清理
        :return:
        """
        while True:
            if yml['Token'] and yml['Administrator']:
                tg_ms = self.tg_mes.get_long_link(ti=1)
                if tg_ms['ok'] and tg_ms['result']:
                    for result in tg_ms["result"]:
                        if result['message']['date'] < int(time.time()) - 1200:
                            tg_mes.data['offset'] = result['update_id'] + 1
                        else:
                            self.tg_mes.send_message("活动监控机器人正式为你保驾护航\n"
                                                     "不定期重启项目可以获取最新的线报支持\n"
                                                     "未经作者允许随意转发者，本项目将从github删库\n"
                                                     "来自开发者的善意警告!!!!!!", yml['Administrator'])
                            return
                else:
                    self.tg_mes.send_message("活动监控机器人正式为你保驾护航\n"
                                             "不定期重启项目可以获取最新的线报支持\n"
                                             "未经作者允许随意转发者，本项目将从github删库\n"
                                             "来自开发者的善意警告!!!!!!", yml['Administrator'])
                    return
            else:
                self.logger.write_log("没有提交必要参数机器人Token或自己ID,不进行下一步执行\t如果不知道怎么获取请 https://t.me/InteIJ 群回复 "
                                      "/id@KinhRoBot 查看自己ID")
                time.sleep(60)

    def new_message(self):
        """
        执行新的消息死循环
        :return:
        """
        while True:
            try:
                tg_ms = tg_mes.get_long_link()
                # 消息不为空和没有异常
                if not tg_ms['ok']:
                    self.logger.write_log(f"异常消息 {tg_ms['result'][0]} 触发异常停止10秒")
                    time.sleep(10)
                    continue
                if tg_ms["result"]:
                    # 确认收到消息
                    tg_mes.data['offset'] = tg_ms["result"][len(tg_ms["result"]) - 1]['update_id'] + 1
                    for result in tg_ms["result"]:
                        # message 一般是 私聊 群消息 加入群组 and 是消息而非加入群组
                        if 'message' in result and "chat" in result['message']:
                            # 跳过转发频道或群
                            if 'sender_chat' in result['message'] and yml['Send_IDs'] == \
                                    result['message']['sender_chat']['id']:
                                continue
                            # 私聊消息
                            if result['message']['chat']['type'] == 'private':
                                if 'text' in result['message']:
                                    self.logger.write_log(
                                        "收到私聊消息内容 " + str(result['message']['text']).replace('\n', '\t'))
                                    self.interact.get_id(result)
                                    tx_revise(result['message']['text'])
                            # 群消息 supergroup 公开群 group 非公开群 公开后再私有还是 supergroup
                            elif result['message']['chat']['type'] == 'supergroup' or result['message']['chat'][
                                'type'] == 'group':
                                if 'text' in result['message']:
                                    # logger.write_log(f"收到群消息内容 {result['message']['text']}")
                                    tx_revise(result['message']['text'])
                                    self.interact.group_id(result)
                                # 加入群聊
                                elif 'new_chat_member' in result['message']:
                                    tg_mes.banChatMember(result, '-1001565778760',
                                                         result['message']['new_chat_member']['id'])
                        # 频道消息
                        elif 'channel_post' in result:
                            if result['channel_post']['chat']['type'] == 'channel':
                                if 'text' in result['channel_post']:
                                    # logger.write_log(f"收到频道监控消息内容 {result['channel_post']['text']}")
                                    tx_revise(result['channel_post']['text'])
            except Exception as e:
                self.logger.write_log(f"个人开发类异常: {e}")
