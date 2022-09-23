"""
禁用青龙活动任务
"""
import re

import requests

from conn.gheaders.conn import read_yaml

yam = read_yaml()


class Prohibition:
    def __init__(self):
        pass

    def get_re(self):
        """
        获取爬虫端的数据库
        :return:
        """
        url = re.findall('(https?://.*?/)', yam['url'])[0] + 'sql'
        sqli = requests.post(url, timeout=20)
        return sqli.json()

    def compareds(self, jst: str, va: int) -> list:
        """
        遍历青龙任务来对比,获取任务ID返回多个
        :param jst: 脚本名称
        :param va: 版本号
        :return: ID or -1
        """
        try:
            li = []
            jstx = read_yaml(yam['json'])
            va1 = jstx if int(va) < 14 else jstx['data']
            # 找到脚本立即停止
            for i in va1:
                for j in jst:
                    if i['command'].split('/')[-1] == j[2]:
                        # 适配版本10
                        if int(va) == 10:
                            li.append(i['_id'])
                        else:
                            li.append(i['id'])
            return li
        except Exception as e:
            print(e)
            return [-1]
