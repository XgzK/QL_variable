import datetime
import re
from queue import Queue

from conn.Plugin.lottery import Lottery
from conn.Template.ancestors import Father
from conn.Template.jdql import JdQl
from conn.bots.interaction import Interaction
from conn.tools.log import LoggerClass
from conn.tools.sql import Sql

q = Queue()


class Sundries(Father):

    def __init__(self):
        """
        处理杂物的类
        """
        super().__init__()
        self.q = q
        self.flash_Config()
        self.sql = Sql()
        self.lottery = Lottery()
        self.logger = LoggerClass()
        self.li = ['jd', 'pr', 'co', 'ji', 'sh', 'tx', 'wq']
        self.Markings = ["RUN", "NOT"]
        self.interaction = Interaction()

    def looking(self, text_str: str) -> JdQl:
        """
        用户传入变量返回脚本库
        :param text_str:
        :return: JdQl类或None
        """
        value1 = self.sql.selectTopone(table=self.sql.surface[0],
                                       where=f'jd_value1="NOT{text_str}" or jd_value1="{text_str}" '
                                             f'or jd_value2="{text_str}" '
                                             f'or jd_value3="{text_str}"')
        return JdQl(value1) if value1 else None

    def https_txt(self, http) -> list[[str, JdQl]]:
        """
        处理链接类型转成活动
        :param http: 待处理的数据
        :return: []
        """
        try:
            lis = []
            http = self.sh_venderId(http.replace('"', ""))

            # 先查询是否存有这个链接
            li = self.fuzzy_query(http)
            if not li:
                self.logger.write_log(
                    f"conn.mission.sundries.Sundries.https_txt,没有查询到的链接是: {http}")
                return []

            # 遍历数组
            for ink in li:
                tx = re.findall(f'{ink.jd_re}', http)
                if not tx:
                    self.logger.write_log(
                        f"conn.mission.sundries.Sundries.https_txt,匹配不到内容: {ink.jd_re} 链接是: {http}")
                    continue
                st2 = ''
                # 往后推
                sun = 0
                # 拼接数组
                for i in tx[0] if type(tx[0]) == tuple else tx:
                    if type(list) and len(i) == 2 and ink.jd_value2 is None:
                        st2 += ink.Change[sun] + "=" + f'\"{i[0]}{ink.partition if ink.partition else ""}{i[1]}\";'
                        sun += 1
                    else:
                        if ink.Change[sun] is None:
                            st2 = st2.replace('";', '')
                            st2 += ink.partition + str(i) + '";'
                        else:
                            st2 += ink.Change[sun] + "=" + f'"{i}";'
                            sun += 1
                if st2:
                    TYPE = re.findall("https://(\w{2})", http)[0]
                    st2 += f'export NOT_TYPE="{TYPE}";'
                    lis.append([st2, ink])
            return lis
        except Exception as e:
            self.logger.write_log(f"conn.mission.sundries.Sundries.https_txt,异常问题: {e} 活动链接 {http}")
            return []

    def sh_venderId(self, url=None):
        """
        检测是否需要获取 venderId
        :param url:
        :return:
        """
        try:
            shven = re.findall("https://shop\.m\.jd\.com/shop/lottery.*?shopId=(\d+)$", url)
            if shven:
                return url + self.lottery.get_venderId(shven[0])
            else:
                return url
        except Exception as e:
            self.logger.write_log(f"conn.mission.sundries.Sundries.sh_venderId异常 {e}")
            return url

    def fuzzy_query(self, url: str) -> list[JdQl]:
        """
        模糊查询,没有就打印日志让管理者添加
        :param url: 查询的url带问号后面的内容,如果没有就传None
        :return: 返回数据库 or []
        """
        try:
            li1s = []
            TYPE = re.findall("https://(.{2})", url)[0]
            # 读取数据库中活动全部链接的数据
            lines = self.sql.selectAll(table=self.sql.surface[0],
                                       where=f'jd_type == "{TYPE}"') if TYPE in self.li else self.sql.selectAll(
                table=self.sql.surface[0], where=f'jd_type == "{TYPE}" or jd_type == "cl"', order="id DESC")
            # 遍历数据库正则表达式非空
            if type(lines) == list:
                for i in lines:
                    i = JdQl(i)
                    try:
                        zzbds = re.findall(i.jd_url, url)
                        if zzbds:
                            li1s.append(i)
                        else:
                            # 如果没有就清理
                            del i
                    except Exception as e:
                        self.logger.write_log(
                            f"conn.mission.sundries.Sundries.fuzzy_query 在对比数据库中出现异常: {e} 触发异常的值是 {url} 数据库值的脚本名称是 {i[2]}")
                if li1s:
                    return li1s
                self.logger.write_log("模糊查询中: " + str(url) + " 没有找到,请添加")
            return li1s
        except Exception as e:
            self.logger.write_log(
                "conn.mission.sundries.Sundries.fuzzy_query,异常问题: " + str(e) + "异常的值是: " + url)
            return []

    def turn_url(self, export: str):
        """
        参数转连接
        :param export: 活动参数
        :return:
        """
        export = re.sub("[()'`;\"*]+(?:export NOT_TYPE=\".*?\";)", "", export)
        ex_sun = re.findall('(export \w+)=', export)

        jsva = ''.join(
            f"{'{0}{1}' + str(ex_sun[i]) + '{1} or ' if i != len(ex_sun) - 1 else '{0}{1}' + str(ex_sun[i]) + '{1}'} "
            for i
            in
            range(len(ex_sun))).format('export1=', '"')

        sq = self.sql.selectAll(table=self.sql.surface[2], where=f"{jsva}")

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

    def contrast(self, str12: dict):
        """
        去除掉相同脚本参数,如果脚本相同只执行一次
        :param str12: 活动参数
        :return: NOT关键字返回 [0] 执行过返回 [1, 关键字] 没有执行过 [2, 关键字] 没有识别 [3] 异常 [-1] 执行
        """
        try:
            if str12["marking"] in self.Markings:
                return [0]

            # 提取链接类型关键字
            keywords_url1 = re.findall("(?:activityId|configCode|actId|user_id|shopId|a|token)=\"?(\w+)",
                                       str12["activities"], re.S)
            if keywords_url1:
                inquire = 1 if self.sql.selectTopone(table=self.sql.surface[1],
                                                     where=f"jd_value1='{keywords_url1[0]}'") else 2
                return [inquire, keywords_url1[0]]

            # 提取特殊链接类型
            keywords_url2 = re.findall("(?:id|code|Id|activityUrl)=\"?(\w+)", str12["activities"], re.S)
            if keywords_url2:
                inquire = 1 if self.sql.selectTopone(table=self.sql.surface[1],
                                                     where=f"jd_value1='{keywords_url2[0]}'") else 2
                return [inquire, keywords_url2[0]]

            # 提取变量非链接类型
            keywords_url3 = re.findall("=\"([a-zA-Z0-9&]+)", str12["activities"], re.S)
            if keywords_url3:
                inquire = 1 if self.sql.selectTopone(table=self.sql.surface[1],
                                                     where=f"jd_value1='{keywords_url3[0]}'") else 2
                return [inquire, keywords_url3[0]]
            return [3]
        except Exception as e:
            self.logger.write_log('去掉相同活动异常: ', e)
            return [-1]

    def ql_write(self, data: dict, essential: list):
        """
        写入青龙任务配置文件
        :param data: 传入内容
        :param essential: 添加进重复数据库的关键字
        :return: 如果没有执行过返回0，如果执行过返回-1
        """
        try:
            if self.AdReg.get('deduplication') == 1:
                return 0
            # 0表示不去重复
            elif data["marking"] == "NOT":
                self.interaction.for_message(f"NOT表示属于不去重复关键字(未开发功能): \n{data['activities']}", False)
                return 0
            elif data["marking"] == "RUN":
                return 0
            elif essential[0] == 2:
                self.sql.insert(table=self.sql.surface[1], jd_value1=f"{essential[1]}",
                                jd_data=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                return 0
        except Exception as e:
            self.logger.write_log("ql_write,异常信息：" + str(e))
            return -1

    def ql_compared(self, jst: str, ql_ck: tuple) -> list:
        """
        遍历青龙任务来对比,获取任务ID
        :param jst: 脚本名称
        :param ql_ck: 青龙数据库
        :return: ID or -1
        """
        try:
            jstx = self.read(ql_ck[5])
            # 判断脚本时否存在,不存在直接返回
            if not (jst in jstx):
                return [-1]
            va1 = jstx[jst]
            # 判断用户时否需要优先执行特定库 task 库/脚本.js
            lis = list(va1.keys())
            return [va1[lis[0]]['id']]
        except Exception as e:
            self.logger.write_log(f'查询任务异常信息: {e}')
            return [-1]

    def tx_compared(self, value1: list):
        """
        用于对比数据，由TG获取的文本对比数据库中的数据
        :return: 返回数组的脚本名称[0]和变量[1],异常返回-1
        """
        try:
            # [脚本, 活动, 时间, 关键字]
            self.q.put({
                "jd_js": value1[1].jd_js,
                "activities": value1[2],
                "interval": value1[1].interval,
                "marking": value1[0]
            })
            self.logger.write_log(
                f"脚本名称 {value1[1].jd_js} 脚本 {value1[1].jd_name} 加入队列任务, 当前队列任务剩余 {q.qsize()} 个")
            return
        except Exception as e:
            self.logger.write_log(f"conn.mission.sorting.Sorting.tx_compared 异常对比脚本异常信息信息: {e}")
