import time

from conn import q
from conn.ql.ql import QL
from conn.tools.log import LoggerClass
from conn.tools.sql import Sql
from .sundries import Sundries


class Main_core():
    """
    执行类
    """

    def __init__(self):
        super().__init__()
        self.ql_js = 'qlva.sh'
        self.ql_cks = []
        # 添加配置文件的内容
        self.Mark = {}
        self.conn = Sql()
        self.ql = QL()
        self.logger = LoggerClass()
        self.sundries = Sundries()

    def main_while(self):
        while True:
            data = q.get()
            self.sundries.marking_time()
            # 检测是否需要跳过
            team = self.Team(data)
            if not team:
                q.task_done()
                continue

            # 检测是否被执行过
            ctr = self.sundries.contrast(data)
            # 执行过返回-1结束
            if ctr[0] == -1:
                q.task_done()
                self.logger.write_log(f"识别关键字异常: {data['activities']}")
                time.sleep(2)
                continue
            elif ctr[0] == 3:
                self.logger.write_log(f"没有识别到关键字: {data['activities']}")
                q.task_done()
                time.sleep(2)
                continue
            elif ctr[0] == 1:
                self.logger.write_log(f"识别到关键字已经执行过了, 关键字: {ctr[1]}")
                q.task_done()
                time.sleep(2)
                continue

            # 转发
            self.sundries.interaction.for_message(data['activities'])

            self.ql_cks = self.conn.selectAll(table=self.conn.surface[3], where="state=0")
            if not self.ql_cks:
                q.task_done()
                self.logger.write_log("主人你好像没有对接青龙或者没有给我发送 /start")
                time.sleep(15)
                continue

            # 加入数组伪装队列
            data['time'] = int(time.time()) + int(data['interval'])
            self.Mark.setdefault(data['jd_js'], data)

            self.execution_ql(data, ctr)
            q.task_done()

    def Team(self, data):
        """
        伪造队列，如果不在规定时间会让任务重新排队
        :return:
        """
        # 检测是否值1小黑屋
        if data['jd_js'] in self.sundries.AdReg.get('prohibit'):
            self.logger.write_log(f'脚本 {data["jd_js"]} 被你的主人狠心的拖进小黑屋关了永久禁闭')
            return False

        # 如果在任务里边
        if data['jd_js'] in self.Mark:
            if int(self.Mark[data['jd_js']]['time']) < int(time.time()):
                # 删除这个值
                self.Mark.pop(data['jd_js'])
                self.logger.write_log(f"脚本 {data['jd_js']} 的时间到了出去玩耍吧, 后面排队的还有 {q.qsize()}")
                return True
            else:
                q.put(self.Mark[data['jd_js']])
                self.logger.write_log(f"脚本 {data['jd_js']} 刚刚才出去被扔到后面排队了 号码为 {q.qsize()}")
                # 根据队列执行不同的时间
                sun = q.qsize()
                if sun < 5:
                    time.sleep(int(data['interval']) / 2)
                elif sun < 10:
                    time.sleep(int(data['interval']) / 4)
                elif sun < 20:
                    time.sleep(3)
                else:
                    time.sleep(1)
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
            ids = self.sundries.ql_compared(data["jd_js"], self.ql_cks[j])
            # 判断是否有脚本
            if ids[0] == -1:
                # 如果没有这个任务就去转换多适配
                # 把参数传递进去
                url = self.sundries.turn_url(data["activities"])
                # 没有获取到
                if not url:
                    self.logger.write_log(f"脚本 {data['jd_js']} 活动参数 {data['activities']} 没有找到, 开始进行系列脚本匹配")
                    continue
                # 记录是否被执行
                tf1 = True
                for va in url:
                    text_list = self.sundries.https_txt(va)
                    if not text_list:
                        continue
                    for ji in text_list:
                        # 把原来的data部分内容替换
                        data["jd_js"] = ji[1].jd_js
                        data['activities'] = ji[0]
                        ids = self.sundries.ql_compared(data["jd_js"], self.ql_cks[j])
                        if ids[0] == -1:
                            continue
                        self.for_ql(j, data, ctr, ids)
                        tf1 = False
                        # 结束这个方法
                        break
                    if tf1:
                        self.logger.write_log(f"系列脚本缺失提醒: {url[0]}")
                        continue
            else:
                # 如果有这个任务就执行
                self.for_ql(j, data, ctr, ids)
        # 脚本结束自定义延迟时间
        time.sleep(self.sundries.AdReg.get('Delay') if 'Delay' in self.sundries.AdReg.keys() else 0)

    def for_ql(self, j, data, ctr, ids) -> bool:
        """
        对execution_ql方法进行拆分出来的后半部分
        :return:
        """
        if j == 0:
            # 把关键字添加到数据库
            self.sundries.ql_write(data, ctr)
        # 向青龙配置文件添加活动
        revise = self.ql.configs_revise(self.ql_js, data["activities"], self.ql_cks[j])

        # 表示添加活动成功
        if revise["code"] == 200:
            # 根据脚本id，执行脚本
            qid = self.ql.ql_run(ids, self.ql_cks[j])
            if qid == 0:
                self.logger.write_log(
                    f"已经帮主人你把 {self.ql_cks[j][0]} 的小金库填充 {data['jd_js']} 脚本成功 ID {ids[0]} 执行参数: {data['activities']}")

            time.sleep(2)
            self.ql.configs_revise(self.ql_js, '', self.ql_cks[j])
            return True
        else:
            self.logger.write_log(
                f"{self.ql_cks[j][0]}异常问题,请主人给我进入你小金库的权限我需要 的权限有 定时任务权限 和 配置文件权限, 否则无法吧金克拉放入主人小金库",
                level='error')
            return False
