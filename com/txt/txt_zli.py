import re

from com.bot.information import Interact
from com.gheaders.conn import read_yaml
from com.gheaders.log import LoggerClass
from com.txt.deal_with import https_txt
from com.txt.inquire import turn_url
from com.txt.txt_compared import tx_compared

logger = LoggerClass()
interact = Interact()

def tx_revise(tx1: str):
    """
    用与修改文本,只保留关键字到文本
    :param tx1: 接收到的消息
    :return: 正常返回200, 否则返回-1
    """
    yml = read_yaml()
    try:
        tx1 = tx1.replace("(", "").replace(")", "").replace("`", "")
        # 需要跳过的域名
        jdht = re.findall(r'(https://u\.jd\.com/.*?)', tx1, re.S)
        if len(jdht) > 0:
            return
        # 获取链接
        ht_tx = re.findall(r'(https://.*?isv.*?\.com/[a-zA-Z0-9&?=_/-].*)"?', tx1)
        if ht_tx:
            for i in ht_tx:
                https_txt(i)
                if yml['Send_IDs']:
                    interact.distribute(i, yml['Send_IDs'])
            return
        # 对多个参数支持
        ex_t1 = tx1.split('\n')
        ex_t2 = ''
        for i in ex_t1:
            ex_tx = re.findall(r'(export [0-9a-zA-Z_]+)="?([A-Za-z0-9&_/:.-]{5,})"?', i, re.S)
            for j in ex_tx:
                ex_t2 += j[0] + '="' + str(j[1]).replace("export", '') + '";'
        if len(ex_t2) > 10:
            ur = turn_url(ex_t2)
            if ur:
                for i in ur:
                    if yml['Send_IDs']:
                        interact.distribute(ex_t2, yml['Send_IDs'])
                    https_txt(i)
            else:
                if yml['Send_IDs']:
                    interact.distribute(ex_t2, yml['Send_IDs'])
                ex_t2 += 'export NOT_TYPE="no";'
                tx_compared(ex_t2)
    except Exception as e:
        logger.write_log(f"分类型异常问题: {e}")
