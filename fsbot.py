import os
import threading

from apscheduler.schedulers.background import BackgroundScheduler

from conn.Template.ancestors import Father
from conn.Web.htws import app, socketio
from conn.bots.tgbot import Filter
from conn.mission.core import Main_core
from conn.ql.Timing import Timing
from conn.tools.Inspector import Check


class RunMain(Father):

    def __init__(self):
        super().__init__()
        self.yml.creat_yml()
        self.chech = Check()
        self.timing = Timing()
        self.filter = Filter()
        os.environ['marking_time'] = '0'
        self.core = Main_core()

    def ti_ck(self):
        """
        定时清空数据库
        :return:
        """
        self.log_object.read_log()
        self.timing.clear_list()

    def timing_ck(self):
        """
        设置每半个月获取一次新的ck,青龙作者是的是一个月保质期，不过这里设置为半个月
        :return: 0 or -1
        """
        self.timing.check_ct()

    def run_web(self):
        socketio.run(app,
                     debug=False,
                     log_output=False,
                     host='0.0.0.0',
                     port=5008)

    def bot_main(self):
        self.chech.cpath()
        scheduler = BackgroundScheduler()
        # 使用多线程防止任务阻塞
        t1 = threading.Thread(target=self.run_web)
        t2 = threading.Thread(target=self.core.main_while)

        t1.start()

        scheduler.add_job(self.ti_ck, 'interval', hours=12)
        scheduler.add_job(self.timing_ck, 'interval', days=15)
        scheduler.start()

        self.timing_ck()
        self.ti_ck()
        t2.start()
        self.log_write("云端数据库同步成功") if self.chech.sql() == 0 else self.log_write("云端数据库同步失败")
        self.filter.main_bots()


if __name__ == '__main__':
    RunMain().bot_main()
