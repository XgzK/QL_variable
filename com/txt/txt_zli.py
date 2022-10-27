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
        # ht_tx = re.findall(r'(https://.*?-isv.*?\.com/[a-zA-z0-9-&\.\?=_/\+].*)', tx1, re.S)
        # if len(ht_tx) > 0:
        #     https_txt(ht_tx[0])
        # ex_ht = re.findall('(export [0-9a-zA-Z_]+="?https://[a-zA-Z0-9-&\.\?=_/]{21,}")', tx1, re.S)
        # # 如果开头是export =后面有"https://则添加到文本中
        # if ex_ht:
        #     print(ex_ht[0])
        #     tx_compared(ex_ht[0])
        # 对多个参数支持
        ex_t1 = tx1.split('\n')
        ex_t2 = ''
        for i in ex_t1:
            print(i)
            ex_tx = re.findall(r'(export [0-9a-zA-Z_]+="?[A-Za-z0-9&_/:\.-]{7,}"?)', i, re.S)
            print(ex_tx)
            if len(ex_tx) > 0:
                ex_t2 += ex_tx[0] + ";"
        print(ex_t2)
        tx_compared(ex_t2) if ex_t2 else ''
    except Exception as e:
        logger.write_log(f"异常问题: {e}")

