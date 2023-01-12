import threading

from flask_apscheduler import APScheduler

from com.bot import tg_mes
from com.bot.information import Interact
from com.bot.whiles import WhileLong
from com.fo.core import Main_core
from com.gheaders.Inspector import Check
from com.gheaders.conn import read_yaml
from com.gheaders.log import LoggerClass, rz
from com.initialization import Implement
from com.ql.ql_timing import Timing
from com.Web.htws import app, socketio

scheduler = APScheduler()
interact = Interact()
timing = Timing()
logger = LoggerClass('debug')
whileLong = WhileLong()
yml = read_yaml()
implement = Implement()
main_core = Main_core()

@scheduler.task('interval', id='ti_ck', hours=12)
def ti_ck():
    """
    定时清空数据库
    :return:
    """
    rz()
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
    t2 = threading.Thread(target=main_core.main_while)
    t1.start()
    # 启动定时任务
    scheduler.start()
    timing_ck()
    ti_ck()
    t2.start()
    logger.write_log("云端数据库同步成功") if implement.sql() == 0 else logger.write_log("云端数据库同步失败")
    whileLong.old_message()
    whileLong.new_message()
