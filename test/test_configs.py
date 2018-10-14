'''
Created on Oct 8, 2018

@author: QiZhao
'''
# show config
SCHOOL_NAME = '陕师大'
VERSION = 'v0.2.0'
AUTHOR_NAME = 'QiZhao'
AUTHOR_EMAIL = 'zhaoqi99@outlook.com'

# twillo config
ACCOUNT_ID = ''
AUTH_TOKEN = ''
TWILIO_NUMBER = ''

# send_email config
FROM_ADDR = ""
PASSWORD = ""
EMAIL_PORT = 0
EMAIL_SERVER = ''

# spider config
SPIDER_CONFIG = [
{
    'subject_EN':'snnu_index', 
    'subject_CN':'师大主页', 
    'url': 'http://www.snnu.edu.cn/tzgg.htm', 
    'url_main' : 'http://www.snnu.edu.cn/info/1085/',
    'rule' : 'info/1085/(?P<link>\d+\.htm)" target="_blank">(?P<title>[\s\S]{5,100})（(?P<date>\d*-\d*-\d*)）', 
    'coding':'utf-8'
},
{
    'subject_EN':'snnu_css', 
    'subject_CN':'计科院主页', 
    'url': 'http://ccs.snnu.edu.cn/tzgg.htm', 'url_main' : 'http://ccs.snnu.edu.cn/',
    'rule' : '<a target="_blank" href="(?P<link>[^"]*)">(?P<title>[^( </)]*)[^"]*"[^>]*>(?P<date>\d*-\d*-\d*)', 
    'coding':'utf-8'
},
{
    'subject_EN':'snnu_jwc', 
    'subject_CN':'教务处主页', 
    'url': 'http://jwc.snnu.edu.cn/news_more.xhm?lm=2', 
    'url_main' : 'http://jwc.snnu.edu.cn/html/news_view.xhm?newsid=',
    'rule' : 'newsid=(?P<link>\d*)" [^ ]* title="(?P<title>[^(">)]*)[^<]*[^(]*\((?P<date>\d*/\d*/\d*)', 
    'coding':'gbk'
},
{
    'subject_EN':'snnu_xsc', 
    'subject_CN':'学生处主页', 
    'url': 'http://www.xsc.snnu.edu.cn/Announcements.asp', 
    'url_main' : 'http://www.xsc.snnu.edu.cn/Announcements.asp?id=144&bh=',
    'rule' : 'gk3">(?P<date>\d*-\d*-\d*)[^;]*;[^;]*;[^;]*;[^;]*;bh=(?P<link>\d*)[^>]*>(?P<title>[^</]*)', 
    'coding':'gbk'
},
{
    'subject_EN':'snnu_lib', 
    'subject_CN':'图书馆主页', 
    'url': 'http://www.lib.snnu.edu.cn/action.do?webid=w-d-bggg-l', 
    'url_main' :  'http://www.lib.snnu.edu.cn/action.do?webid=w-l-showmsg&gtype=a&pid=',
    'rule' :  'pid=(?P<link>\d*)[\s\S]{20,57}>(?P<title>[^<]*)</[af][\S\s]{18,70}(?P<date>\d{4}-\d*-\d*)', 
    'coding':'utf-8'
}
]
