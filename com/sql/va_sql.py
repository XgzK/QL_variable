import sqlite3
from sqlite3 import IntegrityError

from com.gheaders.conn import read_yaml

"""
数据库类
"""
yam = read_yaml()


class Sql:
    """
    授权数据库类
    """

    def __init__(self):
        # 172.17.0.2 localhost
        self.conn = sqlite3.connect(yam["repeat"], timeout=10, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.surface = ['JdQl', 'repeat']

    def execute(self, sql):
        """
            返回执行execute()方法后影响的行数
            :param self:
            :param sql:
            :return:
            """
        self.cursor.execute(sql)
        rowcount = self.cursor.rowcount
        return rowcount

    def delete(self, **kwargs):
        """
        删除并返回影响行数
        table="表", where="列 = 值"
        :param kwargs:
        :return:
        """
        table = kwargs['table']
        where = kwargs['where'] if 'where' in kwargs else None
        if where:
            sql = f'DELETE FROM {table} where {where}'
        else:
            sql = f'DELETE FROM {table}'
        # print(sql)
        global rowcount
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            # 影响的行数
            rowcount = self.cursor.rowcount
        except Exception as e:
            # 发生错误时回滚
            self.conn.rollback()
            return str(e)
        return rowcount

    def insert(self, **kwargs):
        """
        返回添加的ID
        table="表", 列1="值", 列2="值"
        :param kwargs:
        :return:
        """
        table = kwargs['table']
        del kwargs['table']
        sql = 'insert into %s(' % table
        fields = ""
        values = ""
        for k, v in kwargs.items():
            fields += "%s," % k
            values += "'%s'," % v
        fields = fields.rstrip(',')
        values = values.rstrip(',')
        sql = sql + fields + ") values(" + values + ")"
        # print(sql)
        global res
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            # 获取自增id
            res = self.cursor.lastrowid
        except IntegrityError:
            # 发生错误时回滚
            self.conn.rollback()
            return "请不要重复获取授权"
        except Exception as e:
            # 发生错误时回滚
            self.conn.rollback()
            return str(e)
        return res

    def update(self, **kwargs):
        """
        修改数据返回影响的行
        table="表", 列="值", 列="值", where="列="值""
        :param kwargs:
        :return:
        """
        table = kwargs['table']
        # del kwargs['table']
        kwargs.pop('table')
        where = kwargs['where']
        kwargs.pop('where')
        sql = 'update %s set ' % table
        for k, v in kwargs.items():
            sql += "%s='%s'," % (k, v)
        sql = sql.rstrip(',')
        sql += ' where %s' % where
        # print(sql)
        global rowcount
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            # 影响的行数
            rowcount = self.cursor.rowcount
        except Exception as e:
            # 发生错误时回滚
            self.conn.rollback()
            return str(e)
        return rowcount

    def selectTopone(self, **kwargs):
        """
        查-一条条数据
        :param kwargs:
        :return:
        """
        table = kwargs['table']
        field = 'field' in kwargs and kwargs['field'] or '*'
        where = 'where' in kwargs and 'where ' + kwargs['where'] or ''
        order = 'order' in kwargs and 'order by ' + kwargs['order'] or ''
        sql = 'select %s from %s %s %s limit 1' % (field, table, where, order)
        # print(sql)
        global data
        try:
            # 实时刷新 self.conn.commit()
            # self.conn.commit()
            # 执行SQL语句
            self.cursor.execute(sql)
            # 使用 fetchone() 方法获取单条数据.
            data = self.cursor.fetchone()
        except Exception as e:
            # 发生错误时回滚
            self.conn.rollback()
            return str(e)
        return data

    def selectAll(self, **kwargs):
        """
        查所有数据
        table="表", where="列 = '值'"
        :param kwargs:
        :return:
        """
        # table
        table = kwargs['table']
        field = 'field' in kwargs and kwargs['field'] or '*'
        where = 'where' in kwargs and 'where ' + kwargs['where'] or ''
        order = 'order' in kwargs and 'order by ' + kwargs['order'] or ''
        sql = 'select %s from %s %s %s ' % (field, table, where, order)
        # print(sql)
        try:
            # 实时刷新 self.conn.commit()
            # self.conn.commit()
            # 执行SQL语句
            self.cursor.execute(sql)
            # 使用 fetchone() 方法获取单条数据.
            data = self.cursor.fetchall()
        except Exception as e:
            # 发生错误时回滚
            self.conn.rollback()
            return str(e)
        return data
