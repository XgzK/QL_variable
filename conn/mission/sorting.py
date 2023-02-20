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
        global ex_name
        try:
            # 对多个参数支持
            points_list = text_str.split('\n')
            mark = None
            text1 = ''
            spell = ''
            # 遍历数组
            for poi_str in points_list:
                # 检测是否在黑名单
                re_text = re.findall(r'((?:NOTexport|RUNexport|export)\s+[0-9a-zA-Z_]+)="?([A-Za-z0-9&_/:.?=\-]{5,})"?',
                                     poi_str, re.S)
                # 如果获取数组为空跳过
                if not re_text or len(re_text[0]) != 2:

                    # 如果断开表示是两个活动
                    if spell:
                        # 如果关键字在数组中执行并且清空字典
                        ex_name = self.sundries.looking(text1)

                        if ex_name:
                            for ex_list in ex_name:
                                TYPE = re.findall("https://(\w{2})", spell)
                                if TYPE:
                                    spell += f'export NOT_TYPE="{TYPE[0]}";'
                                else:
                                    spell += 'export NOT_TYPE="no";'
                                # 发送去队列了
                                self.sundries.tx_compared([mark, ex_list, spell])
                        mark = None
                        spell = ''
                    continue

                # 如果一行出现两个关键字
                for text2 in re_text:
                    text2 = list(text2)

                    # 如果值存在关键字跳过执行
                    if re.findall('(?:shopId\d|venderId\d|shopid\d|venderid\d)', text2[-1]):
                        self.logger.write_log(f"检测到屏蔽关键字屏蔽内容是: {poi_str}")
                        continue

                    mark_text = re.findall("((?:NOT|RUN)+)", text2[0])
                    # 如果是关键字则切割和记录
                    if mark_text:
                        mark = mark_text[0]
                        text2[0] = text2[0][3::]
                    text1 = text2[0]

                    spell += text2[0] + '="' + text2[1] + '";'
                    # 获取脚本
            if not text1:
                return []
            ex_name = self.sundries.looking(text1)

            if ex_name:
                for ex_list in ex_name:
                    TYPE = re.findall("https://(\w{2})", spell)
                    if TYPE:
                        spell += f'export NOT_TYPE="{TYPE[0]}";'
                    else:
                        spell += 'export NOT_TYPE="no";'
                    # 发送去队列了
                    self.sundries.tx_compared([mark, ex_list, spell])
            else:
                self.logger.write_log(f"没有查询到 {poi_str}")
            return []
        except Exception as e:
            self.logger.write_log(f"conn.mission.sorting.Sorting.finishing_text 异常 {e}")
            return []
