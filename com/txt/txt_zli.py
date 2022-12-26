import re

from com.bot.information import Interact
from com.gheaders.conn import read_yaml
from com.gheaders.log import LoggerClass
from com.txt.deal_with import https_txt
from com.txt.inquire import turn_url
from com.txt.txt_compared import tx_compared

logger = LoggerClass()
interact = Interact()


def forward(ex_t2, yml):
    """
    简单的转发和执行
    :param ex_t2:
    :param yml:
    :return:
    """
    ur = turn_url(ex_t2)
    if not ur:
        if yml['Send_IDs']:
            interact.distribute(ex_t2, yml['Send_IDs'])
        ex_t2 += 'export NOT_TYPE="no";'
        tx_compared(ex_t2)
    tx = ''
    for j in ur:
        tx += j + '\n'
        https_txt(j)
    if yml['Send_IDs'] and tx:
        interact.distribute(tx, yml['Send_IDs'])


def tx_revise(tx1: str):
    """
    用与修改文本,只保留关键字到文本
    :param tx1: 接收到的消息
    :return: 正常返回200, 否则返回-1
    """
    yml = read_yaml()
    try:
        tx1 = tx1.replace("(", "").replace(")", "").replace("`", "")
        # 如果用户发生的是内容不在正则表达式的理解范围将跳过
        if not re.findall('([A-Za-z0-9&_/:.-]{5,})', tx1):
            return
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
        rep = []
        for i in ex_t1:
            ex_tx = re.findall(r'(export [0-9a-zA-Z_]+)="?([A-Za-z0-9&_/:.-]{5,})"?', i, re.S)
            # 如果获取数组为空跳过
            if ex_tx:
                # 判断是不是同一任务的变量
                if not (ex_tx[0][0] in rep):
                    rep.append(ex_tx[0][0])
                    ex_t2 += ex_tx[0][0] + '="' + str(ex_tx[0][1]) + '";'
                # 如果ex_t2变量的值长度大于4执行，防止为空
                elif ex_t2:
                    forward(ex_t2, yml)
                    # 清空数据库和清空
                    rep.clear()
                    rep.append(ex_tx[0][0])
                    ex_t2 = ex_tx[0][0] + '="' + str(ex_tx[0][1]) + '";'
                # 跳过本次执行
                continue
            # 执行域名是sh 那一块的内容
            jdsh = re.findall(r'(https://shop\.m\.jd\.com/[a-zA-Z0-9&?=_/-].*)"?', i, re.S)
            if jdsh:
                https_txt(jdsh[0])
            # 执行域名是h5 那一块的内容
            jdh5 = re.findall(r'(https://h5\.m\.jd\.com/babelDiy/Zeus.*?token=\w+)"?', i, re.S)
            if jdh5:
                https_txt(jdh5[0])
        # 执行后面结尾的内容
        if len(ex_t2) > 4:
            forward(ex_t2, yml)
    except Exception as e:
        logger.write_log(f"分类型异常问题: {e}")
