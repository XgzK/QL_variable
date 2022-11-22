import os
import re
import threading
import time

from com.gheaders.conn import read_yaml, revise_yaml
from com.ql import ql
from com.sql import conn

yml = read_yaml()


def ym_change(li: list):
    """
    根据用户表单提交的值往conn.yml添加内容
    :param li: 表单返回的数组
    :return:
    """
    tf = 0  # 记录是否需要重启
    st = ''
    # 任务是否去重复
    if len(li) == 5:
        revise_yaml(f"deduplication: 1", yml['Record']['deduplication'])
        st += '任务不去重复'
    elif len(li) == 6:
        revise_yaml(f"deduplication: 0", yml['Record']['deduplication'])
        st += '任务去重复'
    if li[0] != '':
        revise_yaml(f'Administrator: {li[0]}', yml['Record']['Administrator'])
        st += f' 你设置机器人的管理员是: {li[0]} '
        tf = 1
    # 表示用户输入了自己优先执行的库了
    if li[1] != '':
        k = li[1].split('/')[0] + '/'
        revise_yaml(f'library: {k}', yml['Record']['library'])
        st += f' 你优先执行的库是: {k}'
    if li[2] != '':
        revise_yaml(f'Token: {li[2]}', yml['Record']['Token'])
        st += f' 机器人密钥添加成功'
        tf = 1
    if li[3] != '':
        revise_yaml(f'Proxy: {li[3]}', yml['Record']['Proxy'])
        st += f'代理添加成功'
        tf = 1
    if li[4] != '':
        tg_url = re.findall('^(http.*)', li[4])
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


def to_stop(sun: int):
    """
    禁止活动任务脚本
    根据sun的值不同采用不同的方式禁用
    :param sun: 1 禁用所有 别的禁用活动
    :return:
    """
    try:
        st = ""
        lis = set()
        lines = conn.selectAll(table=conn.surface[0])
        value1 = conn.selectAll(table=conn.surface[3], where=f"state=0")
        if not value1:
            return f'没有可正常执行的青龙'
        # 循环所有青龙
        for ql_tk in value1:
            js = read_yaml(ql_tk[5])
            st += ql_tk[0]
            if sun == 0:
                for i in js.keys():
                    if js[i] == 1:
                        continue
                    for j in range(len(js[i]) - 1):
                        lis.add(js[i][list(js[i])[j]]['id'])
            # 循环数据库
            for i in lines:
                # 跳过不在json文件的脚本
                if not (i[2] in js):
                    continue
                for j in js[i[2]].keys():
                    if js[i[2]][j]['isDisabled'] == 0:
                        lis.add(js[i[2]][j]['id'])
            st += f": 禁止任务成功禁用ID{list(lis)}\n" if ql.disable(list(lis), ql_tk) == 0 else f": 禁止任务失败\n"
        return st
    except Exception as e:
        return '异常信息' + str(e)
