import requests

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
        print("token_main败，请检查conn.yml文件，异常信息：" + str(e))
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
        for i in jstx:
            if i['command'].split('/')[-1] == jst:
                # 适配版本10
                if int(va) == 10:
                    return [i['_id']]
                else:
                    return [i['id']]
        return [-1]
    except Exception as e:
        print('异常信息',e)
        return [-1]
