from conn.gheaders.conn import read_yaml
from conn.gheaders.log import LoggerClass
from conn.gheaders.ti import date_minutes
from conn.ql.ql_write import yml_file
from conn.sql.addsql import insert_data, select_datati

logger = LoggerClass('debug')
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
        logger.logger("descend,异常信息：" + str(e))


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
        logger.logger("del_file,异常信息：" + str(e))


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
            # 针对某些不需要去重复的数据，如果不是exp则不去重复
            if str12[:3] == "exp":
                # 添加到数据库，如果成功添加表示之前没有运行过
                print("添加到数据库")
                st = insert_data(str12, date_minutes())
                print(st)
                if st == 0:
                    return deduplication(str12)
                else:
                    inquire = select_datati(str12)
                    logger.write_log("===========================================================")
                    logger.write_log("参数已经执行过" + str(str12) + "不再重复执行")
                    logger.write_log("在 " + str(inquire[0][1]) + " 数据库中参数是 " + str(inquire[0][0]) + "所以不再重复执行")
                    logger.write_log("===========================================================")
                    return -1
            else:
                print(str12[3:])
                # 把后端添加的前3位去掉
                return deduplication(str12[3:])
        else:
            return deduplication(str12)
    except Exception as e:
        logger.write_log("ql_write,异常信息：" + str(e))
        return -1
