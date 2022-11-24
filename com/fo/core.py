import time

from com import q
from com.gheaders.conn import read_yaml
from com.gheaders import logger
from com.ql import ql
from com.ql.ql_token import ql_compared, ql_write, contrast
from com.sql import Sql

# from com.sql import conn
conn = Sql()


def main_core():
    """
    主要功能运行
    data: [脚本名称,活动参数]
    :return:
    """
    while True:
        data = q.get()
        jst = read_yaml()
        tf = False
        if data[0] in jst['prohibit']:
            logger.write_log(f'检测到脚本 {data[0]} 在黑名单中,跳过执行')
            q.task_done()
            continue
        ql_ck = conn.selectAll(table=conn.surface[3], where="state=0")
        if not ql_ck:
            q.task_done()
            logger.write_log("没有提交青龙参数或者没有可以正常使用的青龙参数")
            continue
        # 检测是否被执行过
        ctr = contrast(data[1])
        # 执行过返回-1结束
        if ctr[0] == -1:
            q.task_done()
            continue
        # 遍历青龙容器
        for j in range(len(ql_ck)):
            # 传入脚本名称返回任务ID
            ids = ql_compared(data[0], ql_ck[j])
            # 判断是否有脚本
            if ids[0] == -1:
                logger.write_log(f"{data[0]} 脚本没有找到")
                continue
            judge = ql_write(data[1], jst, ctr[1], j)
            # 返回-1表示有异常
            if judge == -1:
                break
            # 获取配置文件的内容
            content = ql.configs_check('config.sh', ql_ck[j])
            # 如果青龙返回200执行
            if content["code"] == 200:
                # 获取配置文件内容
                bytex = content['data']
                # 向青龙配置文件添加活动
                revise = ql.configs_revise('config.sh', bytex + '\n' + judge, ql_ck[j])
                # 表示添加活动成功
                if revise["code"] == 200:
                    # 根据脚本id，执行脚本
                    qid = ql.ql_run(ids, ql_ck[j])
                    if qid == 0:
                        logger.write_log(f"{ql_ck[j][0]} 执行 {data[0]} 脚本成功 ID {ids[0]} 执行参数: {data[1]}")
                        time.sleep(3)
                    # 把原来内容添加回去
                    ql.configs_revise('config.sh', bytex, ql_ck[j])
                    tf = True
            else:
                logger.write_log(f"{ql_ck[j][0]}异常问题,检测到程序非正常状态,不再执行")
        time.sleep(60) if int(time.strftime('%H')) == 0 and tf else ""
        q.task_done()
