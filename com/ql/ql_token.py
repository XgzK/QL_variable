import datetime
import re

from com import Markings, father
from com.bot.information import Interact
from com.gheaders.log import LoggerClass

from com.sql import Sql

conn = Sql()
interact = Interact()
logger = LoggerClass('debug')


def ql_write(data: dict, essential: list):
    """
    写入青龙任务配置文件
    :param data: 传入内容
    :param essential: 添加进重复数据库的关键字
    :return: 如果没有执行过返回0，如果执行过返回-1
    """
    try:
        if father.AdReg.get('deduplication') == 1:
            return 0
        # 0表示不去重复
        elif data["marking"] == "NOT":
            interact.distribute(f"NOT表示属于不去重复关键字(未开发功能): \n{data['activities']}")
            return 0
        elif data["marking"] == "RUN":
            return 0
        elif essential[0] == 2:
            conn.insert(table=conn.surface[1], jd_value1=f"{essential[1]}",
                        jd_data=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            return 0
    except Exception as e:
        logger.write_log("ql_write,异常信息：" + str(e))
        return -1


def ql_compared(jst: str, ql_ck: tuple) -> list:
    """
    遍历青龙任务来对比,获取任务ID
    :param jst: 脚本名称
    :param ql_ck: 青龙数据库
    :return: ID or -1
    """
    try:
        jstx = father.read(ql_ck[5])
        # 判断脚本时否存在,不存在直接返回
        if not (jst in jstx):
            return [-1]
        va1 = jstx[jst]
        # 判断用户时否需要优先执行特定库 task 库/脚本.js
        ta = father.AdReg.get('library') + jst
        lis = list(va1.keys())
        return [va1[ta]['id'] if ta in lis else va1[lis[0]]['id']]
    except Exception as e:
        logger.write_log(f'查询任务异常信息: {e}')
        return [-1]


def contrast(str12:dict):
    """
    去除掉相同脚本参数,如果脚本相同只执行一次
    :param str12: 活动参数
    :return: NOT关键字返回 [0] 执行过返回 [1, 关键字] 没有执行过 [2, 关键字] 没有识别 [3] 异常 [-1] 执行
    """
    try:
        if str12["marking"] in Markings:
            return [0]

        # 提取链接类型关键字
        keywords_url1 = re.findall("(?:activityId|configCode|actId|user_id|shopId|a|token)=\"?(\w+)", str12["activities"], re.S)
        if keywords_url1:
            inquire = 1 if conn.selectTopone(table=conn.surface[1], where=f"jd_value1='{keywords_url1[0]}'") else 2
            return [inquire, keywords_url1[0]]

        # 提取特殊链接类型
        keywords_url2 = re.findall("(?:id|code|Id|activityUrl)=\"?(\w+)", str12["activities"], re.S)
        if keywords_url2:
            inquire = 1 if conn.selectTopone(table=conn.surface[1], where=f"jd_value1='{keywords_url2[0]}'") else 2
            return [inquire, keywords_url2[0]]

        # 提取变量非链接类型
        keywords_url3 = re.findall("=\"([a-zA-Z0-9&]+)", str12["activities"], re.S)
        if keywords_url3:
            inquire = 1 if conn.selectTopone(table=conn.surface[1], where=f"jd_value1='{keywords_url3[0]}'") else 2
            return [inquire, keywords_url3[0]]
        return [3]
    except Exception as e:
        logger.write_log('去掉相同活动异常: ', e)
        return [-1]
