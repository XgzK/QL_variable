import re

from com.gheaders import LoggerClass
from com.txt.deal_with import https_txt
from com.txt.txt_compared import tx_compared

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
        ht_tx = re.findall(r'(https://.*?-isv.*?\.com/[a-zA-z0-9-&\.\?=_/\+].*)', tx1, re.S)
        if len(ht_tx) > 0:
            https_txt(ht_tx[0])
            return
        # 对多个参数支持
        ex_t1 = tx1.split('\n')
        ex_t2 = ''
        for i in ex_t1:
            ex_tx = re.findall(r'(export [0-9a-zA-Z_]+="?[A-Za-z0-9&_/:\.-]{7,}"?)', i, re.S)
            if len(ex_tx) > 0:
                ex_t2 += ex_tx[0] + ";"
        tx_compared(ex_t2) if ex_t2 else ''
    except Exception as e:
        logger.write_log(f"异常问题: {e}")

