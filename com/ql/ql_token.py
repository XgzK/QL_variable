import datetime
import re

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
            yml_file("judge: 0", read_yaml()['Record']['judge'])
            return 0
        else:
            # 如果异常就向conn.yml添加一个值 1
            yml_file("judge: 1", read_yaml()['Record']['judge'])
            return -1
    except Exception as e:
        logger.write_log("token_main败，请检查conn.yml文件，异常信息：" + str(e))
        return -1


def ql_write(str12, yal):
    """
    写入青龙任务配置文件
    :param str12: 传入内容
    :param yal: conn.yml配置文件内容
    :return: 如果没有执行过返回0，如果执行过返回-1
    """
    try:
        # 针对某些不需要去重复的数据，如果不是exp则不去重复
        if str12[:3] == "exp":
            # 判断是否去重数据
            if yal['deduplication'] == 0:
                # 添加到数据库，如果成功添加表示之前没有运行过
                conn.insert(table=conn.surface[1], jd_value1=str12,
                                 jd_data=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            return str12
        else:
            # 把后端添加的NOT不去重标记去掉
            return str12[3:]
    except Exception as e:
        logger.write_log("ql_write,异常信息：" + str(e))
        return -1


def ql_compared(jst: str, va: int) -> list:
    """
    遍历青龙任务来对比,获取任务ID
    :param jst: 脚本名称
    :param va: 版本号
    :return: ID or -1
    """
    try:
        jstx = read_yaml(yam['json'])
        va1 = jstx if int(va) < 14 else jstx['data']
        #  task 库/脚本.js
        if yam['library'] != '/':
            ku = yam['library'] + jst
            for i in va1:
                # 直接不分隔用最完整的格式百分之百匹配
                if i['command'] == ku:
                    # 适配版本10
                    if int(va) == 10:
                        return [i['_id']]
                    else:
                        return [i['id']]
        for i in va1:
            if i['command'].split('/')[-1] == jst:
                # 适配版本10
                if int(va) == 10:
                    return [i['_id']]
                else:
                    return [i['id']]
        return [-1]
    except Exception as e:
        logger.write_log(f'查询任务异常信息: {e}')
        return [-1]


def contrast(str12):
    """
    去除掉相同脚本参数,如果脚本相同只执行一次
    :param str12: 活动参数
    :return: 有返回-1 没有返回0
    """
    try:
        print("进入匹配页面")
        # 提取脚本关键部分
        str1 = re.findall('export .*?="(.*?=?\w+)"', str12)
        print(str1)
        a1 = str1[0].split('=')
        print(a1)
        print('请求去重复数据库')
        inquire = conn.selectAll(table=conn.surface[1])
        for i in inquire:
            print(i)
            aa = re.findall('export .*?="(.*?=?\w+)"', i[0])
            # 如果返回有值对比
            if aa:
                a2 = aa[0].split('=')[-1]
                if a1[-1] == a2:
                    logger.write_log(f'检测到活动已经执行过本次跳过执行本次参数 {str12} 之前执行的参数 {i[0]}')
                    return -1
            else:
                logger.write_log(f'检测到活动失败跳过执行本次参数 {str12}')
                return -1
        return 0
    except Exception as e:
        logger.write_log('去掉相同活动异常: ', e)
        return -1
