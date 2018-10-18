# encoding='utf-8'
'''
Created on Mar 8, 2018

@author: QiZhao
@license: GNU GPLv3
@version: 0.2.0
'''
import time
import os


def time_text():
    '''
    Returns:
        返回当前系统时间，例如：
        2018-03-09 21:35:34
    '''
    return time.strftime("%Y-%m-%d %X", time.localtime())


def Log_Write(subject, log_txt, flag=1):
    '''
    对log_txt进行处理，生成带有时间信息的日志信息，并返回或输出(可选)。
    在Log目录下的subject+'log.md'文件写入日志信息。

    Args:
        subject: 生成的日志文件的文件名前缀，以及输出时显示在单条日志信息前的对日志类型的描述
        log_txt: 不带时间信息的日志内容，类型可以为字符串，每个元素均为列表(该列表中每个元素要求为字符串)的列表
        flag: 一个可选变量，决定是否在输出设备输出日志信息，默认为1(输出)

    Returns:
        返回由处理后的单条或多条日志信息组成的列表。

    '''

    file_name = 'Log/' + subject + '_log.log'
    file = open(file_name, 'a', encoding='utf-8')  # 以“附加写”的方式打开文件
    log_show = ''
    log_return = []
    if(type(log_txt) == str):  # 处理第一次爬取或无新通知时的日志的写入
        temp = time_text() + ' ' + log_txt
        log_show = subject + ':' + temp
        log_return.append(temp)
        file.write(temp)
    elif type(log_txt) == list:  # 处理发送更新提醒后日志的写入,处理有更新信息时的日志的写入
        for log in log_txt:
            temp = time_text() + ' ' + ' '.join(log) + '\n'
            file.write(temp)
            log_return.append(temp)
            log_show += subject + ':' + temp
    file.close()

    if(flag == 1):
        print(log_show, end='')
    return log_return


def Mkdir(dir_name, flag=1):
    '''
    获取到当前文件所在的目录，并检查是否有'dir_name'文件夹，
    如果不存在则自动新建'dir_name'文件夹

    Args:
        dir_name: 文件夹名，类型为字符串
        flag: 一个可选变量，决定是否在输出设备输出日志信息，默认为1(输出)
    '''

    File_Path = os.getcwd() + '/' + dir_name + '/'
    if not os.path.exists(File_Path):
        os.makedirs(File_Path)
        Log_Write('新建文件夹', File_Path + '\n', flag)


def Mkfile(fname, flag=1):
    '''
    检查当前路径下是否存在'fname'文件，
    如果不存在则自动新建'fname'文件

    Args:
        fname: 文件名，类型为字符串
        flag: 一个可选变量，决定是否在输出设备输出日志信息，默认为1(输出)
    '''
    fname = os.getcwd() + '/' + fname
    if not os.path.exists(fname):
        fobj = open(fname, 'w')
        fobj.close()
        Log_Write('新建文件', fname + '\n', flag)
