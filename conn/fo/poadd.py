import os
import re

from conn.gheaders.conn import read_yaml, revise_yaml

yml = read_yaml()


def ym_change(li: list):
    """
    往conn.yml添加内容
    :param li:
    :return:
    """
    l = re.findall('(http.*?:\d+)', li[0])
    li[0] = l[0]
    # li34都是空
    if li[3] == '' and li[4] == '':
        # 表示用户没有输入时间
        revise_yaml(f"ip: '{li[0]}'", 2)
        revise_yaml(f"Client ID: '{li[1]}'", 4)
        revise_yaml(f"Client Secret: '{li[2]}'", 5)
        return '添加成功青龙'
    # li34都非空
    elif li[4] != '' and li[3] != '':
        # 自己搭建了爬虫接口
        revise_yaml(f"ip: '{li[0]}'", 2)
        revise_yaml(f"Client ID: '{li[1]}'", 4)
        revise_yaml(f"Client Secret: '{li[2]}'", 5)
        ur = re.findall(r'xgzq\.ml', li[4])
        if len(ur) == 0 and int(li[3]) >= 2:
            revise_yaml(f"time: {li[3]}", 17)
            revise_yaml(f"url: '{li[4]}'", 7)
            os.system("kill -9 $(netstat -nlp | grep addvalue.py | awk '{print $7}' | awk -F'/' '{ print $1 }')")
            return "添加私人API成功"
        else:
            return "提交的公益API禁止修改时间,或时间不得小于2分钟"
    # li3空4非空
    elif li[4] != '' and li[3] == '':
        # 提交非自己搭建的接口
        revise_yaml(f"ip: '{li[0]}'", 2)
        revise_yaml(f"Client ID: '{li[1]}'", 4)
        revise_yaml(f"Client Secret: '{li[2]}'", 5)
        revise_yaml(f"url: '{li[4]}'", 7)
        os.system("kill -9 $(netstat -nlp | grep addvalue.py | awk '{print $7}' | awk -F'/' '{ print $1 }')")
        return "添加API成功"
    elif li[3] != '' and li[4] == '':
        # 自己搭建了爬虫接口
        revise_yaml(f"ip: '{li[0]}'", 2)
        revise_yaml(f"Client ID: '{li[1]}'", 4)
        revise_yaml(f"Client Secret: '{li[2]}'", 5)
        ur = re.findall(r'xgzq\.ml', yml['url'])
        if len(ur) == 0 and int(li[3]) >= 2:
            revise_yaml(f"time: {li[3]}", 17)
            os.system("kill -9 $(netstat -nlp | grep addvalue.py | awk '{print $7}' | awk -F'/' '{ print $1 }')")
            return "修改爬取时间成功"
        else:
            return "提交的公益API禁止修改时间,或时间不得小于2分钟"
    return "错误"


def upgrade(sun: int):
    """
    根据sun的值不同采用不同的方式升级
    :param sun: 0 or 1
    :return:
    """
    if int(sun) == 0:
        print("不保留配置更新")
        os.system("sh /root/UpdateAll.sh")
    elif int(sun) == 1:
        print("保留配置更新")
        os.system("sh /root/UpdateAll.sh 1")
