import threading
import time

from flask_apscheduler import APScheduler
from engineio.async_drivers import gevent

from com.bot import tg_mes
from com.bot.information import Interact
from com.fo.core import main_core
from com.gheaders.Inspector import Check
from com.gheaders.conn import read_yaml
from com.gheaders.log import LoggerClass
from com.ql.ql_timing import Timing
from com.txt.txt_zli import tx_revise
from com.Web.htws import app, socketio

scheduler = APScheduler()
interact = Interact()
timing = Timing()
logger = LoggerClass('debug')

@scheduler.task('interval', id='ti_ck', hours=12)
def ti_ck():
    """
    定时清空数据库
    :return:
    """
    st = timing.clear_list()
    if st:
        tg_mes.send_message(f"{st}\n上面已经被删除,如需使用重新提交", yml["Administrator"])


@scheduler.task('interval', id='timing_ck', days=15)
def timing_ck():
    """
    设置每半个月获取一次新的ck,青龙作者是的是一个月保质期，不过这里设置为半个月
    :return: 0 or -1
    """
    st = timing.check_ct()
    if st:
        tg_mes.send_message(f"{st}\n上面已经被删除,如需使用重新提交", yml["Administrator"])


def run_web():
    socketio.run(app,
                 debug=False,
                 log_output=False,
                 host='0.0.0.0',
                 port=5008)


if __name__ == '__main__':
    Check().cpath()
    # 使用多线程防止任务阻塞
    t1 = threading.Thread(target=run_web)
    t1.start()
    # 启动定时任务
    scheduler.start()
    timing_ck()
    ti_ck()
    t2 = threading.Thread(target=main_core)
    t2.start()
    # 先执行清理掉之前的记录
    ids = True
    while ids:
        yml = read_yaml()
        if yml['Token']:
            tg_ms = tg_mes.get_long_link(ti=1)
            if tg_ms['ok'] and tg_ms['result']:
                tg_mes.data['offset'] = tg_ms["result"][len(tg_ms["result"]) - 1]['update_id'] + 1
            else:
                ids = False
        else:
            time.sleep(10)
            logger.write_log("没有提交必要参数机器人Token,不进行下一步执行")
    while True:
        try:
            yml = read_yaml()
            tg_ms = tg_mes.get_long_link()
            # 消息不为空和没有异常
            if not tg_ms['ok']:
                logger.write_log(f"异常消息 {tg_ms['result'][0]} 触发异常停止10秒")
                time.sleep(10)
                continue
            if tg_ms["result"]:
                # 确认收到消息
                tg_mes.data['offset'] = tg_ms["result"][len(tg_ms["result"]) - 1]['update_id'] + 1
                for result in tg_ms["result"]:
                    # message 一般是 私聊 群消息 加入群组 and 是消息而非加入群组
                    if 'message' in result and "chat" in result['message']:
                        # 跳过转发频道或群
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
                                # logger.write_log(f"收到群消息内容 {result['message']['text']}")
                                tx_revise(result['message']['text'])
                                interact.group_id(result)
                                if 'sender_chat' in result['message'] and yml['Send_IDs']:
                                    interact.distribute(result['message']['text'], yml['Send_IDs'])
                            # 加入群聊
                            elif 'new_chat_member' in result['message']:
                                tg_mes.banChatMember(result, '-1001565778760',
                                                     result['message']['new_chat_member']['id'])
                    # 频道消息
                    elif 'channel_post' in result:
                        if result['channel_post']['chat']['type'] == 'channel':
                            if 'text' in result['channel_post']:
                                # logger.write_log(f"收到频道监控消息内容 {result['channel_post']['text']}")
                                tx_revise(result['channel_post']['text'])
                                if yml['Send_IDs']:
                                    interact.distribute(result['channel_post']['text'], yml['Send_IDs'])
        except Exception as e:
            logger.write_log(f"个人开发类异常: {e}")
