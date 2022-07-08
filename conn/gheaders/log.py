import logging
import os
import time

from conn.gheaders.conn import read_yaml

path = read_yaml()['log']
# 1.创建日志器对象
logger = logging.getLogger()
# 2.创建处理器(控制台)
file_handle = logging.FileHandler(path, mode='a', encoding="utf-8")
# 控制台的等级
file_handle.setLevel(level="ERROR")
logger.addHandler(file_handle)


def log_ip(data):
    aa = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    logging.error(f"{aa} : {data}")
    file_handle.close()
    dele_ip()


def dele_ip():
    # 当文件大于10M时，删除文件
    if os.path.getsize(path) > 10485760:
        os.remove(path)
        print("删除文件")
