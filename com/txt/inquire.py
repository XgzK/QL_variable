import re

from com import q
from com.Plugin.lottery import Lottery
from com.gheaders.log import LoggerClass
from com.sql import Sql

lottery = Lottery()
sql = Sql()
logger = LoggerClass()


class Conversion:

    def __init__(self):
        self.li = ['jd', 'pr', 'co', 'ji', 'sh', 'tx', 'wq']

    def sh_venderId(self, url=None):
        """
        检测是否需要获取 venderId
        :param url:
        :return:
        """
        shven = re.findall("https://shop\.m\.jd\.com/shop/lottery.*?shopId=(\d+)$", url)
        if shven:
            return url + lottery.get_venderId(shven[0])
        else:
            return url

    def fuzzy_query(self, url=None):
        """
        模糊查询,没有就打印日志让管理者添加
        :param url: 查询的url带问号后面的内容,如果没有就传None
        :return: 返回数据库 or []
        """
        try:
            li1s = []
            TYPE = re.findall("https://(\w{2})", url)[0]
            # 读取数据库中活动全部链接的数据
            lines = sql.selectAll(table=sql.surface[0],
                                  where=f'jd_type == "{TYPE}"') if TYPE in self.li else sql.selectAll(
                table=sql.surface[0], where=f'jd_type == "{TYPE}" or jd_type == "cl"', order="id DESC")
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

    def turn_url(self, export: str):
        """
        参数转连接
        :param export: 活动参数
        :return:
        """
        export = re.sub("[()'`\"*]+", "", export)
        ex_sun = re.findall('(export \w+)=', export)

        jsva = ''.join(
            f"{'{0}{1}' + str(ex_sun[i]) + '{1} or ' if i != len(ex_sun) - 1 else '{0}{1}' + str(ex_sun[i]) + '{1}'} "
            for i
            in
            range(len(ex_sun))).format('export1=', '"')

        sq = sql.selectAll(table=sql.surface[2], where=f"{jsva}")

        # 返回的有数组
        if sq:
            for jd_va in sq:

                if jd_va[2] and len(ex_sun) == 2:
                    try:
                        return [
                            str(jd_va[0]).replace('#0', re.findall('activityUrl="([A-Za-z0-9&_/:.-]{5,})"', export)[-1])
                            .replace('#1', re.findall('activityId="(\w+)"', export)[-1])]
                    except:
                        pass
                # 参数2没有
                elif not jd_va[2] and len(ex_sun) == 1:
                    lis = []
                    sun = 0
                    st = ""
                    ex_tx = export.split('=')
                    # 进入这里表示只需要一个值
                    points = ex_tx[1].split(jd_va[4]) if jd_va[4] else [ex_tx[1]]
                    su = len(jd_va[0].split('#'))
                    for son in set(points):
                        if su > 2:
                            st += str(jd_va[0]).replace(f"#{sun}", re.findall('(\w+)', son)[-1])
                            if sun == su - 1:
                                lis.append(st)
                        else:
                            lis.append(str(jd_va[0]).replace("#0", re.findall('(\w+)', son)[-1]))
                        sun += 1
                    return lis
            return []
        else:
            # 没有返回空
            return []

    def https_txt(self, http):
        """
        处理.*?>(https://.*?\?\w+=\w+)</a>
        :param http: 待处理的数据
        :return: 处理后的二维list，异常返回-1
        """
        try:
            http = http.replace('"', "")
            http = self.sh_venderId(http)
            # 先查询是否存有这个链接
            li = self.fuzzy_query(http)
            if len(li) == 0:
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
                            st2 += ink[9] + str(i) + '";'
                        else:
                            st2 += ink[3 + sun] + "=" + f'"{i}";'
                            sun += 1
                if st2:
                    TYPE = re.findall("https://(\w{2})", http)[0]
                    st2 += f'export NOT_TYPE="{TYPE}";'
                    self.tx_compared(st2, ink)
            return 0
        except Exception as e:
            logger.write_log("https_txt,异常问题: " + str(e))
            return -1

    def export_txt(self, extx):
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
            sq = sql.selectTopone(table=sql.surface[0], where=f"jd_value1='NOT{separate[0]}'")
            if len(sq) > 0:
                # 获取设置得正则表达式
                separate[0] = 'NOT' + separate[0]
            # 把两端重新拼接并且返回
            return str(separate[0]) + '="' + str(separate[1]) + '"'
        except Exception as e:
            logger.write_log("export_txt，异常问题: " + str(e))
            return -1

    def tx_compared(self, tx1, value1=None):
        """
        用于对比数据，由TG获取的文本对比数据库中的数据
        :return: 返回数组的脚本名称[0]和变量[1],异常返回-1
        """
        try:
            # 把export DPLHTY="b4be"的键和值分开
            tx = re.findall('(export .*?)=(.*)', tx1)
            # 如果分成两个尝试判断数据库中是否需要跳过去重复
            if value1 is None:
                value1 = sql.selectTopone(table=sql.surface[0],
                                          where=f'jd_value1="NOT{tx[0][0]}" or jd_value1="{tx[0][0]}" '
                                                f'or jd_value2="{tx[0][0]}" '
                                                f'or jd_value3="{tx[0][0]}"')

            if value1:
                # [脚本, 活动, 时间]
                q.put({
                    "jd_js": value1[2],
                    "activities": value1[3] + '=' + tx[0][1],
                    "interval": value1[10]
                })
                logger.write_log(f"脚本名称 {value1[1]} 脚本 {value1[2]} 加入队列任务, 当前队列任务剩余 {q.qsize()} 个")
                return

            else:
                logger.write_log(f"在数据库中没有找到: {tx1}")
        except Exception as e:
            logger.write_log(f"tx_compared 异常对比脚本异常信息信息: {e}")
