"""
文件有关的函数
"""
import yaml


class ConnYml:

    def __init__(self):
        self.file_name = "./conn.yml"

    def read_yaml(self, file_name=""):
        """
        读取yaml文件
        :param file_name:默认读取./conn.yml
        :return data: {}
        """
        try:
            file_name = file_name if file_name else self.file_name
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
            return {}

    def revise_yaml(self, tx, sun, file_name=''):
        """
        指定行添加内容
        :param tx: 添加的值
        :param sun: 添加的行
        :param file_name: 添加的路径,默认./conn.yml
        :return:
        """
        file_name = file_name if file_name else self.file_name
        f = open(file_name, 'r+', encoding='utf-8')
        flist = f.readlines()

        # ql行数从一开始，python读取从零开始
        try:
            flist[sun - 1] = '{}\n'.format(tx)
            f = open(file_name, 'w+', encoding='utf-8')
            f.writelines(flist)
        except Exception as e:
            print("异常问题，revise_yaml：" + str(e))
        finally:
            f.close()

    def read_txt(self, file_name=""):
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
            return -1

    def empty_txt(self, file_name=""):
        """
        清空文件内容
        :param file_name:文件路径默认目录
        :return: 异常返回-1
        """
        try:
            file_name = file_name if file_name else self.file_name
            with open(file_name, mode='w', encoding='utf-8') as f:
                f.write('')
        except Exception as e:
            return -1

    def delete_first_lines(self, count, file_name=""):
        """
        删除前多少行
        :param count: 行
        :param file_name: 路径
        :return:
        """
        global fin, fout
        try:
            file_name = file_name if file_name else self.file_name
            fin = open(file_name, 'r', encoding='utf-8')
            a = fin.readlines()
            fout = open(file_name, 'w', encoding='utf-8')
            b = ''.join(a[count:])
            fout.write(b)
        except Exception as e:
            print(e)
        finally:
            fin.close()
            fout.close()

    def yml_file(self, tx, sun, file_name=''):
        """

        :param tx: 添加的值
        :param sun: 添加的行
        :param file_name: 添加的路径默认./conn.yml
        :return:
        """
        global f, f1
        try:
            file_name = file_name if file_name else self.file_name

            f = open(file_name, 'r+', encoding='utf-8')
            flist = f.readlines()
            # ql行数从一开始，python读取从零开始

            flist[sun - 1] = '{}\n'.format(tx)
            f1 = open(file_name, 'w+', encoding='utf-8')
            f1.writelines(flist)
        except Exception as e:
            print("异常问题，yml_file：" + str(e))
        finally:
            f.close()
            f1.close()
