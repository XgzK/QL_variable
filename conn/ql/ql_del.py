from conn.gheaders.conn import read_yaml
from conn.gheaders.log import log_ip
from conn.ql.ql_write import yml_file
from conn.sql.addsql import insert_data


def descend():
    """
    用于读取青龙配置文件的末尾，并添加到conn.yml指定行
    :return:
    """
    try:
        yml = read_yaml()
        file = open(yml['qlpath'], 'r', encoding="utf-8")
        lines = file.readlines()
        str1 = 'delql: ' + str(len(lines))
        yml_file(str1, yml['Record']['delql'])
        file.close()
    except Exception as e:
        log_ip("descend,异常信息：" + str(e))


def del_file():
    """
    删除添加的行,但是保留sun行，获取到的是文件的行数，删除行后面的内容
    :return:
    """
    try:
        yml = read_yaml()
        file = open(yml['qlpath'], encoding="utf-8")
        lines = file.readlines()
        del lines[yml['delql']::]  # 删除最后一行
        # lines.append("\n")
        file.close()

        file_new = open(yml['qlpath'], 'w', encoding="utf-8")
        file_new.writelines(lines)  # 将删除行后的数据写入文件
        file_new.close()
    except Exception as e:
        log_ip("del_file,异常信息：" + str(e))


def deduplication(str12):
    """
    添加到内容到青龙配置文件
    :param str12: 传入内容
    :return:
    """
    yml = read_yaml()
    file = open(yml['qlpath'], 'a', encoding="utf-8")
    file.write("\n" + str12)
    file.close()
    return 0


def ql_write(str12):
    """
    写入青龙任务列表，把内容添加到文件最后一行
    :param str12: 传入内容
    :return: 如果没有执行过返回0，如果执行过返回-1
    """
    try:
        deve = read_yaml()
        # 判断是否去重数据
        if deve['deduplication'] == 0:
            # 添加到数据库，如果成功添加表示之前没有运行过
            st = insert_data(str12)
            if st == 0:
                return deduplication(str12)
            else:
                log_ip("参数已经执行过" + str(str12) + "不再重复执行")
                return -1
        else:
            return deduplication(str12)
    except Exception as e:
        log_ip("ql_write,异常信息：" + str(e))
        return -1
