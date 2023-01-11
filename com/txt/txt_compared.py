import re

from com import q
# from com.fo.core import main_core
from com.gheaders.log import LoggerClass
from com.sql import Sql

conn = Sql()
logger = LoggerClass('debug')


def tx_compared(tx1):
    """
    用于对比数据，由TG获取的文本对比数据库中的数据
    :return: 返回数组的脚本名称[0]和变量[1],异常返回-1
    """
    try:
        # 把export DPLHTY="b4be"的键和值分开
        tx = re.findall('(export .*?)=(.*)', tx1)
        # 如果分成两个尝试判断数据库中是否需要跳过去重复
        value1 = conn.selectTopone(table=conn.surface[0],
                                   where=f'jd_value1="NOT{tx[0][0]}" or jd_value1="{tx[0][0]}" '
                                         f'or jd_value2="{tx[0][0]}" '
                                         f'or jd_value3="{tx[0][0]}"')
        if value1 and value1[3] is None and value1[4] is None:
            # [脚本, 活动, 时间]
            q.put({
                "jd_js": value1[2],
                "activities": value1[3] + '=' + tx[0][1],
                "interval": value1[10]
            })
            logger.write_log(f"脚本名称 {value1[1]} 脚本 {value1[2]} 加入队列任务, 当前队列任务剩余 {q.qsize()} 个")
            return
        elif value1:
            q.put({
                "jd_js": value1[2],
                "activities": value1[3] + '=' + tx[0][1],
                "interval": value1[10],
                "time": 0
            })
            logger.write_log(f"脚本 {value1[1]} 加入队列任务, 当前队列任务剩余 {q.qsize()} 个")
            return
        else:
            logger.write_log(f"在数据库中没有找到: {tx1}")
    except Exception as e:
        logger.write_log(f"tx_compared 异常对比脚本异常信息信息: {e}")
