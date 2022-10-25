import json
import threading
import time

from flask_apscheduler import APScheduler

from conn.bot import bot
from conn.gheaders.Inspector import Check
from conn.gheaders.conn import read_yaml
from conn.ql import ql
from conn.gheaders import logger
from conn.ql.ql_token import token_main
from conn.sql.addsql import dele_datati
from conn.txt.txt_zli import tx_revise
from conn.web.ql_web import run_web
from conn.fo.core import adaptation

scheduler = APScheduler()
yml = read_yaml()


@scheduler.task('interval', id='ti_ck', days=1)
def ti_ck():
    """
    定时清空数据库
    :return:
    """
    dele_datati()


@scheduler.task('interval', id='timing_ck', days=15)
def timing_ck():
    """
    设置每半个月获取一次新的ck,青龙作者是的是一个月保质期，不过这里设置为半个月
    :return: 0 or -1
    """
    for i in range(3):
        ck = token_main()
        if ck == 0:
            logger.write_log("新的Bearer添加成功token_main")
            return 0
        logger.write_log("新的Bearer添加失败, 30s后再次获取")
        time.sleep(30)
    logger.write_log("新的Bearer添加失败停止执行后面步骤")
    return -1


@scheduler.task('interval', id='list', minutes=30)
def ql_crons():
    """
    获取青龙任务列表
    :return: 0 or -1
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


@bot.message_handler(func=lambda m: True)
def ordinary(message):
    """
    私聊群聊消息
    :param message:
    :return:
    """
    print(message)
    tx_revise(message.text)



# @bot.channel_post_handler()
# def ordi(message):
#     """
#     频道消息
#     :param message:
#     :return:
#     """
#     print(message)


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
            # 把版本号传递给青龙
            ql.Version = adaptation()
            # 获取必备青龙参数
            ck = timing_ck()
            cr = ql_crons()
            if ck == 0 and cr == 0:
                logger.write_log("连接青龙端成功")
                # 结束循环
                tf = False
            else:
                logger.write_log("连接青龙端失败,定时任务不启动,请重新输入")
                # n秒检测一次
                time.sleep(20)
        else:
            logger.write_log("没有检测到青龙必要参数存在不继续向下执行后续功能")
            # n秒检测一次
            time.sleep(20)
    # 启动定时任务
    scheduler.start()


if __name__ == '__main__':
    # 使用多线程防止任务阻塞
    t1 = threading.Thread(target=run_web)
    t1.start()
    mai()
    bot.infinity_polling()
