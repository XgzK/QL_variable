import time

from com import q
from com.gheaders.conn import read_yaml
from com.ql import QL
from com.ql.ql_token import contrast, ql_compared, ql_write
from com.sql import Sql


# conn = Sql()
# logger = LoggerClass()
# ql_js = 'qlva.sh'
# ql_cks = []
# # 添加配置文件的内容
# bytex = ""
# # 时间
# delay = time.time() + 3600


class Main_core(Sql, QL):
    """
    执行类
    """

    def __init__(self):
        super().__init__()
        Sql.__init__(self)
        QL.__init__(self)
        # self.level = 'info'
        self.ql_js = 'qlva.sh'
        self.ql_cks = []
        # 添加配置文件的内容
        self.bytex = ""
        # 时间
        self.delay = time.time() + 3600
        self.q = q
        self.yml = read_yaml()
        self.Mark = {}

    def main_while(self):
        while True:
            data = self.q.get()
            # 表示已经没有任务了,清理配置文件和内容
            if q.qsize() <= 4 and self.ql_cks and self.delay < time.time():
                self.write_log("清空添加的内容")
                self.bytex = ""
                self.delay = int(time.time()) + 3600
                for i in self.ql_cks:
                    # 把原来内容添加回去
                    self.configs_revise(self.ql_js, '', i)

            # 检测是否需要跳过
            team = self.Team(data)
            if not team:
                self.q.task_done()
                continue

            self.ql_cks = self.selectAll(table=self.surface[3], where="state=0")
            if not self.ql_cks:
                self.q.task_done()
                self.write_log("主人你好像没有对接青龙或者没有给我发送 /start")
                continue

            # 检测是否被执行过
            ctr = contrast(data["activities"])
            # 执行过返回-1结束
            if ctr[0] == -1:
                self.q.task_done()
                continue

            data['time'] = int(time.time()) + int(data['interval'])
            self.Mark.setdefault(data['jd_js'], data)

            self.execution_ql(data, ctr)
            self.q.task_done()

    def Team(self, data):
        """
        伪造队列，如果不在规定时间会让任务重新排队
        :return:
        """
        self.yml = read_yaml()
        # 检测是否值1小黑屋
        if data['jd_js'] in self.yml['prohibit']:
            self.write_log(f'脚本 {data["jd_js"]} 被你的主人狠心的拖进小黑屋关了永久禁闭')
            return False

        # 如果在任务里边
        if data['jd_js'] in self.Mark:
            if int(self.Mark[data['jd_js']]['time']) < int(time.time()):
                # 删除这个值
                self.Mark.pop(data['jd_js'])
                self.write_log(f"脚本 {data['jd_js']} 的时间到了出去玩耍吧, 后面排队的还有 {q.qsize()}")
                return True
            else:
                self.q.put(self.Mark[data['jd_js']])
                self.write_log(f"脚本 {data['jd_js']} 刚刚才出去被扔到后面排队了 号码为 {q.qsize()}")
                # 根据队列执行不同的时间
                sun = q.qsize()
                if sun < 5:
                    time.sleep(int(data['interval']) / 2)
                elif sun < 10:
                    time.sleep(int(data['interval']) / 4)
                elif sun < 15:
                    time.sleep(2)
                return False

        return True

    def execution_ql(self, data, ctr):
        """
        执行青龙任务
        :return:
        """
        # 遍历青龙容器
        for j in range(len(self.ql_cks)):

            # 传入脚本名称返回任务ID
            ids = ql_compared(data["jd_js"], self.ql_cks[j])
            # 判断是否有脚本
            if ids[0] == -1:
                self.write_log(f"脚本 {data['jd_js']} 没有找到, 请主人别忘记找寻缺失的一部分哦")
                continue

            judge = ql_write(data["activities"], self.yml, ctr[1], j)
            # 返回-1表示有异常
            if judge == -1:
                self.write_log(f"脚本 {data['jd_js']} 任务关键字 {ctr[1]} 已经被执行过")
                return

            # 向青龙配置文件添加活动
            revise = self.configs_revise(self.ql_js, self.bytex + '\n' + judge, self.ql_cks[j])
            self.bytex += '\n' + judge

            # 表示添加活动成功
            if revise["code"] == 200:
                # 根据脚本id，执行脚本
                qid = self.ql_run(ids, self.ql_cks[j])
                if qid == 0:
                    self.write_log(
                        f"已经帮主人你把 {self.ql_cks[j][0]} 的小金库填充 {data['jd_js']} 脚本成功 ID {ids[0]} 执行参数: {data['activities']}")
            else:
                self.write_log(
                    f"{self.ql_cks[j][0]}异常问题,请主人给我进入你小金库的权限我需要 的权限有 定时任务权限 和 配置文件权限, 否则无法吧金克拉放入主人小金库",
                    level='error')
