import re

from conn.gheaders import LoggerClass
from conn.txt.deal_with import https_txt
from conn.txt.txt_compared import tx_compared

logger = LoggerClass('debug')


def tx_revise(tx1: str):
    """
    用与修改文本,只保留关键字到文本
    :param tx1: 接收到的消息
    :return: 正常返回200, 否则返回-1
    """
    try:
        # 需要跳过的域名
        jdht = re.findall(r'(https://u\.jd\.com/.*?)', tx1, re.S)
        if len(jdht) > 0:
            return
        ex_ht = re.findall('(export [0-9a-zA-Z_]+="?https://[a-zA-Z0-9-&\.\?=_/].*")', tx1, re.S)
        # 如果开头是export =后面有"https://则添加到文本中
        if ex_ht:
            tx_compared(ex_ht[0])
        ex_tx = re.findall(r'(export [0-9a-zA-Z_]+="?[A-Za-z0-9&_]{7,}"?)', tx1, re.S)
        if len(ex_tx) > 0:
            tx_compared(ex_tx[0])
        ht_tx = re.findall(r'(https://.*?-isv.*?\.com/[a-zA-z0-9-&\.\?=_/\+].*)', tx1, re.S)
        if len(ht_tx) > 0:
            https_txt(ht_tx[0])
    except Exception as e:
        logger.write_log(f"异常问题: {e}")

