# -*- coding: utf-8 -*-
import os

"""
自动添加进程守护，每次启动时，先杀死进程，再重启
只有在启动的时候才会杀死进程，其他时候不会杀死进程
如果用户使用守护进程启动，则不会杀死进程
"""


def process_kill(process_name):
    """
    杀死进程之前进程，防止重复启动，并添加新的进程
    :param process_name:ps -ef|grep firefox|awk '{print $2}'|xargs kill -9
    :return:
    """
    # ps -ef|grep ql_cs.py |grep -v grep|awk '{print $2}'|xargs kill -9
    os.system("ps -ef|grep %s |grep -v grep|awk '{print $2}'|xargs kill -9" % process_name)
    # 重启进程 nohup python3 ip_broker.py & > ip_brok.log 2>&1
    os.system("nohup python3 %s &" % process_name)
    print("添加进程守护成功")


process_kill("ql_cs.py")
