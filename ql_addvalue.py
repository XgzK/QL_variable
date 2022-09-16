import json
import os
import re

from flask_apscheduler import APScheduler

from conn.Inspector import Check
from conn.get_value import get_main
from conn.gheaders.conn import read_yaml
from conn.gheaders.log import LoggerClass
# from conn.ql.ql_del import descend, ql_write, del_file
# from conn.ql.ql_list import vaguefind
from conn.ql.ql import QL
from conn.ql.ql_token import token_main, ql_write, ql_compared
from conn.web.ql_web import run_web

logger = LoggerClass('debug')
scheduler = APScheduler()
jstx = read_yaml()
ql = QL()


@scheduler.task('interval', id='timing_ck', days=15)
def timing_ck():
    """
    设置每半个月获取一次新的ck,青龙作者是的是一个月保质期，不过这里设置为半个月
    :return:
    """
    token_main()


@scheduler.task('interval', id='list', minutes=30)
def ql_crons():
    """
    获取青龙任务列表
    :return:
    """
    try:
        js = ql.crons()
        with open(jstx['json'], mode='wt', encoding='utf-8') as f:
            json.dump(js, f, ensure_ascii=False)
            f.close()
    except Exception as e:
        logger.write_log('获取列表异常', e)


@scheduler.task('interval', id='immortal_main', minutes=read_yaml()['time'])
def immortal_main():
    """
    主要功能运行,每15分钟运行一次
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
                ids = ql_compared(li[0][i])
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


if __name__ == '__main__':
    # 创建一些路径和数据库
    Check().cpath()
    # 定时任务第一次不会执行，所以手动添加一次
    # timing_ck()
    ql_crons()
    immortal_main()
    # 添加定时任务
    scheduler.start()
    run_web()
