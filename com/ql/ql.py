"""
青龙接口类
"""
import json

import requests

from com.gheaders.conn import read_yaml
from com.gheaders.get_headers import ql_header, qlck_header
from com.gheaders.log import LoggerClass

logger = LoggerClass('debug')
yam = read_yaml()


class QL:
    def __init__(self):
        self.headers = ql_header

    def ql_tk(self, ql_tk):
        """
        用于获取登录用的ck,ck有效期一个月
        :param ql_tk: 青龙数据库
        :return: 返回登录用的Bearer XXXXXXXXXXX，[状态码,内容]
        """
        url = ql_tk[1] + "/open/auth/token"
        data = {
            'client_id': ql_tk[2],
            'client_secret': ql_tk[3]
        }
        try:
            cs = requests.get(url=url, params=data, timeout=10, headers=qlck_header())
            jstx = cs.json()
            if jstx['code'] == 200:
                return [jstx['code'], jstx['data']['token_type'] + " " + jstx['data']['token']]
            else:
                logger.write_log(f"{ql_tk[0]} 获取青龙Authorization异常 状态码: {jstx['code']} 原因: {jstx['data']}")
                return [403]
        except Exception as e:
            logger.write_log(f"{ql_tk[0]} 请求青龙异常: {e}")
            return [500]

    def ql_run(self, data, ql_tk: tuple):
        """
        执行青龙任务
        :param data: int数组
        :param ql_tk: 青龙数据库
        :return: 0 or -1
        """
        try:
            url = ql_tk[1] + '/open/crons/run'
            ss = requests.put(url=url, headers=self.headers(ql_tk[4]), data=json.dumps(data), timeout=10)
            status = ss.status_code
            # 获取返回的状态码
            if status == 200:
                return 0
            else:
                logger.write_log("任务执行失败:" + str(status))
                return -1
        except Exception as e:
            logger.write_log("执行青龙任务失败，错误信息：" + str(e))
            return -1

    def crons(self, ql_tk: list):
        """
        获取任务列表
        :param ql_tk: 青龙数据库的列表
        :return: [状态码, 列表]
        """
        try:
            url = ql_tk[1] + '/open/crons'
            lis = requests.get(url=url, headers=self.headers(ql_tk[4]))
            li = lis.json()
            if li['code'] == 200:
                return [li['code'], li['data']]
            logger.write_log(f"状态码: {li['code']} 请给相应权限")
            return li['code']
        except Exception as e:
            logger.write_log(f"获取青龙任务列表失败: {e}")
            return [403]

    def configs_check(self, path, ql_tk: tuple):
        """
        获取配置文件的内容
        :param path: 配置文件名称
        :param ql_tk: 青龙数据库
        :return: 返回文件内容,错误返回{'code': 404}
        """
        try:
            url = ql_tk[1] + '/open/configs/' + path
            ss = requests.get(url=url, headers=self.headers(ql_tk[4]), timeout=10)
            status = ss.status_code
            # 获取返回的状态码
            if status == 200:
                return ss.json()
            return {'code': 404}
        except Exception as e:
            logger.write_log("获取配置文件内容失败: ", e)
            return {'code': 404}

    def configs_revise(self, path, data, ql_tk: tuple):
        """
        修改配置文件
        :param path: 配置文件名称
        :param data: 传输的内容
        :param ql_tk: 青龙数据库
        :return: 返回{"code":200,"message":"保存成功"},错误返回{'code': 404}
        """
        try:
            url = ql_tk[1] + '/open/configs/save'
            cs = {"content": data, "name": path}
            ss = requests.post(url=url, headers=self.headers(ql_tk[4]), data=json.dumps(cs), timeout=10)
            status = ss.status_code
            # 获取返回的状态码
            if status == 200:
                return ss.json()
            return {'code': 404}
        except Exception as e:
            logger.write_log("修改配置文件内容失败: ", e)
            return {'code': 404}

    def disable(self, data: list, ql_tk: tuple):
        """
        禁用青龙任务
        :param data: int数组
        :param ql_tk: 青龙数据库
        :return: 0 or -1
        """
        try:
            url = ql_tk[1] + '/open/crons/disable'
            ss = requests.put(url=url, headers=self.headers(ql_tk[4]), data=json.dumps(data), timeout=10)
            status = ss.status_code
            # 获取返回的状态码
            if status == 200:
                logger.write_log("禁用任务成功")
                return 0
            else:
                logger.write_log("任务禁用失败:" + str(status))
                return -1
        except Exception as e:
            logger.write_log("执行青龙禁用任务失败，错误信息：" + str(e))
            return -1
