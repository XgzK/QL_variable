import os

from ..tools.log import LoggerClass
from ..tools.conn import ConnYml


class Father:
    AdReg = {
        # value记录值，初始化随便填，目前只适配了高级配置的key
    }

    def __init__(self):
        # 配置文件有关
        self.yml = ConnYml()
        self.read = self.yml.read_yaml
        self.revise = self.yml.revise_yml
        self.delete = self.yml.delete_first_lines
        self.log_object = LoggerClass()
        self.log_write = self.log_object.write_log
        # 用于记录是否需要更新
        self.Marking_time = 0

    def flash_Config(self):
        """
        把配置文件内容读取到AdReg中
        :return:
        """
        conf = self.read()
        for i in conf.keys():
            self.AdReg[i] = conf.get(i)

    def revise_Config(self, Key: str, Value):
        """
        修改配置文件覆盖原始值形式,动态录入
        :param Key:
        :param Value:
        :return: -1:修改的值和原先值类型不符，适用于bool-bool的验证
        """
        # 检测KEY在不在配置文件中
        Key = Key.split('.')
        if Key[0] in self.AdReg.keys():
            config = self.read()
            if len(Key) == 2:
                config[Key[0]][Key[1]] = Value
            else:
                config[Key[0]] = Value
            # 动态录入
            if type(Value) is bool:
                if not type(self.AdReg[Key[0]]) is bool:
                    self.log_write(f"提交的 {Key[0]} : {Value} 值类型不符")
                    return -1
            if len(Key) == 2:
                config[Key[0]][Key[1]] = Value
            else:
                config[Key[0]] = Value
            self.revise(config)
        else:
            self.log_write(f"提交的 {Key[0]} : {Value} 不在配置文件中")

    def marking_time(self):
        # 这一点是为了检测标记是否需要更新
        if self.Marking_time < int(os.environ.get('marking_time', 0)):
            self.flash_Config()
            self.Marking_time = int(os.environ.get('marking_time', 0))
            print("配置文件发生改变重新获取新的内容")
            return True
        return Father
