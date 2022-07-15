import json

import requests

from conn.gheaders.conn import read_yaml
from conn.gheaders.get_headers import ql_header
from conn.gheaders.log import log_ip
from conn.ql.ql_write import yml_file


def ql_lis():
    """
    获取青龙任务列表,用于对比数据
    :return:
    """
    try:
        jstx = read_yaml()
        # 判断所有获取所需的值，如果没有获取则跳过
        print(jstx['judge'])
        if jstx['judge'] == 0:
            url = jstx['ip'] + "/open/crons"
            ss = requests.get(url=url, headers=ql_header(), timeout=5)
            js = ss.json()
            with open(jstx['qljson'], mode='wt', encoding='utf-8') as f:
                json.dump(js, f, ensure_ascii=False)
                f.close()
        else:
            print("异常问题，没有获取到青龙的CK，后面将会不执行")
    except Exception as e:
        log_ip("ql_lis,异常信息" + str(e))
        # 如果异常返回添加这个拒绝执行后面任务
        yml_file("judge: 1", 19)


def vaguefind(str12):
    """
    对比脚本和获取的值找到运行青龙需要的数字
    :param str12: 传入脚本名称
    :return: 如果成功返回脚本的专属id,如果脚本不存在返回-1
    """
    try:
        # 获取的是文件路径
        jstx = read_yaml()
        with open(jstx['qljson'], mode='rt', encoding='utf-8') as f:
            json_res = f.read()
            l = json.loads(json_res)
            f.close()
        # 循环读取青龙脚本
        for i in range(len(l['data']) - 1):
            # 把多余的部分去掉
            cs = l['data'][i]['command'].split("/")
            # 对比脚本名称
            if cs[-1] == str12:
                print("脚本名称：" + str12 + "脚本id：" + str(l['data'][i]['id']))
                # 因为必须数组所以这里创建一个数组
                dd = [l['data'][i]['id']]
                # 如果对比成功立刻结束此方法
                log_ip("脚本: " + str12 + "名称: " + l['data'][i]['name'] + "id: " + str(l['data'][i]['id']))
                return dd
        # 如果运行到这里表示这个脚本你没有
        log_ip(str(str12) + "脚本不存在")
        return -1
    except Exception as e:
        log_ip("vaguefind,异常信息：" + str(e))
