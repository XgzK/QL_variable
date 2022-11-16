from com import q
from com.fo.core import main_core
from com.gheaders import LoggerClass
from com.sql import conn

logger = LoggerClass('debug')


def tx_compared(tx1):
    """
    用于对比数据，由TG获取的文本对比数据库中的数据
    :return: 返回数组的脚本名称[0]和变量[1],异常返回-1
    """
    try:
        # 初始化
        value1, value2, value3 = '', '', ''
        # 切割字符串
        if tx1[0:6:1] == 'export':
            # 把export DPLHTY="b4be"的键和值分开
            tx = tx1.split('=')
            # 如果分成两个尝试判断数据库中是否需要跳过去重复
            value1 = conn.selectTopone(table=conn.surface[0], where=f'jd_value1="NOT{tx[0]}"')
            if len(tx) == 3 and value1:
                q.put([value1[2], "NOT" + tx1])
            else:
                # 先查询这个值在不在jd_value1中
                value1 = conn.selectTopone(table=conn.surface[0], where=f'jd_value1="{tx[0]}"')
                # 再查询这个值在不在jd_value2中
                value2 = conn.selectTopone(table=conn.surface[0], where=f'jd_value2="{tx[0]}"')
                # 再查询这个值在不在jd_value3中
                value3 = conn.selectTopone(table=conn.surface[0], where=f'jd_value3="{tx[0]}"')
                if value1:
                    q.put([value1[2], tx1])
                if value2:
                    q.put([value2[2], tx1])
                if value3:
                    q.put([value3[2], tx1])
            if value1 == value2 == value3 is None:
                logger.write_log(f"在数据库中没有找到: {tx1}")
        else:
            # 直接带NOT开头的
            tx = tx1.split('=')
            # 如果分成两个尝试判断数据库中是否需要跳过去重复
            value1 = conn.selectTopone(table=conn.surface[0], where=f'jd_value1="{tx[0]}"')
            if len(tx) == 3 and value1:
                q.put([value1[2], tx1])
        tx1 = q.get()
        main_core(tx1)
    except Exception as e:
        logger.write_log(f"tx_compared 异常对比脚本异常信息信息: {e}")
