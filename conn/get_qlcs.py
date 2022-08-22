import time

import requests

from conn.gheaders.conn import read_yaml
from conn.gheaders.log import LoggerClass

logger = LoggerClass('debug')


def get_url():
    """
    获取爬取的网址
    :return: 返回爬取的网址
    """
    try:
        ur = read_yaml()
        res = requests.get(url=ur['url'], timeout=15)
        # 返回状态码为200时
        return res
    except Exception as e:
        logger.write_log("get_url,获取爬取的网址异常，请去github反馈,异常信息：" + str(e))
        return -1


def get_qlcs():
    """
    获取青龙任务需要的参数
    :return: 返回json格式文件,如果没有返回空列表
    """
    try:
        # 最多请求3次，避免请求失败
        for i in range(3):
            res = get_url()
            # 返回状态码为200时
            if res.status_code == 200:

                jstx = res.json()
                # 判断是是否为空
                if len(jstx) > 0:
                    return jstx
                else:
                    return -1
            else:
                # 返回状态码不为200时，延迟3秒再请求
                time.sleep(3)
        return -1
    except Exception as e:
        logger.write_log("get_qlcs,异常信息：" + str(e))
        return -1


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
        logger.write_log("js_parameter,异常信息：" + str(e))
        return []


def get_main():
    """
    主要用于获取爬取
    :return: [0]返回的脚本名称 [1] 运行脚本需要的参数,如果没有返回空列表
    """
    gejs = get_qlcs()
    if gejs != -1:
        js = js_parameter(gejs)
        return js
    else:
        return -1
