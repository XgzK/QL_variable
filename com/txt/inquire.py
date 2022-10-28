import re

from com.gheaders import LoggerClass
from com.sql import conn

logger = LoggerClass('debug')


def fuzzy_query(url=None):
    """
    模糊查询,没有就打印日志让管理者添加
    :param url: 查询的url带问号后面的内容,如果没有就传None
    :return: 返回数据库 or []
    """
    try:
        # 读取数据库中活动全部链接的数据
        lines = conn.selectAll(table=conn.surface[0], where=f'jd_url != "" and jd_re != ""')
        # print(lines)
        lis = []
        # 遍历数据库正则表达式非空
        for i in lines:
            try:
                # print('----------------------------')
                # print(i)
                # print(url)
                zzbds = re.findall(f'{i[6]}', url)
                # print('匹配结果',zzbds)
                if zzbds:
                    # print('添加之前',lis)
                    lis.append(i)
                    # print('添加后',lis)
            except Exception as e:
                logger.write_log(f"异常的数据库值是: {i}")
                logger.write_log(f"inquire.fuzzy_query 在对比数据库中出现异常: {e}")
        if lis:
            return lis
        logger.write_log("模糊查询中: " + str(url) + " 没有找到,请添加")
        return []
    except Exception as e:
        logger.write_log("inquire.fuzzy_query,异常问题: " + str(e) + "异常的值是: " + url)
        return []
