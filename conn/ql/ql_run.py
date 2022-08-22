import json
import time
import requests

from conn.gheaders.conn import read_yaml
from conn.gheaders.get_headers import ql_header
from conn.gheaders.log import LoggerClass

logger = LoggerClass('debug')


def ql_run(data):
    """
    执行青龙任务
    :param data: int数组
    :return:
    """
    try:
        ip = read_yaml()
        url = ip['ip'] + '/open/crons/run'
        ss = requests.put(url=url, headers=ql_header(), data=json.dumps(data), timeout=10)
        status = ss.status_code
        # 获取返回的状态码
        if status == 200:
            # 延迟3秒
            time.sleep(3)
            logger.write_log("任务执行成功")
        else:
            logger.write_log("任务执行失败:" + str(status))
    except Exception as e:
        logger.write_log("执行青龙任务失败，错误信息：" + str(e))
