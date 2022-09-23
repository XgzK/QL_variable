import json
import threading
import time

from flask_apscheduler import APScheduler

from conn.gheaders.Inspector import Check
from conn.gheaders.conn import read_yaml
from conn.gheaders.log import LoggerClass
from conn.ql.ql import QL
from conn.ql.ql_token import token_main
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
    token_main()


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
    except Exception as e:
        logger.write_log(f'获取列表异常,{e}')


@scheduler.task('interval', id='immortal_main', minutes=yml['time'])
def immortal_main():
    """
    主要功能运行,特定分钟运行一次
    :return:
    """
    main_core(val)


def mai():
    """
    执行主要程序
    :return:
    """
    tf = True
    while tf:
        ym = read_yaml()
        if ym['ip'] != '' and ym['Client ID'] != '' and ym['Client Secret'] != '':
            tf = False
        else:
            # 10秒检测一次
            time.sleep(10)
    # 创建一些路径和数据库
    Check().cpath()
    global val
    val = adaptation()
    # 定时任务第一次不会执行，所以手动添加一次
    timing_ck()
    ql_crons()
    immortal_main()
    # 添加定时任务
    scheduler.start()


if __name__ == '__main__':
    t1 = threading.Thread(target=mai, args=())
    t1.start()
    run_web()
