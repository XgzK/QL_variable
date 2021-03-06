import sqlite3

from conn.gheaders.conn import read_yaml

"""
用于去重复的数据
"""


def create_db():
    """
    创建数据库
    :return:
    """
    # 创建数据库
    db = sqlite3.connect(read_yaml()["repeat"])
    # 创建游标
    cursor = db.cursor()
    return cursor, db


# 创建表方法
def create_table():
    """
    创建表
    :return:
    """
    # 创建数据库
    cursor, db = create_db()
    # 创建表 ip= 服务器ip port=端口 protocol=协议 country=国家，ip不能为空和唯一
    cursor.execute('CREATE TABLE `repeat` (`jd_value1` varchar(255) NOT NULL UNIQUE)')
    # 关闭数据库
    db.close()


# 插入数据方法
def insert_data(jd_value1, jd_data):
    """
    插入数据
    :param jd_value1: 传入的数据
    :param jd_data: 传入的数据
    :return: 添加成功返回0，失败返回-1
    """
    try:
        # 创建数据库
        cursor, db = create_db()
        # 插入数据
        cursor.execute('INSERT INTO `repeat` VALUES (?,?)', (jd_value1, jd_data))
        # 提交数据
        db.commit()
        # 关闭数据库
        db.close()
        return 0
    except Exception as e:
        return -1


# 查询数据方法
def select_datati(value1):
    """
    查询数据
    :param value1: 传入的数据
    :return: 返回查询到的数据
    """
    try:
        # 创建数据库
        cursor, db = create_db()
        # 查询数据
        cursor.execute('select * from repeat WHERE jd_value1 = ?', (value1,))
        data = cursor.fetchall()
        # 关闭数据库
        db.close()
        return data
    except Exception as e:
        return -1
