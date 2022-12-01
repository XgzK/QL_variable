"""
此脚本用于处理txt文件里面的数据，并且二次加工
"""
import re

from com.gheaders.log import LoggerClass
from com.sql import Sql
from com.txt.inquire import fuzzy_query
from com.txt.txt_compared import tx_compared

logger = LoggerClass('debug')
conn = Sql()


def export_txt(extx):
    """
    处理export \w+="\w+"这种格式
    :param extx: 待处理的数据
    :return: 处理后的行，异常返回-1
    """
    try:
        # 把extx分隔，去除中间的"="
        # 按=分隔
        separate = extx.split('=')

        # 去除separate[1]前后的",避免有的值有有的没有
        separate[1] = separate[1].replace('"', '')
        # 程序第一个值是不是和自己相识
        sq = conn.selectTopone(table=conn.surface[0], where=f"jd_value1='NOT{separate[0]}'")
        if len(sq) > 0:
            # 获取设置得正则表达式
            separate[0] = 'NOT' + separate[0]
        # 把两端重新拼接并且返回
        return str(separate[0]) + '="' + str(separate[1]) + '"'
    except Exception as e:
        logger.write_log("export_txt，异常问题: " + str(e))
        return -1


def https_txt(http):
    """
    处理.*?>(https://.*?\?\w+=\w+)</a>
    :param http: 待处理的数据
    :return: 处理后的二维list，异常返回-1
    """
    try:
        http = http.replace('"', "")
        # 先查询是否存有这个链接
        li = fuzzy_query(http)
        if len(li) == 0:
            logger.write_log("https_txt,正则表达式没有匹配到值:  " + str(http))
            return -1
        # 遍历数组
        for ink in li:
            tx = re.findall(f'{ink[7]}', http)
            if not tx:
                logger.write_log(f"https_txt,匹配不到内容: {ink[7]} 链接是: {http}")
                continue
            st2 = ''
            # 往后推
            sun = 0
            # 拼接数组
            for i in tx[0] if type(tx[0]) == tuple else tx:
                if type(list) and len(i) == 2 and ink[4] is None:
                    st2 += ink[3 + sun] + "=" + f'"{i[0]}&{i[1]}";'
                    sun += 1
                else:
                    if ink[3 + sun] is None:
                        st2 = st2.replace('";', '')
                        st2 += '&' + str(i) + '";'
                    else:
                        st2 += ink[3 + sun] + "=" + f'"{i}";'
                        sun += 1
            if st2:
                TYPE = re.findall("https://(\w{2})", http)[0]
                st2 += f'export NOT_TYPE="{TYPE}";'
                tx_compared(st2)
        return 0
    except Exception as e:
        logger.write_log("https_txt,异常问题: " + str(e))
        return -1
