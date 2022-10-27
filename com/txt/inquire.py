import re

from com.gheaders import LoggerClass
from com.sql import conn

logger = LoggerClass('debug')


def fuzzy_query(url=None):
    """
    模糊查询,没有就打印日志让管理者添加
    :param url: 查询的url带问号后面的内容,如果没有就传None
    :return: 正常原二维数组[url,v1,v2,v3,re], 否则返回-1
    """
    try:
        # 读取数据库中活动全部链接的数据
        lines = conn.selectAll(table=conn.surface[0], where=f'jd_url != ""')
        # 获取数据库中的参数
        values = conn.selectAll(table=conn.surface[0], field="jd_value1,jd_value2,jd_value3, jd_re")
        lis = []
        if len(values) != 0:
            for i in range(len(lines)):
                # 打印非None的值
                if lines[i][0] is not None and lines[i][0] != "":
                    zzbds = re.findall(r'{}.*?'.format(str(lines[i][0])), url)
                    if zzbds is not None and len(zzbds) > 0:
                        lis.append([lines[i][0], values[i][0], values[i][1], values[i][2], values[i][3]])
            if len(lis) > 0:
                return lis
        logger.write_log("模糊查询中: " + str(url) + " 没有找到,请添加")
        return -1
    except Exception as e:
        logger.write_log("inquire.fuzzy_query,异常问题: " + str(e))
        return -1
