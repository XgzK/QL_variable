"""
模板库
"""
from com.gheaders.conn import ConnYml
from com.gheaders.log import LoggerClass

yml = ConnYml()


class Father:
    AdReg = {
        # value记录值，初始化随便填，目前只适配了高级配置的key
    }

    def __init__(self):
        # 配置文件有关
        self.read = yml.read_yaml
        self.revise = yml.revise_yml
        self.delete = yml.delete_first_lines
        self.flash_Config()

        # 日志
        self.log_object = LoggerClass()
        self.log_write = self.log_object.write_log

    def flash_Config(self):
        """
        把配置文件内容读取到AdReg中
        :return:
        """
        conf = self.read()
        for i in conf.keys():
            self.AdReg[i] = conf.get(i)

    def revise_Config(self, Key:str, Value):
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
