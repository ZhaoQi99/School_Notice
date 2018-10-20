# encoding='utf-8'
'''
Created on Mar 7, 2018

@author: QiZhao
@license: GNU GPLv3
@version: 0.2.0
'''
import urllib.request
import re
import tool
import sqlhelper


def Spider_data(url, rule, coding='utf-8'):
    '''
    爬取url的源码，并从中按照rule提供的正则表达式规则提取有用分组
    Args:
        url: 要爬取的页面的统一资源定位符
        rule: 表示正则表达式规则的字符串,限制为三个分组

    Returns:
        data_use: 存储经正则表达式匹配后的有用信息的列表，且该列表每个元素为字典
        例如：[{'title':'关于xxx的通知','date':'2017-03-10','link':'id=5'},
        {'title':'关于xxx的通知','date':'2017-03-10','link':'id=5'}]
    '''

    response = urllib.request.urlopen(url)
    data = response.read().decode(coding)
    pattern = re.compile(rule, re.S)
    data_use = []
    it = pattern.finditer(data)
    for i in it:
        data_use.append(i.groupdict())
    return data_use


def Data_processing(subject_EN, data, url_main):
    '''
    读取数据文件,并将新抓取的通知信息中的链接部分处理为长链接,
    然后以通知链接为参照,与数据文件中的数据进行对比，并将新通知的以附加写的形式写入数据文件,
    返回检查更新的状态码与处理后的数据

    Args:
        subject_EN: 生成的数据文件的文件名
        data: 存储通知主要内容的列表，且该列表每个元素为字典
        例如：[{'title':'关于xxx的通知','date':'2017-03-10','link':'id=5'},
        {'title':'关于xxx的通知','date':'2017-03-10','link':'id=5'}]
        url_main: 单条通知的url的公共部分
    Returns:
        status: 检查更新的状态码,无新通知时为0,首次抓取为-1,有新通知时通知条数
        new_data: 存储经处理后的通知内容的列表,且该列表每个元素为字典
            例如：[{'title':'关于xxx的通知','date':'2017-03-10','link':'http://xxxx.com'},
        {'title':'关于xxx的通知','date':'2017-03-10','link':'http://xxxx.com‘}]
    '''

    # 处理为长网址
    for item_dict in data:
        item_dict['link'] = url_main + item_dict['link']

    table_name = subject_EN
    if sqlhelper.ExistTable('database', table_name) == False:
        sql = 'CREATE TABLE' + ' ' + table_name + \
            '(link Text PRIMARY KEY,title Text,datee Text)'
        sqlhelper.Execute('database', sql)

    # 收集所有的link信息
    sql = 'select * from' + ' ' + table_name
    all_link = sqlhelper.FetchRow('database', sql, 0)

    # 生成新数据
    status = 0  # 是否有新通知的标志
    new_data = []
    for item in data:
        if item['link'] not in all_link:
            item['date'] = item['date'].replace('/', '-')  # 将日期统一转换为yy-mm-dd格式
            status += 1
            new_data.append(item)
    if len(all_link) == 0:  # 首次抓取
        status = -1

    # 将新抓取到的通知信息写入数据文件
    # f_temp = open(file, 'ab')
    # for item in new_data:
    #     f_temp.write(item['title'].encode('utf-8'))
    #     f_temp.write(" ".encode('utf-8') + item['date'].encode('utf-8'))
    #     f_temp.write(" ".encode('utf-8') + item['link'].encode('utf-8'))
    #     f_temp.write("\n".encode('utf-8'))
    # f_temp.close()

    # Todo: 解决频繁开启关闭数据库的问题
    # Todo: 异常处理
    for item in new_data:
        sql = "insert into" + " " + table_name + "(link,title,datee) values ('%s','%s','%s')" % (
            item['link'], item['title'], item['date'])
#         print(sql)
        sqlhelper.Execute('database', sql)
    return status, new_data


def Log_generate(status, data, subject_CN):
    '''
    依据检查更新的结果，生成不同的日志内容，并返回日志内容

    Args:
        data:存储通知提醒主要内容的列表，且该列表每个元素为字典
        例如：[{'title':'关于xxx的通知','date':'2017-03-10','link':'http://xxxx.com'},
        {'title':'关于xxx的通知','date':'2017-03-10','link':'http://xxxx.com'}]
        subject_CN: 抓取的网站类型
        status: 检查更新的状态码

    Returns:
        log_txt: 日志的主要内容，类型为字符串或每个元素均为列表的列表，且元素列表的元素均为字符串。
        例如:'首次抓取师师大主页！\n','师大主页暂无新通知！\n'
        [['关于xxx的通知','2017-03-10','http://xxxx.com'],['关于xxx的通知','2017-03-10','http://xxxx.com']]   
    '''
    if status == -1:
        log_txt = '首次抓取' + subject_CN + '!\n'
    elif status == 0:
        log_txt = subject_CN + "暂无新通知!" + '\n'
    else:
        log_txt = []
        for dic in data:
            temp = []
            temp.append(dic['title'])
            temp.append(dic['link'])
            temp.append(dic['date'])
            log_txt.append(temp)
    return log_txt


def Spider(url, url_main, rule, subject_CN, subject_EN, coding, flag=True):
    '''
    爬取url的源码，并从中按照rule提供的正则表达式规则提取有用信息，并对数据进行处理，
    生成通知提醒的内容，在subject_EN+'_log.md'文件中记录日志，
    返回检查更新的状态码，以及通知提醒的内容
    若无新通知，则通知提醒的内容为空
    支持选择是否将此次检查更新的结果写入日志

    Args:
        url: 要爬取的页面的统一资源定位符
        url_main: 单条通知的url的公共部分
        rule: 表示正则表达式规则的字符串,限制为三个分组，用于从源码中提取信息
        subject_CN: 抓取的网站类型
        subject_EN: 生成的日志文件的文件名前缀，数据文件的文件名，以及输出时显示在单条日志信息前的对日志类型的描述
        flag: 一个可选变量，用来决定是否在日志中记录此次检查的结果，默认为True(记录)

    Returns:
        status: 检查更新的状态码
        new_data: 存取通知提醒的主要内容，类型每个元素均为字典的列表
            例如：[{'title':'关于xxx的通知','date':'2017-03-10','link':'http://xxxx.com'},
        {'title':'关于xxx的通知','date':'2017-03-10','link':'http://xxxx.com'}]
    '''
    data_use = Spider_data(url, rule, coding)
    status, new_data = Data_processing(subject_EN, data_use, url_main)

    log_txt = Log_generate(status, new_data, subject_CN)
    if flag == True:
        tool.Log_Write(subject_EN, log_txt)
    return status, new_data
