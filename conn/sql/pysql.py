import sqlite3

from conn.gheaders.conn import read_yaml


def create_db():
    """
    创建数据库
    :return:
    """
    # 创建数据库
    db = sqlite3.connect(read_yaml()["db"])
    # 创建游标
    cursor = db.cursor()
    return cursor, db


def select_data() -> list:
    """
    查询数据
    :return: 返回数组
    """
    try:
        # 创建数据库
        cursor, db = create_db()
        # 查询数据
        cursor.execute('select * from Crontabs')
        data = cursor.fetchall()
        # 关闭数据库
        db.close()
        return data
    except Exception as e:
        print("数据库异常信息,表不存在: ", e)
        return [-1]
