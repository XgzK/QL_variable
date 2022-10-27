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
        print('-----对比脚本')
        # 切割字符串
        if tx1[0:6:1] == 'export' or tx1[0:9:1] == 'NOTexport':
            # 把export DPLHTY="b4be"的键和值分开
            tx = tx1.split('=')
            print(tx)
            # 先查询这个值在不在jd_value1中
            value1 = conn.selectTopone(table=conn.surface[0], where=f'jd_value1="{tx[0]}"')
            print(value1)
            # 再查询这个值在不在jd_value2中
            value2 = conn.selectTopone(table=conn.surface[0], where=f'jd_value2="{tx[0]}"')
            print(value2)
            # 再查询这个值在不在jd_value3中
            value3 = conn.selectTopone(table=conn.surface[0], where=f'jd_value3="{tx[0]}"')
            if value1:
                main_core([value1[2], tx1])
            elif value2:
                main_core([value2[2], tx1])
            elif value3:
                main_core([value3[2], tx1])
            else:
                logger.write_log(f"在数据库中没有找到: {tx1}")
    except Exception as e:
        logger.write_log(f"tx_compared 异常对比脚本异常信息信息: {e}")
