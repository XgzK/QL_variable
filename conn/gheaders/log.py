import logging
import re
import time
from sys import stdout

import colorlog
import os

from logging.handlers import RotatingFileHandler

from conn.gheaders.conn import read_yaml, read_txt

yml = read_yaml()


class LoggerClass:
    logFile = yml['log']  # 定义日志存储的文件夹
    log_colors_config = {
        'DEBUG': 'cyan',
        'INFO': 'purple',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }

    def __init__(self, level='info', fmt=None):
        # [%(name)s] \t
        self.norm_fomatter = colorlog.ColoredFormatter(f'%(log_color)s[%(asctime)s]\t'
                                                       '%(message)s',
                                                       log_colors=self.log_colors_config)
        # 提取路径
        pa = re.findall('(.*?)/\w+\.log', self.logFile)
        if pa:
            if not os.path.exists(pa[0]):  # 判断日志存储文件夹是否存在，不存在，则新建
                os.makedirs(pa[0])
        # 初始化日志类参数
        self.logger = logging.getLogger(__name__)
        # self.logger.setLevel(self.level_relations.get(level))
        self.logger.setLevel('DEBUG')
        # 生成以当天日期为名称的日志文件
        self.filename = self.logFile
        # 定义日志输出到前面定义的filename中
        print(self.filename)
        self.filelogger = RotatingFileHandler(self.logFile, 'a+', encoding="UTF-8")
        self.filelogger.setLevel('DEBUG')  # 设置Handler级别
        # self.filelogger.setLevel(self.level_relations.get(level))
        # 定义日志输出的格式
        # formatter = logging.Formatter(fmt)
        # asctime可能用不了
        self.filelogger.setFormatter(self.norm_fomatter)

        # 控制台
        self.norm_hdl_std = logging.StreamHandler(stdout)
        self.norm_hdl_std.setLevel('DEBUG')  # 设置Handler级别
        self.norm_hdl_std.setFormatter(self.norm_fomatter)

        if not self.logger.handlers:
            self.logger.addHandler(self.norm_hdl_std)
            self.logger.addHandler(self.filelogger)

    def write_log(self, message, level="info"):
        """
       #日志输出到控制台
       console=logging.StreamHandler()
       self.logger.addHandler(console)
       """

        # 暂不记录在哪行哪个方法，隐藏
        # frame = sys._getframe().f_back
        # funcName = frame.f_code.co_name
        # lineNumber = frame.f_lineno
        # fileName = frame.f_code.co_filename

        lev = level.lower()
        # msg_format = f'{pre_format_str} [{lev}]-\t{message}'
        msg_format = f'[{lev}]-\t{message}'
        try:
            if lev == 'debug':
                self.logger.debug(msg=msg_format)
            elif lev == 'info':
                self.logger.info(msg=msg_format)
            elif lev == 'warning':
                self.logger.warning(msg=msg_format)
            elif lev == 'error':
                self.logger.error(msg=msg_format)
            else:
                self.logger.critical(msg=msg_format)
        except Exception as e:
            print("日志写入权限错误：", e)

    # class LogHandleError(Exception):
    #     print("日志级别错误")
    #     # "日志级别错误"
    #     pass

    # def del_log():
    #     # 当文件大于1M时，删除文件
    #     if os.path.getsize(path) > 1242880:
    #         os.remove(path)

    def get_file_sorted(self, file_path):
        """最后修改时间顺序升序排列 os.path.getmtime()->获取文件最后修改时间"""
        dir_list = os.listdir(file_path)
        if not dir_list:
            return
        else:
            dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
            return dir_list

    def TimeStampToTime(self, timestamp):
        """格式化时间"""
        timeStruct = time.localtime(timestamp)
        return str(time.strftime('%Y-%m-%d', timeStruct))

    def handle_logs(self):
        """
        因为日志类问题没办法使用天切换只能打开日志文件并且清空
        """
        f = open(self.filename, 'w', encoding='utf-8')
        f.close()

    def delete_logs(self, file_path):
        try:
            os.remove(file_path)
            # print(file_path)
        except PermissionError as e:
            # self.norm_log.error('删除日志文件失败：{}'.format(e))
            pass


def rz():
    """
    读取日志文件
    :return: 打印html格式的日志，异常返回-1
    """
    try:
        sun = ''
        __count = 0
        if yml == -1:
            return -1
        log = yml['log']
        # print(log)
        rz1 = read_txt(log)
        if rz1 == -1:
            return -1
        # 遍历所有行
        for i in rz1:
            # print(i)
            if __count > 100:
                __count = 0
                sun = ''
            # 如果就\n则跳过
            if i == '\n':
                # __count += 1
                # print(__count)
                continue
            #  把末尾的\n换成<br>
            # j = i.replace('\n', '<br>')
            j = re.findall(r"\[\d+m(.*)\x1b", i)
            if j:
                sun += j[0] + "<br>"
                __count += 1
                continue
            j = re.findall(r"\d+m(.*)", i)
            if j:
                sun += j[0] + "<br>"
                __count += 1
                continue
        return sun
    except Exception as e:
        return -1


def def_log():
    """
    删除日志
    :return:
    """
    lo = yml['log']
    with open(lo, 'w', encoding='utf-8') as f:
        # 关闭文件
        f.close()