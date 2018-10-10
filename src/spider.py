# encoding='utf-8' 
'''
Created on Mar 7, 2018

@author: QiZhao
@license: GNU GPLv3
@version: 0.1.7
'''
import urllib.request
import re
import tool

def Spider_data(url, rule, coding='utf-8'):
    '''
    爬取url的源码，并从中按照rule提供的正则表达式规则提取有用信息
    Args:
        url: 要爬取的页面的统一资源定位符
        rule: 表示正则表达式规则的字符串,限制为三个分组
        
    Returns:
        data_use: 存储经正则表达式匹配后的有用信息的列表，且该列表每个元素为元组
        例如：[('关于xxx的通知','2017-03-10','id=5'),('关于xxx的通知','2017-03-10','id=3')]
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
    将数据文件读取为字符串形式，并将从新抓取的源码中提取的信息加工为与数据文件一致的格式，
    并写入数据文件，再次将数据文件读取为字符串形式，返回两个字符串
    
    Args:
        subject_EN: 生成的数据文件的文件名
        data: 存储通知提醒主要内容的列表，且该列表每个元素为元组
        例如：[('关于xxx的通知','2017-03-10','id=5'),('关于xxx的通知','2017-03-10','id=3')]
        url_main: 单条通知的url的公共部分
    Returns:
        txt: 新文本字符串
        txt_before: 旧文本字符串
    '''
    
    # 处理为长网址
    for item_dict in data:
        item_dict['link']=url_main+item_dict['link']
    
    file = 'Data\\' + subject_EN + '.md'
    tool.Mkfile(file)  # 初次抓取时新建数据文件
    f_before = open(file, 'rb')  # 读取数据文件中的通知信息
    txt_before = f_before.read().decode('utf-8')
    f_before.close()
        
    # 收集所有的link信息
    all_link=[]
    split_rule='(?P<title>[^ ]*) (?P<date>\d*-\d*-\d*) (?P<link>[^\n]*)\n'
    pattern = re.compile(split_rule, re.S)
    data_before = pattern.finditer( txt_before)
    for item in data_before:
        dic=item.groupdict()
        all_link.append(dic['link'])

    # 生成新数据
    status=0 # 是否有新通知的标志
    new_data=[]
    for item in data:
        if item['link'] not in all_link:
            item['date']=item['date'].replace('/','-')# 将日期统一转换为yy-mm-dd格式
            status+=1
            new_data.append(item)
    if len(txt_before)==0:
        status=-1
            
    # 将新抓取到的通知信息写入数据文件
    f_temp = open(file, 'ab')  
    for item in new_data:
        f_temp.write(item['title'].encode('utf-8'))
        f_temp.write(" ".encode('utf-8') + item['date'].encode('utf-8'))
        f_temp.write(" ".encode('utf-8') + item['link'].encode('utf-8'))
        f_temp.write("\n".encode('utf-8'))
    f_temp.close()
    return status,new_data

def Log_generate(status,data,subject_CN):
    '''
    依据两个字符串对比的结果，生成不同的日志内容，并返回日志内容以及通知提醒的内容
    若两个字符串不同，则依据split_rule对字符串进行分组，并生成通知提醒的内容
    若两个字符串相同，则通知提醒的内容为空
    
    Args:
        txt: 新文本字符串
        txt_before: 旧文本字符串
        split_rule: 表示正则表达式规则的字符串,限制为三个分组
        subject: 抓取的网站类型
        status: 两个文本字符串对比的结果
        
    Returns:
        log_txt: 日志的主要内容，类型为字符串或每个元素均为列表的列表，且元素列表的元素均为字符串。
        例如:'首次抓取师师大主页！\n','师大主页暂无新通知！\n'
        [['关于xxx的通知','2017-03-10','http://xxxx.com'],['关于xxx的通知','2017-03-10','http://xxxx.com']]
        new_msgs: 
            存取通知提醒的主要内容，类型每个元素均为列表的列表，且元素列表的元素均为字符串。
            例如：[['关于xxx的通知','2017-03-10','http://xxxx.com'],
            ['关于xxx的通知','2017-03-10','http://xxxx.com']]
        
    '''
    if status == -1:
        log_txt = '首次抓取' + subject_CN + '!\n'
    elif status == 0:
        log_txt = subject_CN + "暂无新通知!" + '\n'
    else:
        log_txt = []
        for dic in data:
            temp=[]
            temp.append(dic['title'])
            temp.append(dic['link'])
            temp.append(dic['date'])
            log_txt.append(temp)
    return log_txt

def Spider(url, url_main, rule, subject_CN, subject_EN,coding,flag=1):
    '''
    爬取url的源码，并从中按照rule提供的正则表达式规则提取有用信息，并对数据进行加工，
    比教新旧字符串文本，并按split_rule分组，生成通知提醒的内容，在subject_EN+'_log.md'文件中记录日志，
    返回检查更新通知的结果，以及通知提醒的内容
    若无新通知，则通知提醒的内容为空
    支持选择是否将此次检查更新的结果写入日志
    
    Args:
        url: 要爬取的页面的统一资源定位符
        url_main: 单条通知的url的公共部分
        rule: 表示正则表达式规则的字符串,限制为三个分组，用于从源码中提取信息
        split_rule: 表示正则表达式规则的字符串,限制为三个分组，用于将字符串分组
        subject: 抓取的网站类型
        subject_EN: 生成的日志文件的文件名前缀，数据文件的文件名，以及输出时显示在单条日志信息前的对日志类型的描述
        flag: 一个可选变量，用来决定是否在日志中记录此次检查的结果，默认为1(记录)
        
    Returns:
        status: 两个文本字符串对比的结果，即检查有无新通知的结果
        new_msgs: 存取通知提醒的主要内容，类型每个元素均为列表的列表，且元素列表的元素均为字符串。
            例如：[['关于xxx的通知','2017-03-10','http://xxxx.com'],['关于xxx的通知','2017-03-10','http://xxxx.com']]
    '''
    data_use = Spider_data(url, rule,coding)
    status,new_data= Data_processing(subject_EN, data_use, url_main)
    
    log_txt = Log_generate(status,new_data,subject_CN)
    if flag == 1:
        tool.Log_Write(subject_EN, log_txt)
    return status,new_data

        

    
