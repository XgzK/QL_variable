import re
from urllib import parse

from com.bot.information import Interact
from com.gheaders.conn import ConnYml
from com.gheaders.log import LoggerClass
from com.txt.inquire import Conversion

interact = Interact()
connyml = ConnYml()
conver = Conversion()
logger = LoggerClass()


class Delivery:

    def __init__(self):
        self.read = connyml.read_yaml()

    def dispatch(self, tg_text: str):
        """
        把tg的消息进行分类派送到他们需要去的地方
        :param tg_text: text文本
        :return:
        """
        try:
            self.read = connyml.read_yaml()

            # 对URL进行处理去掉关键字和URL解码
            tg_text = re.sub("[()`\"*]+", "", parse.unquote(tg_text))
            # 直接结束
            if re.findall(r'(https://u\.jd\.com/.*?)', tg_text, re.S):
                return

            if not self.url(tg_text):
                self.export_txt(tg_text)
        except Exception as e:
            logger.write_log(f"com.txt.txt.zil.Delivery.dispatch 异常 {e}")

    def url(self, tg_text):
        """
        处理URL链接
        :return:
        """
        try:
            # 获取链接
            ht_tx = re.findall(r'(https://[\w\-\.]+(?:isv|jd).*?\.com/[a-zA-Z0-9&?=_/-].*)"?', tg_text)
            if not ht_tx:
                return []
            for i in ht_tx:
                conver.https_txt(i)
                interact.distribute(i, self.read["Send_IDs"]) if self.read["Send_IDs"] else ""
            return [200]
        except Exception as e:
            logger.write_log(f"com.txt.txt.zil.Delivery.url 异常 {e}")
            return []

    def export_txt(self, tg_text: str):
        """
        处理关键字
        :param tg_text:
        :return:
        """
        try:
            # 对多个参数支持
            points = tg_text.split('\n')
            spell = ''
            rep = []

            for poi in points:
                re_text = re.findall(r'(export [0-9a-zA-Z_]+)="?([A-Za-z0-9&_/:.?=-]{5,})"?', poi, re.S)
                # 如果获取数组为空跳过
                if not re_text or len(re_text[0]) != 2:
                    continue

                if re_text[0][0] in rep:
                    # 如果关键字在数组中执行并且清空数组
                    self.forward(spell)
                    rep.clear()

                # 如果关键字不在数组加入数组
                rep.append(re_text[0][0])
                spell += re_text[0][0] + '="' + str(re_text[0][1]) + '";'
                self.forward(spell)
            return
        except Exception as e:
            logger.write_log(f"com.txt.txt.zil.Delivery.export_txt 异常 {e}")

    def forward(self, export_text):
        """
        简单的转发和执行
        :param export_text:
        :return:
        """
        try:
            url_list = conver.turn_url(export_text)

            if not url_list:
                interact.distribute(url_list) if self.read["Send_IDs"] else ""
                export_text += 'export NOT_TYPE="no";'
                conver.tx_compared(export_text)
                return
            tx = ''

            for url in url_list:
                tx += url + '\n'
                conver.https_txt(url)

            interact.distribute(tx, self.read["Send_IDs"]) if self.read["Send_IDs"] else ""
        except Exception as e:
            logger.write_log(f"com.txt.txt.zil.Delivery.forward 异常 {e}")
