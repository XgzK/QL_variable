import json
import re

from conn.gheaders.conn import read_txt, read_yaml
from conn.gheaders.log import LoggerClass
from conn.sql.pysql import select_data
logger = LoggerClass('debug')

"""
此脚本用来适配青龙版本的
"""


def ql13_sql(str12):
    """
    适配青龙13，直接调用数据库查询
    :param str12: 脚本名称
    :return: 异常和没有脚本返回[-1]，有返回脚本id
    """
    try:
        l = select_data()
        # 循环读取青龙脚本
        for i in range(len(l)):
            # 把多余的部分去掉
            cs = l[i][2].split("/")
            # print(cs[-1])
            # 对比脚本名称
            if cs[-1] == str12:
                print("脚本名称：" + str12 + "脚本id：" + str(l[i][0]))
                # 因为必须数组所以这里创建一个数组,返回数组id
                dd = [l[i][0]]
                # 如果对比成功立刻结束此方法
                logger.write_log("脚本: " + str12 + "名称: " + l[i][1] + "id: " + str(l[i][0]))
                return dd
        # 如果运行到这里表示这个脚本你没有
        logger.write_log(str(str12) + "脚本不存在")
        return [-1]
    except Exception as e:
        logger.write_log("ql13_sql,异常信息：" + str(e))
        return [-1]


def ql10_db(str12):
    """
    适配青龙10版本，调用伪数据库的json
    :param str12: 脚本名称
    :return: 异常和没有脚本返回[-1]，有返回脚本id 字符串类型,
    """
    try:
        js = read_yaml()
        # 获取伪数据库内容
        jstx = read_txt(js['db'])
        # 循环读取青龙脚本
        for i in jstx:
            # 把文件读取成json格式
            sq = json.loads(i)
            scri = sq['command']
            cs1 = scri.split("/")
            # 对比脚本名称
            if cs1[-1] == str12:
                print("脚本名称：" + str12 + "脚本id：" + str(sq['_id']))
                # 因为必须数组所以这里创建一个数组,返回数组id
                dd = [sq['_id']]
                # 如果对比成功立刻结束此方法
                logger.write_log("脚本: " + str12 + " 名称: " + sq['name'] + " id: " + sq['_id'])
                return dd
        # 如果运行到这里表示这个脚本你没有
        logger.write_log(str(str12) + "：脚本你没有!!!!!")
        return [-1]
    except Exception as e:
        logger.write_log("ql10_db,异常信息：" + str(e))
        return [-1]


def ql10_2_db(str12):
    """
    适配青龙10.2版本，调用伪数据库的json
    :param str12: 脚本名称
    :return: 异常和没有脚本返回[-1]，有返回脚本id 字符串类型,
    """
    try:
        js = read_yaml()
        # 获取伪数据库内容
        jstx = read_txt(js['db'])
        # 循环读取青龙脚本
        for i in jstx:
            # 把文件读取成json格式
            sq = json.loads(i)
            scri = sq['command']
            # # 使用正则表达式匹配脚本名称
            cs1 = re.findall(r'{}'.format(str12), scri)
            # # 对比脚本名称
            if len(cs1) == 1:
                # 因为必须数组所以这里创建一个数组,返回数组id
                dd = [sq['_id']]
                # 如果对比成功立刻结束此方法
                logger.write_log("脚本: " + str12 + " 名称: " + sq['name'] + " id: " + sq['_id'])
                return dd
        # 如果运行到这里表示这个脚本你没有
        logger.write_log(str(str12) + "：脚本你没有!!!!!")
        return [-1]
    except Exception as e:
        logger.write_log("ql10_2_db,异常信息：" + str(e))
        return [-1]
