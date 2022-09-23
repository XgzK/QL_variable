import re

from conn.gheaders.conn import read_yaml
from conn.gheaders.log import LoggerClass
from conn.gheaders.ti import date_minutes
from conn.ql.ql import QL
from conn.gheaders.conn import yml_file
from conn.sql.addsql import insert_data, select_datati

logger = LoggerClass('debug')
ql = QL()
yam = read_yaml()


def token_main():
    """
    主要用于调用ck
    :return:
    """
    try:
        ck = ql.ql_tk()

        if ck != 0:
            str1 = 'Authorization:' + f" '{ck}'"
            yml_file(str1, read_yaml()['Record']['Authorization'])
            logger.write_log("新的Bearer添加成功token_main")
            yml_file("judge: 0", read_yaml()['Record']['judge'])
        else:
            logger.write_log("新的Bearer添加失败,token_main")
            # 如果异常就向conn.yml添加一个值 1
            yml_file("judge: 1", read_yaml()['Record']['judge'])
    except Exception as e:
        logger.write_log("token_main败，请检查conn.yml文件，异常信息：" + str(e))


def ql_write(str12):
    """
    写入青龙任务配置文件
    :param str12: 传入内容
    :return: 如果没有执行过返回0，如果执行过返回-1
    """
    try:
        # 判断是否去重数据
        if yam['deduplication'] == 0:
            # 针对某些不需要去重复的数据，如果不是exp则不去重复
            if str12[:3] == "exp":
                # 添加到数据库，如果成功添加表示之前没有运行过
                st = insert_data(str12, date_minutes())
                # 如果数据库中没有存在则返回原值
                if int(st) == 0:
                    return str12
                else:
                    inquire = select_datati(str12)
                    logger.write_log("参数已经执行过" + str(str12) + "不再重复执行")
                    logger.write_log(f"在 {inquire[0][1]} 数据库中参数是 {inquire[0][0]} 所以不再重复执行")
                    return -1
            else:
                # 把后端添加的NOT不去重标记去掉
                return str12[3:]
        else:
            # 不去重复
            if str12[:3] == "exp":
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
        #  task 库/脚本.js
        if jstx != '/':
            ku = yam['library'] + jst
            for i in jstx:
                # 直接不分隔用最完整的格式百分之百匹配
                if i['command'] == ku:
                    # 适配版本10
                    if int(va) == 10:
                        return [i['_id']]
                    else:
                        return [i['id']]
        # 找到脚本立即停止
        for i in jstx:
            if i['command'].split('/')[-1] == jst:
                # 适配版本10
                if int(va) == 10:
                    return [i['_id']]
                else:
                    return [i['id']]
        return [-1]
    except Exception as e:
        logger.write_log('查询任务异常信息: ',e)
        return [-1]


def contrast(str12):
    """
    去除掉相同脚本参数,如果脚本相同只执行一次
    :param str12: 活动参数
    :return: 有返回-1 没有返回0
    """
    try:
        # 提取脚本关键部分
        str1 = re.findall('export .*?="(.*?=?\w+)"', str12)
        a1 = str1[0].split('=')
        inquire = select_datati('*')
        for i in inquire:
            aa = re.findall('export .*?="(.*?=?\w+)"', i[0])
            a2 = aa[0].split('=')[-1]
            if a1[-1] == a2:
                logger.write_log(f'检测到活动已经执行过本次跳过执行本次参数 <br>{str12} <br>之前执行的参数 {i[0]}')
                return -1
        return 0
    except Exception as e:
        logger.write_log('去掉相同活动异常: ', e)
        return -1



