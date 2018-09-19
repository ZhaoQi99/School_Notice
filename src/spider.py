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
from send import Send


def Spider_data(url, rule):
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
    
    find1 = url.find('jwc', 7, 15)
    find2 = url.find('xsc', 7, 20)

    if find1 == -1 & find2 == -1:
        Coding = 'utf-8'
    else:
        # 教务处网页源码编码格式为为gbk
        # 学生处网页源码编码格式为gb2312
        Coding = 'gbk'

    data = response.read().decode(Coding)
    pattern = re.compile(rule, re.S)
    data_use = re.findall(pattern, data)
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
    
    file = 'Data\\' + subject_EN + '.md'
    
    if(subject_EN == 'snnu_xsc'):  # 将数据的顺序调整为时间、标题、链接  
        new_data = []
        for item in data:
            temp = (item[1], item[2], item[0])
            new_data.append(temp)
        data = new_data
        
    tool.Mkfile(file)    # 初次抓取时新建数据文件
    f_before = open(file, 'rb') # 读取数据文件中的通知信息
    txt_before = f_before.read().decode('utf-8')
    f_before.close()
        
    f_temp = open(file, 'wb+')  # 将新抓取到的通知信息写入数据文件
    for item in data:
        f_temp.write(item[1].encode('utf-8'))
        f_temp.write(" ".encode('utf-8') + item[2].encode('utf-8'))
        f_temp.write(" ".encode('utf-8') + url_main.encode('utf-8'))
        f_temp.write(item[0].encode('utf-8'))
        f_temp.write("\n".encode('utf-8'))
    f_temp.close()
    
    f_temp = open(file, 'rb')
    txt = f_temp.read().decode('utf-8')
    f_temp.close()
    
    return txt, txt_before


def Log_generate(txt, txt_before, split_rule, subject, status):
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
    new_msgs = []
    if status == -1:
        log_txt = '首次抓取' + subject + '!\n'
    elif status == 0:
        log_txt = subject + "暂无新通知!" + '\n'
    else:
        log_txt = new_msgs = tool.Get_new_message(txt_before, txt, split_rule)
#         print(new_msgs)
    return log_txt, new_msgs


def Spider(url, url_main, rule, split_rule, subject, subject_EN, flag=1):
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
    data_use = Spider_data(url, rule)
    txt, txt_before = Data_processing(subject_EN, data_use, url_main)
    
    status = tool.Compare(txt, txt_before)
    log_txt, new_msgs = Log_generate(txt, txt_before, split_rule, subject, status)
    
    if flag == 1:
        tool.Log_Write(subject_EN, log_txt)

    return status, new_msgs

        
def Spider_snnu_index(send_number,to_addr_str,flag=1):
    '''
    爬取校园主页通知信息,若有通知更新，向手机号码为send_number的接收者
    发送短信提醒，向邮箱地址为to_addr_str的收件人发送邮件提醒
    Args:
        send_number: 短信接收者的手机号码
        to_add_sttr: 收件人的邮箱地址，多个邮箱地址之间应以','分割，类型为字符串
            例如：'example@qq.com','example1@qq.com,example2@qq.com'
        flag: 可选变量，决定是否将此次检查结果记录在日志中，默认为1（记录）
    '''
    subject_EN = 'snnu_index'
    subject = '师大主页'
    url = 'http://www.snnu.edu.cn/tzgg.htm'
    url_main = 'http://www.snnu.edu.cn/info/1085/'
    rule = 'info/1085/(\d+\.htm)" target="_blank">([\s\S]{5,100})（(\d*-\d*-\d*)）'
    split_rule = '([^ ]*) (\d*-\d*-\d*) ([^\n]*)\n'
    
    status, new_msgs = Spider(url, url_main, rule, split_rule, subject, subject_EN,flag)
    if status == 1:
        Send(new_msgs, subject,send_number,to_addr_str)


    
def Spider_snnu_css(send_number,to_addr_str,flag=1):
    '''
    爬取计科院主页通知信息,若有通知更新，向手机号码为send_number的接收者
    发送短信提醒，向邮箱地址为to_addr_str的收件人发送邮件提醒
    Args:
        send_number: 短信接收者的手机号码
        to_add_sttr: 收件人的邮箱地址，多个邮箱地址之间应以','分割，类型为字符串
            例如：'example@qq.com','example1@qq.com,example2@qq.com'
        flag: 可选变量，决定是否将此次检查结果记录在日志中，默认为1（记录）
    '''
    subject_EN = 'snnu_css'
    subject = '计科院主页'
    url = 'http://ccs.snnu.edu.cn/tzgg.htm'
    url_main = 'http://ccs.snnu.edu.cn/'
    rule = '<a target="_blank" href="([^"]*)">([^( </)]*)[^"]*"[^>]*>(\d\d\d\d-\d\d-\d\d)'
    split_rule = '([^ ]*) (\d*-\d*-\d*) ([^\n]*)\n'
    
    status, new_msgs = Spider(url, url_main, rule, split_rule, subject, subject_EN,flag)
    if status == 1:
        Send(new_msgs, subject,send_number,to_addr_str)



