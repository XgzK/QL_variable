import logging
import re
from datetime import datetime
from sys import stdout

import colorlog
import os

from logging.handlers import RotatingFileHandler

from com.Web.ws_send import send_message
from com.gheaders.conn import ConnYml

cooyml = ConnYml()


class LoggerClass:
    logFile = cooyml.read_yaml()['log']  # 定义日志存储的文件夹
    log_colors_config = {
        'DEBUG': 'cyan',
        'INFO': 'purple',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }

    def __init__(self, level='info'):
        self.level = level
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

    def write_log(self, message, level=""):
        """
       #日志输出到控制台
       console=logging.StreamHandler()
       self.logger.addHandler(console)
       """
        lev = level if level else self.level
        msg_format = f'[{lev}]-\t{message}'
        try:
            if lev == 'debug':
                self.logger.debug(msg=msg_format)
                send_message(f"{self.TimeStampToTime()}\t{msg_format}")
            elif lev == 'info':
                self.logger.info(msg=msg_format)
                send_message(f"{self.TimeStampToTime()}\t{msg_format}")
            elif lev == 'warning':
                self.logger.warning(msg=msg_format)
                send_message(f"{self.TimeStampToTime()}\t{msg_format}")
            elif lev == 'error':
                self.logger.error(msg=msg_format)
                send_message(f"{self.TimeStampToTime()}\t{msg_format}")
            else:
                self.logger.critical(msg=msg_format)
                send_message(f"{self.TimeStampToTime()}\t{msg_format}")
        except Exception as e:
            print("日志写入权限错误：", e)

    def TimeStampToTime(self):
        """
        伪造日志时间
        :return:
        """
        return str("[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f]')[:-4] + "]")

    def read_log(self):
        """
        读取日志文件
        :return: 打印html格式的日志，异常返回-1
        """
        try:
            st = []
            rz1 = cooyml.read_txt(self.logFile)
            if rz1 == -1:
                return []
            if len(rz1) > 100:
                cooyml.delete_first_lines(-100, self.logFile)
            sun = 0
            # 颠倒数组顺序
            rz1.reverse()
            # 遍历所有行
            for i in rz1:
                if sun < 100:
                    sun += 1
                else:
                    break
                # 如果就\n则跳过
                if i == '\n':
                    continue
                j = i.replace("[35m", "") \
                    .replace("[0m", "") \
                    .replace("[33m", "") \
                    .replace("[36m", "") \
                    .replace("[31m", "") \
                    .replace("\n", "")
                if j:
                    st.append(j)
                    continue
            # 把颠倒的顺序颠倒回来
            st.reverse()
            return st
        except Exception as e:
            return [f'日志文件异常: {e}']
