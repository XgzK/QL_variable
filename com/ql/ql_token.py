import datetime
import re

from com.bot import tg_mes
from com.gheaders.conn import read_yaml
from com.gheaders.log import LoggerClass
from com.ql import ql
from com.gheaders.conn import yml_file

from com.sql import conn

logger = LoggerClass('debug')
yam = read_yaml()


def token_main():
    """
    主要用于调用ck
    :return:
    """
    try:
        ck = ql.ql_tk()

        if ck != -1:
            str1 = 'Authorization:' + f" '{ck}'"
            yml_file(str1, read_yaml()['Record']['Authorization'])
            return 0
        else:
            return -1
    except Exception as e:
        logger.write_log("token_main败，请检查conn.yml文件，异常信息：" + str(e))
        return -1


def ql_write(str12, yal, essential):
    """
    写入青龙任务配置文件
    :param str12: 传入内容
    :param yal: conn.yml配置文件内容
    :param essential: 添加进重复数据库的关键字
    :return: 如果没有执行过返回0，如果执行过返回-1
    """
    try:
        # 针对某些不需要去重复的数据，如果不是exp则不去重复
        if str12[:3] == "exp":
            # 判断是否去重数据
            if yal['deduplication'] == 0 and len(essential) > 5:
                # 添加到数据库，如果成功添加表示之前没有运行过
                conn.insert(table=conn.surface[1], jd_value1=f"{essential}",
                            jd_data=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            return str12
        else:
            js = re.findall('(.*?)export NOT_TYPE=', str12)
            if yal['Administrator'] and js:
                tg_mes.send_message(f"NOT开头表示此活动参数需要连续几天执行: \n{js[0]}", yal['Administrator'])
            # 把后端添加的NOT不去重标记去掉
            return str12[3:]
    except Exception as e:
        logger.write_log("ql_write,异常信息：" + str(e))
        return -1


def ql_compared(jst: str) -> list:
    """
    遍历青龙任务来对比,获取任务ID
    :param jst: 脚本名称
    :return: ID or -1
    """
    try:
        jstx = read_yaml(yam['json'])
        # 判断脚本时否存在,不存在直接返回
        if not (jst in jstx):
            return [-1]
        va1 = jstx[jst]
        # 判断用户时否需要优先执行特定库 task 库/脚本.js
        ta = yam['library'] + jst
        lis = list(va1.keys())
        return [va1[ta]['id'] if ta in lis else va1[lis[0]]['id']]
    except Exception as e:
        logger.write_log(f'查询任务异常信息: {e}')
        return [-1]


def contrast(str12):
    """
    去除掉相同脚本参数,如果脚本相同只执行一次
    :param str12: 活动参数
    :return: 有返回[-1] 没有返回[0,活动的关键字]
    """
    try:
        # 提取脚本关键部分,并且不提取链接
        str0 = re.findall('^export .*?="(.*?=?\w+)"', str12)
        if str0:
            str1 = ''
            for i in range(len(str0)):
                if not re.findall('^export NOT_TYPE=', str0[i]):
                    aa = re.findall('^https://\w+-isv\.is\w+\.com$', str0[i])
                    if len(aa) == 0:
                        # 把提取到的关键内容
                        str1 = str0[i].split('=')[-1]
                        break
            inquire = conn.selectTopone(table=conn.surface[1], where=f"jd_value1='{str1}'")
            if inquire:
                # logger.write_log(f'检测到活动已经执行过本次跳过执行本次参数 {str12} 之前执行的参数关键字 {inquire[0]}')
                return [-1]
            else:
                return [0, str1]
        else:
            return [0, '']
    except Exception as e:
        logger.write_log('去掉相同活动异常: ', e)
        return -1
