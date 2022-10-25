"""
京东活动签到
"""
from conn.sql.JD_ql import create_db


def to_insert(token, day=7):
    """
    插入数据
    :param token: 获取的 token参数
    :param day: 记录执行的天数，默认为7天
    :return: 插入结果,异常返回-1，正常返回0
    """
    global db
    try:
        # 获取sql连接
        cursor, db = create_db()
        # 插入数据 ip, port,  protocol, country
        cursor.execute(f"insert into sign (token, day) values('{token}', '{day}')")
        # cursor.execute("insert into ip values('%s',)" %)
        db.commit()

        return [0]
    except Exception as e:
        print(e)
        return [-1, str(e)]
    finally:
        # 关闭数据库
        db.close()


def to_update(token, day):
    """
    修改数据，根据token的值，修改day
    :param token: 获取的 token参数
    :param day: 记录执行的天数，默认为7天
    :return: 修改结果,异常返回1，正常返回0
    """
    global db
    try:
        # 获取数据库连接
        cursor, db = create_db()
        # 修改数据
        cursor.execute(f"update sign set day = {day} where token = '{token}'")
        # cursor.execute("insert into ip values('%s',)" %)
        db.commit()
        return 0
    except Exception as e:
        return 1
    finally:
        # 关闭数据库
        db.close()


def to_select(value='*'):
    """
    查询数据
    :param value: 查询的值,默认为*查询所有
    :return: 查询结果,异常返回1
    """
    global db
    try:
        # 获取数据库连接
        cursor, db = create_db()
        # 查询数据
        # 查询所有
        if value == '*':
            cursor.execute("select * from sign")
        # 查询单个
        else:
            cursor.execute(f"select * from sign where token = '{value}'")
        # 获取数据
        data = cursor.fetchall()
        return data
    except Exception as e:
        return []
    finally:
        # 关闭数据库
        db.close()


def to_delete(value):
    """
    删除数据单个或删除全部
    :param value: 删除的值
    :return: 删除结果,异常返回1
    """
    global db
    try:
        # 获取数据库连接
        cursor, db = create_db()
        # 删除数据
        # 删除单个
        if value != '*':
            cursor.execute(f"delete from sign where token = '{value}'")
        # 删除全部
        else:
            cursor.execute("delete from sign")
        # 提交数据
        db.commit()
        # 关闭数据库
        return 0
    except Exception as e:
        return e
    finally:
        db.close()
