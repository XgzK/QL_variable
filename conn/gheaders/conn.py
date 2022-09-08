"""
文件有关的函数
"""
import yaml


def read_yaml(file_name="./conn.yml"):
    """
    读取yaml文件
    :param file_name:默认读取./conn.yml
    :return data: 返回配置文件中的数据
    """
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            # 读取文件内容
            content = f.read()
            # 解析文件内容
            # 全局变量
            yam = yaml.load(content, Loader=yaml.FullLoader)
            # 关闭文件
            f.close()
            return yam
    except Exception as e:
        return -1


def revise_yaml(tx, sun, path='./conn.yml'):
    """
    指定行添加内容
    :param tx: 添加的值
    :param sun: 添加的行
    :param path: 添加的路径,默认./conn.yml
    :return:
    """
    f = open(path, 'r+', encoding='utf-8')
    flist = f.readlines()
    # ql行数从一开始，python读取从零开始
    try:
        flist[sun - 1] = '{}\n'.format(tx)
        f = open(path, 'w+', encoding='utf-8')
        f.writelines(flist)
        # 关闭文件
        f.close()
    except Exception as e:
        print("异常问题，revise_yaml：" + str(e))


def read_txt(file_name="./conn.yml"):
    """
    读取文件内容
    :param file_name:文件路径默认目录./conn.yml
    :return: 返回文件数据,异常返回-1
    """
    try:
        with open(file_name, mode='r', encoding='utf-8') as f:
            tx = f.readlines()
            f.close()
        return tx
    except Exception as e:
        return -1


def empty_txt(file_name="null"):
    """
    清空文件内容
    :param file_name:文件路径默认目录
    :return: 异常返回-1
    """
    try:
        with open(file_name, mode='w', encoding='utf-8') as f:
            f.write('')
            f.close()
    except Exception as e:
        return -1


def delete_first_lines(filename, count):
    """
    删除前多少行
    :param filename: 路径
    :param count: 行
    :return:
    """
    fin = open(filename, 'r', encoding='utf-8')
    a = fin.readlines()
    fout = open(filename, 'w', encoding='utf-8')
    b = ''.join(a[count:])
    fout.write(b)
