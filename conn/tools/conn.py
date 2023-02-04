"""
文件有关的函数
"""
import os

from ruamel.yaml import YAML

yaml = YAML(typ='safe')


class ConnYml:

    def __init__(self):
        self.file_name = "conn.yml"
        self.template = {
            "Administrator": "",
            "Token": "",
            "Send_IDs": "",
            "prohibit": [' '],
            "Proxy": {
                "Proxy": "",
                "TG_API_HOST": "https://api.telegram.org",
                "JK_ALL_PROXY": ""
            },
            "deduplication": 0,
            "json": "data/",
            "log": "log/ql.log",
            "repeat": "repeat.sqlite",
            "kill": [
                "kill -9 $(netstat -nlp | grep fsbot | awk '{print $7}' | awk -F'/' '{ print $1 }')",
                "kill -9 $(netstat -nlp | grep :5008 | awk '{print $7}' | awk -F'/' '{ print $1 }')"
            ],
            "Delay": 0
        }

    def creat_yml(self, file_name="") -> int:
        """
        创建yaml文件，并且补全丢失变量
        """
        file_name = file_name if file_name else self.file_name
        _remake_when_replenish_list = ["kill"]  # 当补充值时，重置此list中的key对应的template
        _remake_flag = False
        # 检测文件是否存在
        if not os.path.exists(file_name):
            with open(file_name, mode='w+', encoding="utf-8") as file:
                yaml.dump(self.template, file)
                file.close()
                return 0
        else:
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    data = yaml.load(f)
                    f.close()
                with open(file_name, 'w', encoding='utf-8') as f:
                    _tmp_dict = dict(data)
                    for _key in _tmp_dict:
                        # 把多余的删除
                        if _key not in self.template:
                            data.pop(_key)
                        # 获取第二阶级
                        elif type(self.template.get(_key)) == dict:

                            if type(self.template.get(_key).keys()) not in type(data.get(_key).keys()):
                                # 第二层检测
                                for j in _tmp_dict.get(_key).keys():
                                    if j not in self.template.get(_key).keys():
                                        data.get(_key).pop(j)

                    for key in self.template:
                        if key not in data:
                            data.setdefault(key, self.template.get(key))
                            _remake_flag = True
                            continue
                        elif type(self.template.get(key)) == dict:

                            if type(self.template.get(key).keys()) in type(data.get(key).keys()):
                                # 第二层检测
                                for j in self.template.get(key).keys():
                                    if j not in data.keys():
                                        data.get(key).setdefault(j, self.template.get(key).get(j))
                                        _remake_flag = True

                    if _remake_flag:
                        for key in _remake_when_replenish_list:
                            data[key] = self.template.get(key)

                    yaml.dump(data, f)
                    f.close()
            except TypeError:
                with open(file_name, mode='w', encoding="utf-8") as file:
                    yaml.dump(self.template, file)
                    file.close()
                    return 0

    def read_yaml(self, file_name="") -> dict:
        """
        读取yaml文件
        :param file_name:默认读取./conn.yml
        :return data: {}
        """
        try:
            file_name = file_name if file_name else self.file_name
            with open(file_name, 'r', encoding='utf-8') as f:
                data = yaml.load(f)
                # 关闭文件
                f.close()
                return data
        except Exception as e:
            return {}

    def revise_yml(self, data, path='./conn.yml') -> int:
        """
        修改yml配置文件
        :param data: 添加的值
        :param path: 添加的路径,默认./conn.yml
        :return: 正常返回 0 非正常 -1
        """
        with open(path, mode='r', encoding="utf-8") as file:
            old_data = yaml.load(file)
            file.close()
        try:
            with open(path, mode='w', encoding="utf-8") as file:
                yaml.dump(data, file)
                file.close()
                return 0
        except Exception as e:
            file.close()
            print("异常问题回滚，revise_yaml：" + str(e))
            with open(path, mode='w', encoding="utf-8") as file:
                yaml.dump(old_data, file)
                file.close()
            return -1

    def read_txt(self, file_name="") -> list:
        """
        读取文件内容
        :param file_name:文件路径默认目录./conn.yml
        :return: 返回文件数据,异常返回-1
        """
        try:
            file_name = file_name if file_name else self.file_name
            with open(file_name, mode='r', encoding='utf-8') as f:
                tx = f.readlines()
                f.close()
            return tx
        except Exception as e:
            return []

    def empty_txt(self, file_name="") -> int:
        """
        清空文件内容
        :param file_name:文件路径默认目录
        :return: 异常返回-1
        """
        try:
            file_name = file_name if file_name else self.file_name
            with open(file_name, mode='w', encoding='utf-8') as f:
                f.write('')
                return 0
        except Exception as e:
            return -1

    def delete_first_lines(self, filename, count) -> int:
        """
        删除前多少行
        :param filename: 路径
        :param count: 行
        :return:
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                a = f.readlines()
            with open(filename, 'w', encoding='utf-8') as fout:
                b = ''.join(a[count:])
                fout.write(b)
            return 0
        except Exception as e:
            return -1
        finally:
            f.close()
            fout.close()
