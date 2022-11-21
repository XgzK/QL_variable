"""
执行青龙有关的定时任务有关
"""
import json
import re
import time

from com.gheaders import logger
from com.ql import ql
from com.sql import conn


class Timing(object):
    def __init__(self):
        self.conn = conn
        self.ql = ql
        self.logger = logger

    def check_ct(self, state=0):
        """
        获取新青龙tk
        :param state: 0 or 1
        :return:
        """
        value1 = self.conn.selectAll(table=self.conn.surface[3], where=f"state={state}")
        for ql_tk in value1:
            for i in range(3):
                ck = self.ql.ql_tk(ql_tk)
                if ck[0] == 200:
                    self.conn.update(table=self.conn.surface[3], Authorization=ck[1], where=f"name='{ql_tk[0]}'")
                    break
                elif ck[0] == 500 or i == 2:
                    self.logger.write_log(f"{ql_tk[0]}容器的 Bearer添加失败, 30s后再次获取")
                    time.sleep(30)
                elif ck[0] == 403:
                    # state = 1 表示异常
                    self.conn.update(table=self.conn.surface[3], state=1, where=f"name='{ql_tk[0]}'")
        return 0

    def clear_list(self, state=0):
        """
        清空参数和获取任务列表
        :param state: 0表示执行正常的 1表示执行异常的,默认 0
        :return:
        """
        self.conn.delete(table=self.conn.surface[1])
        try:
            value1 = self.conn.selectAll(table=self.conn.surface[3], where=f"state={state}")
            for ql_tk in value1:
                js_ql = ql.crons(ql_tk)
                # 跳过检测
                if js_ql[0] != 200:
                    self.logger.write_log(f'{ql_tk[0]} 获取列表异常')
                    self.conn.update(table=self.conn.surface[3], state=1, where=f"name='{ql_tk[0]}'")
                    continue
                js = dict()
                # 如果青龙里面有层data就解包
                for i in js_ql['data'] if 'data' in js_ql else js_ql:
                    if len(i['command'].split('/')) == 2:
                        aa = re.findall('task .*?/([a-zA-Z0-9&=_/-]+\.\w+)', i['command'])
                    else:
                        aa = re.findall('task ([a-zA-Z0-9&=_/-]+\.\w+)', i['command'].split('/')[-1])
                    if aa:
                        if not (aa[0] in js):
                            js[aa[0]] = {}
                        # 用来区分 版本json格式差异
                        if 'id' in i:
                            js[aa[0]].setdefault(i['command'],
                                                 {'id': i['id'], "name": i["name"], "isDisabled": i["isDisabled"]})
                        else:
                            js[aa[0]].setdefault(i['command'],
                                                 {'id': i['_id'], "name": i["name"], "isDisabled": i["isDisabled"]})
                    else:
                        self.logger.write_log(f"跳过录入: {i['command']}")
                with open(js_ql[5], mode='w+', encoding='utf-8') as f:
                    json.dump(js, f, ensure_ascii=False)
                return 0
        except Exception as e:
            self.logger.write_log(f'获取列表异常: {e}')
            return -1
