import threading

from apscheduler.schedulers.background import BackgroundScheduler

from com.bot.information import Interact
from com.bot.whiles import WhileLong
from com.fo.core import Main_core
from com.fo.father import Father
from com.gheaders.Inspector import Check
from com.gheaders.conn import ConnYml
from com.ql.ql_timing import Timing
from com.Web.htws import app, socketio

timing = Timing()
main_core = Main_core()
whileLong = WhileLong()
interact = Interact()
yml = ConnYml()

class RunMain(Father):

    def __init__(self):
        super().__init__()
        yml.creat_yml()
        self.chech = Check()

    def ti_ck(self):
        """
        定时清空数据库
        :return:
        """
        self.log_object.read_log()
        st = timing.clear_list()

        if st:
            interact.distribute(f"{st}\n上面已经被删除,如需使用重新提交")

    def timing_ck(self):
        """
        设置每半个月获取一次新的ck,青龙作者是的是一个月保质期，不过这里设置为半个月
        :return: 0 or -1
        """
        st = timing.check_ct()
        if st:
            interact.distribute(f"{st}\n上面已经被删除,如需使用重新提交")

    def run_web(self):
        socketio.run(app,
                     debug=False,
                     log_output=False,
                     host='0.0.0.0',
                     port=5008)

    def bot_main(self):
        Check().cpath()
        scheduler = BackgroundScheduler()
        # 使用多线程防止任务阻塞
        t1 = threading.Thread(target=self.run_web)
        t2 = threading.Thread(target=main_core.main_while)

        t1.start()

        scheduler.add_job(self.ti_ck, 'interval', hours=12)
        scheduler.add_job(self.timing_ck, 'interval', days=15)
        scheduler.start()

        self.timing_ck()
        self.ti_ck()
        t2.start()
        self.log_write("云端数据库同步成功") if self.chech.sql() == 0 else self.log_write("云端数据库同步失败")
        whileLong.old_message()
        whileLong.new_message()


if __name__ == '__main__':
    RunMain().bot_main()
