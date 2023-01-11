import time

from com import q, Mark
from com.gheaders.conn import read_yaml
from com.gheaders.log import LoggerClass
from com.ql import ql
from com.ql.ql_token import ql_compared, ql_write, contrast
from com.sql import Sql

conn = Sql()
logger = LoggerClass()
ql_js = 'qlva.sh'
ql_cks = []
# 添加配置文件的内容
bytex = ""
# 时间
delay = time.time() + 3600

def main_core():
    """
    主要功能运行
    data: [脚本名称,活动参数]
    :return:
    """

    # 先获取一遍,并加入全局
    global ql_cks, bytex, delay
    ql_cks = conn.selectAll(table=conn.surface[3], where="state=0")

    while True:
        # [脚本, 活动, 活动值, 时间]
        data = q.get()
        # 表示已经没有任务了
        if q.qsize() <= 2 and ql_cks and delay < time.time():
            logger.write_log("清空添加的内容")
            bytex = ""
            delay = time.time() + 3600
            for i in ql_cks:
                # 把原来内容添加回去
                ql.configs_revise(ql_js, '', ql_cks[i])

        # 如果在任务里边
        if data['jd_js'] in Mark:
            if int(Mark[data['jd_js']]['time']) < int(time.time()):
                # 删除这个值
                Mark.pop(data['jd_js'])
                logger.write_log(f"脚本 {data['jd_js']} 的时间到了出去玩耍吧, 后面排队的还有 {q.qsize()}")
            else:
                q.put(Mark[data['jd_js']])
                logger.write_log(f"脚本 {data['jd_js']} 刚刚才出去被扔到后面排队了 号码为 {q.qsize()}")
                q.task_done()
                time.sleep(8)
                continue
        # 加入执行值任务
        data['time'] = int(time.time()) + int(data['interval'])
        Mark.setdefault(data['jd_js'], data)

        jst = read_yaml()
        if data['jd_js'] in jst['prohibit']:
            logger.write_log(f'脚本 {data["jd_js"]} 被你的主人狠心的拖进小黑屋关了永久禁闭')
            q.task_done()
            continue

        ql_cks = conn.selectAll(table=conn.surface[3], where="state=0")
        if not ql_cks:
            q.task_done()
            logger.write_log("主人你好像没有对接青龙或者没有给我发送 /start")
            continue

        # 检测是否被执行过
        ctr = contrast(data["activities"])
        # 执行过返回-1结束
        if ctr[0] == -1:
            q.task_done()
            continue

        # 遍历青龙容器
        for j in range(len(ql_cks)):

            # 传入脚本名称返回任务ID
            ids = ql_compared(data["jd_js"], ql_cks[j])
            # 判断是否有脚本
            if ids[0] == -1:
                logger.write_log(f"脚本 {data['jd_js']} 没有找到, 请主人别忘记找寻缺失的一部分哦")
                continue

            judge = ql_write(data["activities"], jst, ctr[1], j)
            # 返回-1表示有异常
            if judge == -1:
                logger.write_log(f"脚本 {data['jd_js']} 任务关键字 {ctr[1]} 已经被执行过")
                continue

            # 向青龙配置文件添加活动
            revise = ql.configs_revise(ql_js, bytex + '\n' + judge, ql_cks[j])
            bytex += '\n' + judge

            # 表示添加活动成功
            if revise["code"] == 200:
                # 根据脚本id，执行脚本
                qid = ql.ql_run(ids, ql_cks[j])
                if qid == 0:
                    logger.write_log(
                        f"已经帮主人你把 {ql_cks[j][0]} 的朋友执行 {data['jd_js']} 脚本成功 ID {ids[0]} 执行参数: {data['activities']}")
            else:
                logger.write_log(f"{ql_cks[j][0]}异常问题,请主人给我进入你小金库的权限我需要 的权限有 定时任务权限 和 配置文件权限, 否则无法吧金克拉放入主人小金库", level='error')
        q.task_done()
