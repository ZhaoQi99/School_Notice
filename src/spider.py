# encoding='utf-8'
import configs
'''
@author: QiZhao
@contact: zhaoqi99@outlook.com
@since: 2018-05-07
@license: GNU GPLv3
@version: 0.3.0
@LastModifiedBy: QiZhao
@LastModifiedDate: 2018-12-24
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


def Data_processing(department_EN, data, url_main,message_type):
    '''
    读取数据文件,并将新抓取的通知信息中的链接部分处理为长链接,
    然后以通知链接为参照,与文件/数据库中的数据进行对比，并将新通知写入文件/数据库,
    返回检查更新的状态码与处理后的数据

    Args:
        department_EN: 生成的数据文件的文件名
        data: 存储通知主要内容的列表，且该列表每个元素为字典
        例如：[{'title':'关于xxx的通知','date':'2017-03-10','link':'id=5'},
        {'title':'关于xxx的通知','date':'2017-03-10','link':'id=5'}]
        url_main: 单条通知的url的公共部分
        message_type: 类型(通知/新闻)
    Returns:
        status: 检查更新的状态码,无新通知时为0,首次抓取为-1,有新通知时通知条数
        new_data: 存储经处理后的通知内容的列表,且该列表每个元素为字典
            例如：[{'title':'关于xxx的通知','date':'2017-03-10','link':'http://xxxx.com'},
        {'title':'关于xxx的通知','date':'2017-03-10','link':'http://xxxx.com‘}]
    '''

    # 处理为长网址
    for item_dict in data:
        item_dict['link'] = url_main + item_dict['link']
    
    # 生成新数据
    status = 0  # 是否有新通知的标志
    new_data = []
    
    if configs.SAVE_TYPE.upper()=="FILE":
        if message_type=="通知":
            file = "Data/{}_{}.md".format(department_EN,"notice")
        else:
            file="Data/{}_{}.md".format(department_EN,"news")
        tool.Mkfile(file)  # 初次抓取时新建数据文件
        f_before = open(file, 'rb')  # 读取数据文件中的通知信息
        txt_before = f_before.read().decode('utf-8')
        f_before.close()
    
        # 收集所有的link信息
        all_link = []
        split_rule = '(?P<title>[^ ]*) (?P<date>\d*-\d*-\d*) (?P<link>[^\n]*)\n'
        pattern = re.compile(split_rule, re.S)
        data_before = pattern.finditer(txt_before)
        for item in data_before:
            dic = item.groupdict()
            all_link.append(dic['link'])
            
        for item in data:
            if item['link'] not in all_link:
                item['date'] = item['date'].replace('/', '-')  # 将日期统一转换为yy-mm-dd格式
                status += 1
                new_data.append(item)
         
    elif configs.SAVE_TYPE.upper()=="MYSQL":
        helper = sqlhelper.SqlHelper(
            configs.TARGET_IP, configs.SQL_USERNAME, configs.SQL_PASSWORD)
        if helper.ExistDatabase(configs.DATABASE_NAME)==False:
            helper.CreateDatabase(configs.DATABASE_NAME)
    
        table_name = department_EN
        if helper.ExistTable(configs.DATABASE_NAME, table_name) == False:
            sql = 'CREATE TABLE' + ' ' + table_name + \
                '(id int PRIMARY KEY AUTO_INCREMENT,link Text,title Text,date Text,type Text)'
            helper.Execute(configs.DATABASE_NAME, sql)
    
        sql = "select count(*) from" + " " + table_name+" where type='"+message_type+"'"
        link_count = helper.FetchCol(configs.DATABASE_NAME, table_name,sql,1)[0]
    
        for item in data:
            temp_sql="select * from" + " " + table_name+" where link='"+item['link']+"'"
            ret=helper.FetchCol(configs.DATABASE_NAME, table_name,temp_sql, 2)
            if len(ret)==0:
                item['date'] = item['date'].replace('/', '-')  # 将日期统一转换为yy-mm-dd格式
                item['type']=message_type
                status += 1
                new_data.append(item)
            
        if link_count == 0:  # 首次抓取
            status = -1
    return status, new_data

def Save(new_data,department_EN,message_type):
    '''
    将新抓取到的通知信息写入数据文件或数据库中

    Args:
        new_data: 存储经处理后的通知内容的列表,且该列表每个元素为字典
            例如：[{'title':'关于xxx的通知','date':'2017-03-10','link':'http://xxxx.com'},
        {'title':'关于xxx的通知','date':'2017-03-10','link':'http://xxxx.com‘}]
        department_EN: 生成的数据文件的文件名
        message_type: 类型(通知/新闻)
    '''
    if configs.SAVE_TYPE.upper()=="FILE":
        if message_type=="通知":
            file = "Data/{}_{}.md".format(department_EN,"notice")
        else:
            file="Data/{}_{}.md".format(department_EN,"news")
            
        # 存储到文件中
        f_temp = open(file, 'ab')
        for item in new_data:
            f_temp.write(item['title'].encode('utf-8'))
            f_temp.write(" ".encode('utf-8') + item['date'].encode('utf-8'))
            f_temp.write(" ".encode('utf-8') + item['link'].encode('utf-8'))
            f_temp.write("\n".encode('utf-8'))
        f_temp.close()
        
    elif configs.SAVE_TYPE.upper()=="MYSQL":
        table_name=department_EN
        helper = sqlhelper.SqlHelper(
        configs.TARGET_IP, configs.SQL_USERNAME, configs.SQL_PASSWORD)
        for item in new_data:
            sql = "insert into" + " " + table_name + "(link,title,date,type) values ('%s','%s','%s','%s')" % (
                item['link'], item['title'], item['date'],item['type'])
            helper.Execute(configs.DATABASE_NAME, sql)
    return True

def Log_generate(status, data, department_CN,message_type):
    '''
    依据检查更新的结果，生成不同的日志内容，并返回日志内容

    Args:
        data:存储通知提醒主要内容的列表，且该列表每个元素为字典
        例如：[{'title':'关于xxx的通知','date':'2017-03-10','link':'http://xxxx.com'},
        {'title':'关于xxx的通知','date':'2017-03-10','link':'http://xxxx.com'}]
        department_CN: 抓取的部门名称
        status: 检查更新的状态码

    Returns:
        log_txt: 日志的主要内容，类型为字符串或每个元素均为列表的列表，且元素列表的元素均为字符串。
        例如:'首次抓取师师大主页！','师大主页暂无新通知！'
        [['关于xxx的通知','2017-03-10','http://xxxx.com'],['关于xxx的通知','2017-03-10','http://xxxx.com']]   
    '''
    if status == -1:
        log_txt = '首次抓取{}:{}！'.format(department_CN,message_type)
    elif status == 0:
        log_txt = "{}暂无新{}!".format(department_CN,message_type)
    else:
        log_txt = []
        for dic in data:
            temp = []
            temp.append(dic['title'])
            temp.append(dic['link'])
            temp.append(dic['date'])
            log_txt.append(temp)
    return log_txt


def Spider(dic, flag=True):
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
    data_use = Spider_data(dic['url'], dic['rule'], dic['coding'])
    status, new_data = Data_processing(dic['department_EN'], data_use, dic['url_main'],dic['type'])
    Save(new_data, dic['department_EN'], dic['type'])
    log_txt = Log_generate(status, new_data, dic['department_CN'],dic['type'])
    if flag == True:
        if dic['type']=="通知":
            tool.Log_Write(dic['department_EN']+"_notice", log_txt)
        else:
            tool.Log_Write(dic['department_EN']+"_news", log_txt)
            
    return status, new_data
