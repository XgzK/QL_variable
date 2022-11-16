import json
import re
import threading
import time

from flask_apscheduler import APScheduler

from com.bot import tg_mes
from com.bot.information import Interact
from com.gheaders.Inspector import Check
from com.gheaders.conn import read_yaml
from com.ql import ql
from com.gheaders import logger
from com.ql.ql_token import token_main
from com.sql import conn
from com.txt.txt_zli import tx_revise
from com.web.ql_web import run_web

scheduler = APScheduler()
yml = read_yaml()


@scheduler.task('interval', id='ti_ck', hours=12)
def ti_ck():
    """
    定时清空数据库
    :return:
    """
    conn.delete(table=conn.surface[1])
    try:
        js_ql = ql.crons()
        js = dict()
        # 如果青龙里面有层data就解包
        for i in js_ql['data'] if 'data' in js_ql else js_ql:
            aa = re.findall('task .*?/([a-zA-Z0-9&=_/-]+\.\w+)', i['command'])
            if aa:
                if not (aa[0] in js):
                    js[aa[0]] = {}
                # 用来区分 版本json格式差异
                if 'id' in i:
                    js[aa[0]].setdefault(i['command'], {'id': i['id'], "name": i["name"], "isDisabled": i["isDisabled"]})
                else:
                    js[aa[0]].setdefault(i['command'], {'id': i['_id'], "name": i["name"], "isDisabled": i["isDisabled"]})
            else:
                logger.write_log(f"跳过录入: {i['command']}")
        with open(yml['json'], mode='w+', encoding='utf-8') as f:
            json.dump(js, f, ensure_ascii=False)
        return 0
    except Exception as e:
        logger.write_log(f'获取列表异常,{e}')
        return -1


@scheduler.task('interval', id='timing_ck', days=15)
def timing_ck():
    """
    设置每半个月获取一次新的ck,青龙作者是的是一个月保质期，不过这里设置为半个月
    :return: 0 or -1
    """
    for i in range(3):
        ck = token_main()
        if ck == 0:
            return 0
        logger.write_log("新的Bearer添加失败, 30s后再次获取")
        time.sleep(30)
    logger.write_log("新的Bearer添加失败停止执行后面步骤")
    return -1


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
            # 获取必备青龙参数
            ck = timing_ck()
            cr = ti_ck()
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


interact = Interact()

if __name__ == '__main__':
    # 使用多线程防止任务阻塞
    t1 = threading.Thread(target=run_web)
    t1.start()
    mai()
    # 先执行清理掉之前的记录
    ids = True
    while ids:
        tg_ms = tg_mes.get_long_link(ti=1)
        if tg_ms['ok'] and tg_ms['result']:
            tg_mes.data['offset'] = tg_ms["result"][len(tg_ms["result"]) - 1]['update_id'] + 1
        else:
            ids = False
    while True:
        try:
            yml = read_yaml()
            tg_ms = tg_mes.get_long_link()
            # 消息不为空和没有异常
            if tg_ms['ok']:
                if tg_ms["result"]:
                    # 确认收到消息
                    tg_mes.data['offset'] = tg_ms["result"][len(tg_ms["result"]) - 1]['update_id'] + 1
                    for result in tg_ms["result"]:
                        # message 一般是 私聊 群消息 加入群组 and 是消息而非加入群组
                        if 'message' in result and "chat" in result['message']:
                            if 'sender_chat' in result['message'] and yml['Send_IDs'] == \
                                    result['message']['sender_chat']['id']:
                                continue
                            # 私聊消息
                            if result['message']['chat']['type'] == 'private':
                                if 'text' in result['message']:
                                    logger.write_log(f"收到私聊消息内容 {result['message']['text']}")
                                    interact.get_id(result)
                                    tx_revise(result['message']['text'])
                            # 群消息 supergroup 公开群 group 非公开群 公开后再私有还是 supergroup
                            elif result['message']['chat']['type'] == 'supergroup' or result['message']['chat'][
                                'type'] == 'group':
                                if 'text' in result['message']:
                                    logger.write_log(f"收到群消息内容 {result['message']['text']}")
                                    tx_revise(result['message']['text'])
                                    interact.group_id(result)
                                    if 'sender_chat' in result['message'] and yml['Send_IDs']:
                                        interact.distribute(result['message']['text'], yml['Send_IDs'])
                        # 频道消息
                        elif 'channel_post' in result:
                            if result['channel_post']['chat']['type'] == 'channel':
                                if 'text' in result['channel_post']:
                                    logger.write_log(f"收到频道监控消息内容 {result['channel_post']['text']}")
                                    tx_revise(result['channel_post']['text'])
                                    if yml['Send_IDs']:
                                        interact.distribute(result['channel_post']['text'], yml['Send_IDs'])
            else:
                logger.write_log(f"异常消息 {tg_ms['result']} 触发异常停止10秒")
                time.sleep(10)
        except Exception as e:
            logger.write_log(f"个人开发类异常: {e}")
