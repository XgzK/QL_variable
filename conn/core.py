import re

from conn.get_value import get_main
from conn.gheaders.conn import read_yaml
from conn.gheaders.log import LoggerClass
from conn.ql.ql import QL
from conn.ql.ql_token import ql_compared, ql_write

jstx = read_yaml()
ql = QL()
logger = LoggerClass('debug')


def main_core(va):
    """
    主要功能运行,每15分钟运行一次
    :param va: 青龙版本
    :return:
    """
    # 判断运行必备参数是否发送了异常
    if jstx['judge'] == 0:
        li = get_main()
        # 判断是否有任务
        if len(li) != 0:
            # 遍历获取所有任务列表
            for i in range(len(li[0])):
                # 传入脚本名称返回任务ID
                ids = ql_compared(li[0][i], va)
                # 判断是否有脚本
                if ids[0] != -1:
                    # 处理数据和去判断是否去重复,返回处理过的参数
                    judge = ql_write(li[1][i])
                    # 返回-1表示有异常
                    if judge != -1:
                        # 获取配置文件的内容
                        content = ql.configs_check('config.sh')
                        # 如果青龙返回200执行
                        if content["code"] == 200:
                            # 获取配置文件内容
                            bytex = content['data']
                            # 向青龙配置文件添加活动
                            revise = ql.configs_revise('config.sh', str(bytex) + str(judge))
                            # 表示添加活动成功
                            if revise["code"] == 200:
                                # 根据脚本id，执行脚本
                                qid = ql.ql_run(ids)
                                if qid == 0:
                                    logger.write_log(f"执行 {li[0][i]} 脚本成功 ID {ids[0]}")
                            # 把原来内容添加回去
                            ql.configs_revise('config.sh', bytex)
                else:
                    logger.write_log(f"{li[0][i]} 脚本没有找到")
        else:
            logger.write_log(f"本次没有任务，{jstx['time']}分钟后再次运行")
    else:
        logger.write_log("异常问题：conn.yml文件中judge设置为false,表示配置异常")


def adaptation():
    """
    根本版本不同而做不同适配
    :return:
    """
    qlv = ql.system_version()
    if qlv != -1:
        qlv = re.findall('\d+\.(\d+)\.\d+', qlv)
        return qlv[0]
    else:
        return -1
