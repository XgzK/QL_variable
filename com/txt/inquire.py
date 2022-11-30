import re

from com.gheaders import LoggerClass
from com.sql import Sql

conn = Sql()
logger = LoggerClass('debug')
li = ['jd', 'pr', 'co', 'ji', 'sh', 'tx', 'wq']


def fuzzy_query(url=None):
    """
    模糊查询,没有就打印日志让管理者添加
    :param url: 查询的url带问号后面的内容,如果没有就传None
    :return: 返回数据库 or []
    """
    try:
        li1s = []
        TYPE = re.findall("https://(\w{2})", url)[0]
        # 读取数据库中活动全部链接的数据
        lines = conn.selectAll(table=conn.surface[0], where=f'jd_type == "{TYPE}"') if TYPE in li else conn.selectAll(
            table=conn.surface[0], where=f'jd_type == "{TYPE}" or jd_type == "cl"', order="id DESC")
        # 遍历数据库正则表达式非空
        if type(lines) == list:
            for i in lines:
                try:
                    zzbds = re.findall(i[6], url)
                    if zzbds:
                        li1s.append(i)
                except Exception as e:
                    logger.write_log(f"异常的数据库值是: {i}")
                    logger.write_log(f"inquire.fuzzy_query 在对比数据库中出现异常: {e}")
            if li1s:
                return li1s
            logger.write_log("模糊查询中: " + str(url) + " 没有找到,请添加")
        return []
    except Exception as e:
        logger.write_log("inquire.fuzzy_query,异常问题: " + str(e) + "异常的值是: " + url)
        return []


def turn_url(export: str):
    """
    参数转连接
    :param export: 活动参数
    :return:
    """
    export = export.replace('"', '').replace(';', '')
    ex = re.findall('(export \w+)=', export)
    sq = conn.selectTopone(table=conn.surface[2], where=f"export1='{ex[0]}'")
    # 返回的有数组 并且参数1有值参数2没有
    if sq and sq[1] and sq[2] is None:
        ex = export.split('=')
        # 把值和活动隔开
        # 如果 export jd_cjhy_sevenDay_ids 就按&分隔
        if ex[0][-1] == 's':
            stli = []
            # 转换多个链接,全部当成@0位,因为有的有@分隔,统一把@替换成&
            st = ex[1].replace("@", '&').split('&')
            for i in range(len(st)):
                stli.append(str(sq[0]).replace('#' + str(i), st[i]))
            return stli
        else:
            # 如果没有占位符无法添加
            st1 = ''
            # 如果没有s再按&分隔,填充占位
            if len(sq[0].split('#')) > 2:
                st = ex[1].split('&')
                for i in range(len(st)):
                    # 如果 st1 is None 则使用 sq[0]
                    if st1:
                        st1 = st1.replace('#' + str(i), st[i])
                    else:
                        st1 = str(sq[0]).replace('#' + str(i), st[i])
                return [st1]
            else:
                lis = []
                st = ex[1].split('&')
                for i in range(len(st)):
                    lis.append(str(sq[0]).replace('#0', st[i]))
                return lis
    else:
        return []
