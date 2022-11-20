"""
青龙接口类
"""
import json
import time

import requests

from com.gheaders.conn import read_yaml
from com.gheaders.get_headers import ql_header, qlck_header
from com.gheaders.log import LoggerClass

logger = LoggerClass('debug')
yam = read_yaml()


class QL:
    def __init__(self):
        self.headers = ql_header

    def ql_tk(self):
        """
        用于获取登录用的ck,ck有效期一个月
        :return: 返回登录用的Bearer XXXXXXXXXXX，如果没有获取到，返回0
        """
        yal = read_yaml()
        url = str(yal['ip']) + "/open/auth/token"
        data = {
            'client_id': yal['Client ID'],
            'client_secret': yal['Client Secret']
        }
        try:
            cs = requests.get(url=url, params=data, timeout=10, headers=qlck_header())
            jstx = cs.json()
            return jstx['data']['token_type'] + " " + jstx['data']['token']
        except Exception as e:
            logger.write_log("ql_tk异常信息，请检查conn.yml文件，异常信息: " + str(e))
            logger.write_log(f"请求的参数是 {url}?client_id:{data['client_id']}&client_secret:{data['client_secret']}")
            return -1

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
                time.sleep(90) if int(time.strftime('%H')) == 0 else time.sleep(0.3)
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
            return -1
        except Exception as e:
            logger.write_log("获取青龙任务列表失败", e)
            return -1

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
            return {'code': 404}

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
            return {'code': 404}

    def system_version(self):
        """
        青龙版本号
        :return:
        """
        url = ''
        try:
            yam = read_yaml()
            url = yam['ip'] + "/api/system"
            ver = requests.get(url)
            js = ver.json()
            if js['code'] == 200:
                return js['data']['version']
        except Exception as e:
            logger.write_log(f"获取版本号异常请到青龙所在服务器执行 curl {url} 命令如果返回 " + '{"code":200,"data":{"isInitialized":true,"version":"2.XX.X"}} 就联系管理员')
            return -1

    def disable(self, data):
        """
        禁用青龙任务
        :param data: int数组
        :return: 0 or -1
        """
        try:
            ur = read_yaml()
            url = ur['ip'] + '/open/crons/disable'
            ss = requests.put(url=url, headers=self.headers(), data=json.dumps(data), timeout=10)
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
