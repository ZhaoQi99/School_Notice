import pymysql
import re


class SqlHelper():
    '''
    数据库帮助类，实现数据库的一些操作
    Args:
        target_ip: 连接目标的ip
        user_name: 数据库用户名
        pwd: 数据库用户的密码
    '''

    def __init__(self, target_ip, user_name, pwd):
        self.target_ip = target_ip
        self.user_name = user_name
        self.pwd = pwd

    def ExistTable(self, db_name, table_name):
        '''
        判断数据库中是否存在某张表,返回True或Flase
        Args:
            db_name: 数据库名称
            table_name: 表名
        Returns:
            返回True或Flase
        '''
        try:
            connection = pymysql.connect(
                host=self.target_ip, user=self.user_name, passwd=self.pwd, db=db_name)
            cursor = connection.cursor()
            sql = 'show tables;'
            cursor.execute(sql)
            tables = [cursor.fetchall()]
            table_list = re.findall('(\'.*?\')', str(tables))
            table_list = [re.sub("'", '', each) for each in table_list]
            if table_name in table_list:
                return True
            else:
                return False
        except Exception as e:
            connection.rollback()
            connection.close()
            raise e

    def Execute(self, db_name, sql):
        '''
        执行一条SQL语句,返回SQL语句执行后影响的行数
        Args:
            db_name: 数据库名称
            sql: SQL语句
        Returns:
            res: SQL语句执行后影响的行数
        '''
        try:
            connection = pymysql.connect(
                host=self.target_ip, user=self.user_name, passwd=self.pwd, db=db_name)
            cursor = connection.cursor()
            res = cursor.execute(sql)
            connection.commit()
            connection.close()
            return res
        except Exception as e:
            connection.rollback()
            connection.close()
            raise e

    def FetchAll(self, db_name, sql):
        '''
        执行一条SQL语句,返回查询结果的所有行
        Args:
            db_name: 数据库名称
            sql: SQL语句
        Returns:
            res: 一个list,包含查询的结果,元素为元组,代表一行信息
        '''
        try:
            connection = pymysql.connect(
                host=self.target_ip, user=self.user_name, passwd=self.pwd, db=db_name)
            cursor = connection.cursor()
            cursor.execute(sql)
            res = cursor.fetchall()
            connection.close()
            return res
        except Exception as e:
            connection.rollback()
            connection.close()
            raise e

    def FetchCol(self, db_name, table_name, sql, column):
        '''
        执行一条sql语句,并从查询结果中筛选指定的某一列的所有内容
        Args:
            db_name: 数据库名称
            table_name: 表名
            sql: SQL语句
            column: 第几列,从1开始
        Returns:
            res: 一个list,包含指定列的所有结果
        '''
        try:
            connection = pymysql.connect(
                host=self.target_ip, user=self.user_name, passwd=self.pwd, db=db_name)
            cursor = connection.cursor()
            temp_sql = "select count(*) from information_schema.columns where table_schema='" + \
                db_name + "' and table_name='" + table_name+"'"
            cursor.execute(temp_sql)
            tup=cursor.fetchone()
            col_count=int(tup[0])
            if column > col_count or column < 1:
                raise IndexError
            cursor.execute(sql)
            res = cursor.fetchall()
            ret = []
            column-=1
            for col in res:
                ret.append(col[column])
            connection.close()
            return ret
        except Exception as e:
            connection.rollback()
            connection.close()
            raise e