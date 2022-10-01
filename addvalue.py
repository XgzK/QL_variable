import json
import threading
import time

from flask_apscheduler import APScheduler

from conn.gheaders.Inspector import Check
from conn.gheaders.conn import read_yaml
from conn.gheaders.log import LoggerClass
from conn.ql.ql import QL
from conn.ql.ql_token import token_main
from conn.sql.addsql import dele_datati
from conn.web.ql_web import run_web
from conn.fo.core import main_core, adaptation

logger = LoggerClass('debug')
scheduler = APScheduler()
yml = read_yaml()
ql = QL()


@scheduler.task('interval', id='timing_ck', days=15)
def timing_ck():
    """
    设置每半个月获取一次新的ck,青龙作者是的是一个月保质期，不过这里设置为半个月
    :return:
    """
    for i in range(3):
        ck = token_main()
        if ck == 0:
            logger.write_log("新的Bearer添加成功token_main")
            return 0
        logger.write_log("新的Bearer添加失败, 20s后再次获取")
        time.sleep(20)
    logger.write_log("新的Bearer添加失败停止执行后面步骤")
    return -1


@scheduler.task('interval', id='list', minutes=30)
def ql_crons():
    """
    获取青龙任务列表
    :return:
    """
    try:
        js = ql.crons()
        with open(yml['json'], mode='wt', encoding='utf-8') as f:
            json.dump(js, f, ensure_ascii=False)
            f.close()
        return 0
    except Exception as e:
        logger.write_log(f'获取列表异常,{e}')
        return -1


@scheduler.task('interval', id='immortal_main', minutes=yml['time'])
def immortal_main():
    """
    主要功能运行,特定分钟运行一次
    :return:
    """
    main_core(val)


@scheduler.task('interval', id='ti_ck', days=1)
def ti_ck():
    """
    定时清空数据库
    :return:
    """
    dele_datati()


def mai():
    """
    执行主要程序
    :return:
    """
    tf = True
    while tf:
        ym = read_yaml()
        if ym['ip'] != '' and ym['Client ID'] != '' and ym['Client Secret'] != '':
            # 创建一些路径和数据库
            Check().cpath()
            global val
            val = adaptation()
            if val != -1:
                # 定时任务第一次不会执行，所以手动添加一次
                ck = timing_ck()
                cr = ql_crons()
                if ck == 0 and cr == 0:
                    logger.write_log("连接青龙端成功")
                    tf = False
                else:
                    logger.write_log("连接青龙端失败,定时任务不启动,请重新输入")
                    # 20秒检测一次
                    time.sleep(20)
            else:
                logger.write_log("无法获取版本号,程序无法自动适配")
                # 20秒检测一次
                time.sleep(20)
        else:
            # 15秒检测一次
            time.sleep(20)
    immortal_main()
    # 添加定时任务
    scheduler.start()


if __name__ == '__main__':
    t1 = threading.Thread(target=mai, args=())
    t1.start()
    run_web()
