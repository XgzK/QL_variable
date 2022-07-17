"""
文件有关的函数
"""
import yaml


def read_yaml(file_name="./conn.yml"):
    """
    读取yaml文件
    :param file_name:
    :return data: 返回配置文件中的数据
    """
    with open(file_name, 'r', encoding='utf-8') as f:
        # 读取文件内容
        content = f.read()
        # 解析文件内容
        # 全局变量
        yam = yaml.load(content, Loader=yaml.FullLoader)
        return yam


# 读取txt文件
def read_txt(file_name="./conn.txt"):
    """
    读取txt文件
    :param file_name:
    :return data: 返回配置文件中的数据
    """
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            # 按行读取
            content = f.readlines()
            # 关闭文件
            f.close()
            return content
    except Exception as e:
        return -1
