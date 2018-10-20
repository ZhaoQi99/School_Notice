'''
Created on Oct 19, 2018

@author: QiZhao
'''
import pypyodbc
import os


def ExistTable(data_base, table_name):
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
