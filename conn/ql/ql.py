"""
青龙接口类
"""
import json
import time

import requests

from conn.gheaders.conn import read_yaml
from conn.gheaders.get_headers import ql_header
from conn.gheaders.log import LoggerClass

logger = LoggerClass('debug')


class QL:
    def __init__(self):
        self.headers = ql_header

    def ql_tk(self):
        """
        用于获取登录用的ck,ck有效期一个月
        :return: 返回登录用的Bearer XXXXXXXXXXX，如果没有获取到，返回0
        """
        try:
            yam = read_yaml()
            url = yam['ip'] + "/open/auth/token"
            params = {
                'client_id': yam['Client ID'],
                'client_secret': yam['Client Secret']
            }
            cs = requests.get(url=url, params=params, timeout=5)
            print(cs.url)
            jstx = cs.json()
            logger.write_log("获取登录Bearer成功")
            return jstx['data']['token_type'] + " " + jstx['data']['token']
        except Exception as e:
            print("ql_tk异常信息，请检查conn.yml文件，异常信息：" + str(e))
            logger.write_log("ql_tk异常信息，请检查conn.yml文件，异常信息：" + str(e))
            return 0

    def ql_run(self, data):
        """
        执行青龙任务
        :param data: int数组
        :return: 0 or -1
        """
        try:
            ur = read_yaml()
            url = ur['ip'] + '/open/crons/run'
            ss = requests.put(url=url, headers=self.headers(), data=json.dumps(data), timeout=10)
            status = ss.status_code
            # 获取返回的状态码
            if status == 200:
                # 延迟3秒
                time.sleep(3)
                logger.write_log("任务执行成功")
                return 0
            else:
                logger.write_log("任务执行失败:" + str(status))
                return -1
        except Exception as e:
            logger.write_log("执行青龙任务失败，错误信息：" + str(e))
            return -1

    def crons(self):
        """
        获取任务列表
        :return:
        """
        try:
            ur = read_yaml()
            url = ur['ip'] + '/open/crons'
            lis = requests.get(url=url, headers=self.headers())
            li = lis.json()
            if li['code'] == 200:
                return li['data']
        except Exception as e:
            print(e)

    def configs_check(self, path):
        """
        获取配置文件的内容
        :param path: 配置文件名称
        :return: 返回文件内容,错误返回{'code': 404}
        """
        try:
            ur = read_yaml()
            url = ur['ip'] + '/open/configs/' + path
            ss = requests.get(url=url, headers=self.headers(), timeout=10)
            status = ss.status_code
            # 获取返回的状态码
            if status == 200:
                return ss.json()
            return {'code': 404}
        except Exception as e:
            logger.write_log("获取配置文件内容失败: ", e)

    def configs_revise(self, path, data):
        """
        修改配置文件
        :param path: 配置文件名称
        :param data: 传输的内容
        :return: 返回{"code":200,"message":"保存成功"},错误返回{'code': 404}
        """
        try:
            ur = read_yaml()
            url = ur['ip'] + '/open/configs/save'
            cs = {"content": data, "name": path}
            ss = requests.post(url=url, headers=self.headers(), data=json.dumps(cs), timeout=10)
            status = ss.status_code
            # 获取返回的状态码
            if status == 200:
                return ss.json()
            return {'code': 404}
        except Exception as e:
            logger.write_log("修改配置文件内容失败: ", e)

    def system_version(self):
        """
        青龙版本号
        :return:
        """
        try:
            yam = read_yaml()
            url = yam['ip'] + "/api/system"
            ver = requests.get(url)
            js = ver.json()
            if js['code'] == 200:
                return js['data']['version']
        except Exception as e:
            print('异常信息', e)