def Spider_snnu_jwc(send_number,to_addr_str,flag=1):
    '''
    爬取教务处主页通知信息,若有通知更新，向手机号码为send_number的接收者
    发送短信提醒，向邮箱地址为to_addr_str的收件人发送邮件提醒
    Args:
        send_number: 短信接收者的手机号码
        to_add_sttr: 收件人的邮箱地址，多个邮箱地址之间应以','分割，类型为字符串
            例如：'example@qq.com','example1@qq.com,example2@qq.com'
        flag: 可选变量，决定是否将此次检查结果记录在日志中，默认为1（记录）
    '''
    subject_EN = 'snnu_jwc'
    subject = '教务处主页'
    url = 'http://jwc.snnu.edu.cn/news_more.xhm?lm=2'
    url_main = 'http://jwc.snnu.edu.cn/html/news_view.xhm?newsid='
    rule = 'newsid=(\d*)" [^ ]* title="([^(">)]*)[^<]*[^(]*\((\d*/\d*/\d*)'
    split_rule = '([^ ]*) (\d*/\d*/\d*) ([^\n]*)\n'
    
    status, new_msgs = Spider(url, url_main, rule, split_rule, subject, subject_EN,flag)
    if status == 1:
        Send(new_msgs, subject,send_number,to_addr_str)



def Spider_snnu_xsc(send_number,to_addr_str,flag=1):
    '''
    爬取学生处主页通知信息,若有通知更新，向手机号码为send_number的接收者
    发送短信提醒，向邮箱地址为to_addr_str的收件人发送邮件提醒
    Args:
        send_number: 短信接收者的手机号码
        to_add_sttr: 收件人的邮箱地址，多个邮箱地址之间应以','分割，类型为字符串
            例如：'example@qq.com','example1@qq.com,example2@qq.com'
        flag: 可选变量，决定是否将此次检查结果记录在日志中，默认为1（记录）
    '''
    subject_EN = 'snnu_xsc'
    subject = '学生处主页'
    url = 'http://www.xsc.snnu.edu.cn/Announcements.asp'
    url_main = 'http://www.xsc.snnu.edu.cn/Announcements.asp?id=144&bh='
    rule = 'gk3">(?P<time>\d*-\d*-\d*)[^;]*;[^;]*;[^;]*;[^;]*;bh=(?P<link>\d*)[^>]*>(?P<title>[^</]*)'
    split_rule = '([^ ]*) (\d*-\d*-\d*) ([^\n]*)\n'
    
    status, new_msgs = Spider(url, url_main, rule, split_rule, subject, subject_EN,flag)
    if status == 1:
        Send(new_msgs, subject,send_number,to_addr_str)



def Spider_snnu_lib(send_number,to_addr_str,flag=1):
    '''
    爬取图书馆主页通知信息,若有通知更新，向手机号码为send_number的接收者
    发送短信提醒，向邮箱地址为to_addr_str的收件人发送邮件提醒
    Args:
        send_number: 短信接收者的手机号码
        to_add_sttr: 收件人的邮箱地址，多个邮箱地址之间应以','分割，类型为字符串
            例如：'example@qq.com','example1@qq.com,example2@qq.com'
        flag: 可选变量，决定是否将此次检查结果记录在日志中，默认为1（记录）
    '''

    subject_EN = 'snnu_lib'
    subject = '图书馆主页'
    url = 'http://www.lib.snnu.edu.cn/action.do?webid=w-d-bggg-l'
    url_main = 'http://www.lib.snnu.edu.cn/action.do?webid=w-l-showmsg&gtype=a&pid='
    rule = 'pid=(\d*)[\s\S]{20,57}>([^<]*)</[af][\S\s]{18,70}(\d{4}-\d*-\d*)'
    split_rule = '([^ ]*) (\d*-\d*-\d*) ([^\n]*)\n'
    
    status, new_msgs = Spider(url, url_main, rule, split_rule, subject, subject_EN,flag)
    if status == 1:
        Send(new_msgs, subject,send_number,to_addr_str)

    
'''  
def test():
    file=open('Temp\\lib.md','r',encoding='utf-8')
    data=file.read()
    file.close()
    rule='pid=(\d*)[^>]*>([^<]*)[^\d]*2[^\d]*(\d*-\d*-\d*)'
    pattern = re.compile(rule, re.S)
    data_use = re.findall(pattern, data)
    print(data_use)
'''  
