import sqlite3

from conn.gheaders.conn import read_yaml


# 创建数据库方法



def create_db():
    """
    获取虚拟数据库连接
    :return: 返回数据库连接和游标,异常返回1
    """
    try:
        # 获取数据库连接
        db = sqlite3.connect("conn/sql/db.sqlite")
        # 创建游标
        cursor = db.cursor()
        return cursor, db
    except Exception as e:
        return 1


# 插入数据方法
def insert_data(id, jd_name, jd_js, jd_value1, jd_value2=None, jd_value3=None, jd_url=None, jd_re=None) -> int | Exception:
    """
    插入一条数据
    :param id: id 唯一标识
    :param jd_name: 脚本中文名，不能为空,唯一
    :param jd_js: 脚本名，不能为空，唯一
    :param jd_value1: 参数1，不能为空
    :param jd_value2: 参数2
    :param jd_value3: 参数3
    :param jd_url: 活动链接一部分
    :param jd_re: 设置的正则表达式
    :return: 返回0表示插入成功，返回1表示插入失败
    """
    try:
        # 获取sql连接
        cursor, db = create_db()
        # 插入数据 ip, port,  protocol, country
        cursor.execute(
            f"insert into JdQl values('{id}','{jd_name}','{jd_js}','{jd_value1}', '{jd_value2}', '{jd_value3}', '{jd_url}', '{jd_re}')")
        # cursor.execute("insert into ip values('%s',)" %)
        db.commit()
        # 关闭数据库
        db.close()
        return 0
    except Exception as e:
        return e


# 查询数据方法
def select_data(data='*', value='None') -> list:
    """
    查询数据
    :param data: 查询的字段,默认为*
    :param value: 查询的值,默认为None
    :return: 查询结果,异常返回1
    """
    try:
        # 获取数据库连接
        cursor, db = create_db()
        # 查询数据
        if value == 'None':
            cursor.execute(f"select {data} from JdQl order by id asc")
        else:
            cursor.execute(f"select {data} from JdQl where {value}")
        # 获取数据
        data = cursor.fetchall()
        # 关闭数据库
        db.close()
        return data
    except Exception as e:
        return []


# 删除所有数据方法
def delete_data() -> int | Exception:
    """
    删除数据,别调用调用了自己修
    :return: 返回0表示有数据并且删除成功，返回1表示没有成功
    """
    try:
        # 获取数据库连接
        cursor, db = create_db()
        # 删除数据
        cursor.execute('delete from JdQl')
        db.commit()
        # 关闭数据库
        db.close()
        return 0
    except Exception as e:
        return e


# 删除某一条数据方法
def delete_one_data(key, value) -> int | Exception:
    """
    删除某一条数据方法
    :param key: 字段名
    :param value: 字段值
    :return: 返回0表示有数据并且删除成功，返回e表示没有数据
    """
    try:
        # 获取数据库连接
        cursor, db = create_db()
        # 删除数据
        cursor.execute(f"delete from JdQl where {key}='{value}'")
        db.commit()
        # 关闭数据库
        db.close()
        return 0
    except Exception as e:
        return e


def update_date(token, day) -> int | Exception:
    """
    修改数据，根据token的值，修改day
    :param token:
    :param day:
    :return: 修改结果,异常返回1，正常返回0
    """
    try:
        # 获取数据库连接
        cursor, db = create_db()
        # 修改数据
        cursor.execute(f"update sign set day = {day} where token = '{token}'")
        # cursor.execute("insert into ip values('%s',)" %)
        db.commit()
        # 关闭数据库
        db.close()
        return 0
    except Exception as e:
        return e
