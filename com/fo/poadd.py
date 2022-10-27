import os
import re
import threading
import time

from com.fo.core import adaptation
from com.fo.stop import Prohibition
from com.gheaders.conn import read_yaml, revise_yaml
from com.ql.ql import QL

yml = read_yaml()
prohibition = Prohibition()
ql = QL()


def ym_change(li: list):
    """
    根据用户表单提交的值往conn.yml添加内容
    :param li: 表单返回的数组
    :return:
    """
    tf = 0  # 记录是否需要重启
    st = ''
    if len(li) == 7:
        revise_yaml(f"deduplication: 1", yml['Record']['deduplication'])
        st += '任务不去重复'
    elif len(li) == 8:
        revise_yaml(f"deduplication: 0", yml['Record']['deduplication'])
        st += '任务去重复'
    # 判断用户输入的值如果返回的列表是先判断0-3是不是为空,如果为空则表示用户并不是提交青龙URL这里直接判断0位是不是空
    if li[0] != '' and li[1] != '' and li[2] != '':
        # 判断url是否符合要求
        ur = re.findall('^(http.*?:\d+)', li[0])
        # 如果不符合要求则进入
        if len(ur) == 0:
            return [0, "URL不符合格式要求,请复制浏览器上完整的青龙URL"]
        # 把用户提交的青龙相关提交到配置文件
        revise_yaml(f"ip: '{ur[0]}'", yml['Record']['ql'][0])
        revise_yaml(f"Client ID: '{li[1]}'", yml['Record']['ql'][1])
        revise_yaml(f"Client Secret: '{li[2]}'", yml['Record']['ql'][2])
        st += '青龙URL提交成功 '
    # 表示用户输入了自己优先执行的库了
    if li[3] != '':
        k = li[3].split('/')[0] + '/'
        revise_yaml(f'library: {k}', yml['Record']['library'])
        st += f' 你优先执行的库是: {k}'
    if li[4] != '':
        revise_yaml(f'Token: {li[4]}', yml['Record']['Token'])
        st += f' 机器人密钥添加成功'
        tf = 1
    if li[5] != '':
        revise_yaml(f'Proxy: {li[5]}', yml['Record']['Proxy'])
        st += f'代理添加成功'
        tf = 1
    if li[6] != '':
        tg_url = re.findall('^(http.*)', li[6])
        print(tg_url)
        if tg_url:
            revise_yaml(f'TG_API_HOST: {tg_url[0]}', yml['Record']['TG_API_HOST'])
            st += f'反代添加成功'
            tf = 1
    if tf == 1:
        t1 = threading.Thread(target=upgrade, args=(1,))
        t1.start()
        st += f' 正在重启请10秒后手动刷新浏览器'
    return [0, st]


def upgrade(sun: int):
    """
    根据sun的值不同采用不同的方式升级
    :param sun: 0 or 1
    :return:
    """
    time.sleep(3)
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


