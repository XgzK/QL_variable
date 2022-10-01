import os
import re
import time

from conn.fo.core import adaptation
from conn.fo.stop import Prohibition
from conn.gheaders.conn import read_yaml, revise_yaml
from conn.ql.ql import QL

yml = read_yaml()
prohibition = Prohibition()
ql = QL()


def ym_change(li: list):
    """
    根据用户表单提交的值往conn.yml添加内容
    :param li: 表单返回的数组
    :return:
    """
    st = ''
    # 判断用户是否关闭了去重复开关,如果长度为6表示没有开启去重复
    if len(li) == 6:
        revise_yaml(f"deduplication: 1", yml['Record']['deduplication'])
    # 判断用户输入的值如果返回的列表是先判断0-3是不是为空,如果为空则表示用户并不是提交青龙URL这里直接判断0位是不是空
    if li[0] != '' and li[1] != '' and li[2] != '':
        # 判断url是否符合要求
        ur = re.findall('^(http.*?:\d+)/', li[0])
        # 如果不符合要求则进入
        if len(ur) == 0:
            return "URL不符合格式要求,请复制浏览器上完整的青龙URL"
        # 把用户提交的青龙相关提交到配置文件
        revise_yaml(f"ip: '{ur[0]}'", yml['Record']['ql'][0])
        revise_yaml(f"Client ID: '{li[1]}'", yml['Record']['ql'][1])
        revise_yaml(f"Client Secret: '{li[2]}'", yml['Record']['ql'][2])
        st += '青龙URL提交成功 '
    # 3非空表示用户提交了自己的API
    if li[3] != '':
        ur = re.findall(r'xgzq', li[3])
        # 要修改时间不能有 xgzq 的关键字
        if ur and len(li[4]) != '' and type(li[4]) == int:
            revise_yaml(f"time: {li[4]}", yml['Record']['time'])
            revise_yaml(f"url: '{li[3]}'", yml['Record']['url'])
            os.system(yml['kill'])
        else:
            revise_yaml(f"url: '{li[3]}'", yml['Record']['url'])
            st += '爬虫API提交成功 '
    # 表示用户输入了自己优先执行的库了
    if li[5] != '':
        k = li[5].split('/')[0] + '/'
        revise_yaml(f'library: {k}', yml['Record']['library'])
        st += f'你优先执行的库是: {k}'
    return [0, st]


def upgrade(sun: int):
    """
    根据sun的值不同采用不同的方式升级
    :param sun: 0 or 1
    :return:
    """
    time.sleep(15)
    if int(sun) == 0:
        print("不保留配置更新")
        os.system("sh /root/UpdateAll.sh")
    elif int(sun) == 1:
        print("保留配置更新")
        os.system("sh /root/UpdateAll.sh 1")


def to_stop():
    """
    禁止活动任务脚本
    :return:
    """
    try:
        # 获取版本号
        val = adaptation()
        li = prohibition.get_re()
        lis = prohibition.compareds(li, val)
        print(lis)
        ql.disable(lis)
        return '禁止任务成功'
    except Exception as e:
        return '异常信息' + str(e)
