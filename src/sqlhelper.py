'''
Created on Oct 19, 2018
@author: QiZhao
'''
import pypyodbc
import os


def ExistTable(data_base, table_name):
    '''
    判断数据库中是否存在某张表,返回True或Flase

    Args:
        data_base: 数据库文件的文件名
        table_name: 表名
    Returns:
        返回True或Flase
    '''

    path = os.getcwd() + "\\" + data_base + ".mdb"
    try:
        connection = pypyodbc.win_connect_mdb(path)
        cursor = connection.cursor()
        res = cursor.tables()
        tables = []
        for i in res:
            tables.append(i[2])
        if table_name in tables:
            return True
        else:
            return False
    except Exception as e:
        connection.rollback()
        connection.close()
        raise e


def Execute(data_base, sql):
    '''
    执行一条SQL语句,返回SQL语句执行后影响的行数

    Args:
        data_base: 数据库文件的文件名
        sql: SQL语句
    Returns:
        res: SQL语句执行后影响的行数
    '''

    path = os.getcwd() + "\\" + data_base + ".mdb"
    try:
        connection = pypyodbc.win_connect_mdb(path)
        cursor = connection.cursor()
        res = cursor.execute(sql)
        connection.commit()
        connection.close()
        return res
    except Exception as e:
        connection.rollback()
        connection.close()
        raise e


def CreateDatabase(data_base):
    '''
    判断当前路径是否存在数据库文件
    如果不存在,则尝试创建数据库文件,
    返回创建的结果

    Args:
        data_base: 数据库文件的文件名
    Returns:
        返回True或Flase
    '''
    path = os.getcwd() + "\\" + data_base + ".mdb"
    try:
        if not os.path.exists(path):
            connection = pypyodbc.win_create_mdb(path)
            connection.close()
            return True
        return False
    except Exception as e:
        raise e


def Fetchall(data_base, sql):
    '''
    执行一条SQL语句,返回查询结果的所有行
    Args:
        data_base: 数据库文件的文件名
        sql: SQL语句
    Returns:
        res: 一个list,包含查询的结果,
        元素为元组,代表一行信息
    '''
    path = os.getcwd() + "\\" + data_base + ".mdb"
    try:
        connection = pypyodbc.win_connect_mdb(path)
        cursor = connection.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
        connection.close()
        return res
    except Exception as e:
        connection.rollback()
        connection.close()
        raise e


def FetchRow(data_base, sql, column):
    '''
    执行一条sql语句,并从查询结果中筛选指定的某一列的所有内容

    Args:
        data_base: 数据库文件的文件名
        sql: SQL语句
        column: 第几列,从0开始
    Returns:
        res: 一个list,包含指定列的所有结果
    '''
    path = os.getcwd() + "\\" + data_base + ".mdb"
    try:
        connection = pypyodbc.win_connect_mdb(path)
        cursor = connection.cursor()
        cursor.execute(sql)
        row_count = cursor._NumOfCols()
        if column >= row_count:
            raise IndexError
        res = cursor.fetchall()
        ret = []
        for col in res:
            ret.append(col[column])
        connection.close()
        return ret
    except Exception as e:
        connection.rollback()
        connection.close()
        raise e
