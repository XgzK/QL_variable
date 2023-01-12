"""
青龙接口类
"""
import json

import requests

from com.gheaders.conn import read_yaml
from com.gheaders.log import LoggerClass

yam = read_yaml()


class QL(LoggerClass):
    def __init__(self):
        super().__init__()
        LoggerClass.__init__(self)
        self.headers = [
            {
                'Accept': 'application/json',
                'Content-Type': 'application/json;charset=UTF-8'
            },
            {
                'Accept': 'application/json',
                'Authorization': "",
                'Content-Type': 'application/json;charset=UTF-8'
            }
        ]
        self.timeout = 60

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
            tk = requests.get(url=url, params=data, timeout=self.timeout, headers=self.headers[0])
            js_tk = tk.json()
            if js_tk['code'] == 200:
                return [js_tk['code'], js_tk['data']['token_type'] + " " + js_tk['data']['token']]
            else:
                self.write_log(f"{ql_tk[0]} 获取青龙Authorization异常 状态码: {js_tk['code']} 原因: {js_tk['data']}", level='debug')
                return [403]
        except Exception as e:
            self.write_log(f"{ql_tk[0]} 请求青龙异常: {e}", level='debug')
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
            headers = self.headers[1]
            headers['Authorization'] = ql_tk[4]
            ss = requests.put(url=url, headers=headers, data=json.dumps(data), timeout=self.timeout)
            status = ss.status_code
            # 获取返回的状态码
            if status == 200:
                return 0
            else:
                self.write_log(f"任务执行失败: {status}", level='debug')
                return -1
        except Exception as e:
            self.write_log(f"执行青龙任务失败，错误信息: {e}", level='debug')
            return -1

    def crons(self, ql_tk: list):
        """
        获取任务列表
        :param ql_tk: 青龙数据库的列表
        :return: [状态码, 列表]
        """
        try:
            url = ql_tk[1] + '/open/crons'
            headers = self.headers[1]
            headers['Authorization'] = ql_tk[4]
            lis = requests.get(url=url, headers=headers, timeout=self.timeout)
            li = lis.json()
            if li['code'] == 200:
                return [li['code'], li['data']]
            self.write_log(f"状态码: {li['code']} 请给相应权限", level='debug')
            return li['code']
        except Exception as e:
            self.write_log(f"获取青龙任务列表失败: {e}", level='debug')
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
            headers = self.headers[1]
            headers['Authorization'] = ql_tk[4]
            ss = requests.get(url=url, headers=headers, timeout=self.timeout)
            status = ss.status_code
            # 获取返回的状态码
            if status == 200:
                return ss.json()
            return {'code': 404}
        except Exception as e:
            self.write_log(f"获取配置文件内容失败: {e}", level='debug')
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
            headers = self.headers[1]
            headers['Authorization'] = ql_tk[4]
            ss = requests.post(url=url, headers=headers, data=json.dumps(cs), timeout=self.timeout)
            status = ss.status_code
            # 获取返回的状态码
            if status == 200:
                return ss.json()
            return {'code': 404}
        except Exception as e:
            self.write_log(f"修改配置文件内容失败: {e}", level='debug')
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
            headers = self.headers[1]
            headers['Authorization'] = ql_tk[4]
            ss = requests.put(url=url, headers=headers, data=json.dumps(data), timeout=self.timeout)
            status = ss.status_code
            # 获取返回的状态码
            if status == 200:
                self.write_log("禁用任务成功")
                return 0
            else:
                self.write_log(f"任务禁用失败: {status}", level='debug')
                return -1
        except Exception as e:
            self.write_log(f"执行青龙禁用任务失败，错误信息: {e}", level='debug')
            return -1
