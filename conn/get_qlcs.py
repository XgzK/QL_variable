import requests

from conn.gheaders.conn import read_yaml
from conn.gheaders.log import log_ip


def get_qlcs():
    """
    获取青龙任务需要的参数
    :return: 返回json格式文件,如果没有返回空列表
    """
    try:
        ur = read_yaml()
        res = requests.get(url=ur['url'], timeout=5)
        jstx = res.json()
        # 判断是是否为空
        if len(jstx) > 0:
            return jstx
        else:
            return []
    except Exception as e:
        log_ip("get_qlcs,获取参数的网址异常，请去github反馈,异常信息：" + str(e))
        return []


def js_parameter(jsvalue):
    """
    处理获取到的参数，把脚本名称和参数分隔开
    :param jsvalue:
    :return: [0]返回的脚本名称 [1] 运行脚本需要的参数
    """
    try:
        jsname = []
        jsval = []
        # 循环获取的json
        for i in jsvalue:
            data = jsvalue[i]
            qlcs = data.split("\n")
            jsname.append(qlcs[0])
            jsval.append(qlcs[1])
        return [jsname, jsval]
    except Exception as e:
        log_ip("js_parameter,异常信息：" + str(e))
        return []


def get_main():
    """
    主要用于获取爬取
    :return: [0]返回的脚本名称 [1] 运行脚本需要的参数,如果没有返回空列表
    """
    gejs = get_qlcs()
    if len(gejs) > 0:
        js = js_parameter(gejs)
        return js
    else:
        return []
