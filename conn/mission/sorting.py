import re
from urllib import parse

from conn.mission.sundries import Sundries
from conn.tools.log import LoggerClass


class Sorting:

    def __init__(self):
        """
        分拣活动的类型，根据类型分配不同地方
        """
        self.logger = LoggerClass()
        self.sundries = Sundries()

    def dispatch(self, tg_text: str):
        """
        把tg的消息进行分类派送到他们需要去的地方
        :param tg_text: text文本
        :return:
        """
        try:
            self.sundries.marking_time()

            # 对URL进行处理去掉关键字和URL解码
            tg_text = re.sub("[()`*]*(?:export NOT_TYPE=\".*?\";)*", "", parse.unquote(tg_text))
            # 直接结束
            if re.findall(r'(https://u\.jd\.com/.*?)', tg_text, re.S):
                return

            if re.findall('(?:NOTexport|RUNexport|export)\s+[0-9a-zA-Z_]+=', tg_text):
                self.finishing_text(tg_text)
                return
            self.finishing_url(tg_text)
        except Exception as e:
            self.logger.write_log(f"com.txt.txt.zil.Delivery.dispatch 异常 {e}")

    def finishing_url(self, text_url: str):
        """
        处理URL类型
        :param text_url:
        :return:
        """
        try:
            mark = ""
            mark_text = re.findall("((?:NOT|RUN)+)", text_url)
            if mark_text:
                mark = mark_text[0]
            # 获取链接
            ht_tx = re.findall(r'(https://[\w\-.]+(?:isv|jd).*?\.com/[a-zA-Z0-9&?=_/-].*)"?', text_url)
            if not ht_tx:
                return []
            for i in ht_tx:
                self.sundries.interaction.for_message(i)
                text_list = self.sundries.https_txt(i)
                if not text_list:
                    continue
                for j in text_list:
                    # 发送去队列了
                    self.sundries.tx_compared([mark, j[1], j[0]])
            return [200]
        except Exception as e:
            self.logger.write_log(f"conn.mission.sorting.Sorting.finishing_url 异常 {e}")
            return []

    def finishing_text(self, text_str: str):
        """
        对非链接进行处理
        :param text_str:
        :return:
        """
        global re_text, poi, mark
        try:
            # 对多个参数支持
            points = text_str.split('\n')
            spell = ''
            rep = {}

            for poi in points:

                re_text = re.findall(r'((?:NOTexport|RUNexport|export)\s+[0-9a-zA-Z_]+)="?([A-Za-z0-9&_/:.?=\-]{5,})"?',
                                     poi, re.S)
                # 如果获取数组为空跳过
                if not re_text or len(re_text[0]) != 2:
                    continue

                # 如果一行出现两个关键字
                for text2 in re_text:

                    mark = ""
                    mark_text = re.findall("((?:NOT|RUN)+)", text2[0])
                    if mark_text:
                        mark = mark_text[0]

                    # 如果值存在关键字跳过执行
                    if re.findall('(?:shopId\d?|venderId\d?|shopid\d?|venderid\d?)', text2[-1]):
                        self.logger.write_log(f"检测到屏蔽关键字屏蔽内容是: {poi}")
                        continue

                    if text2[0] in rep.keys():
                        self.sundries.interaction.for_message(spell)
                        # 如果关键字在数组中执行并且清空字典
                        ex_name = self.sundries.looking(rep.get(text2[0])["expport"])
                        if ex_name:
                            # 发送去队列了
                            spell += 'export NOT_TYPE="no";'
                            self.sundries.tx_compared([rep.get(text2[0])['mark'], ex_name, spell])
                        else:
                            spell = ''
                            self.logger.write_log(f"没有查询到 {poi}")
                        rep.popitem()

                    # 如果关键字不在数组加入数组
                    rep.setdefault(text2[0], {
                        "mark": mark,
                        "expport": re_text[0][0]
                    })
                    spell += text2[0] + '="' + str(text2[1]) + '";'
            if spell:
                # 如果值相同转发，一般是最后一个了,可能有BUG
                ex_name = self.sundries.looking(rep.get(list(rep.keys())[0])["expport"])
                if not ex_name:
                    self.logger.write_log(f"没有查询到 {poi}")
                self.sundries.interaction.for_message(spell)
                # 发送去队列了
                spell += 'export NOT_TYPE="no";'
                self.sundries.tx_compared([mark, ex_name, spell])
                return [0]
            return []
        except Exception as e:
            self.logger.write_log(f"conn.mission.sorting.Sorting.finishing_text 异常 {e}")
            return []

