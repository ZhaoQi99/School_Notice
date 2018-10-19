'''
Created on Oct 15, 2018

@author: QiZhao
'''
from spider import Spider


def test(dic):
    try:
        status, data = Spider(dic['url'], dic['url_main'], dic['rule'], dic['subject_CN'],
                              dic['subject_EN'], dic['coding'])
        print(status)
        print(data)
    except Exception as e:
        print(e)


def test_index():
    dic = {
        'subject_EN': 'snnu_index',
        'subject_CN': '师大主页',
        'url': 'http://www.snnu.edu.cn/tzgg.htm',
        'url_main': 'http://www.snnu.edu.cn/info/1085/',
        'rule': 'info/1085/(?P<link>\d+\.htm)" target="_blank">(?P<title>[\s\S]{5,100})（(?P<date>\d*-\d*-\d*)）',
        'coding': 'utf-8'
    }
    test(dic)


def test_css():
    dic = {
        'subject_EN': 'snnu_css',
        'subject_CN': '计科院主页',
        'url': 'http://ccs.snnu.edu.cn/tzgg.htm', 'url_main': 'http://ccs.snnu.edu.cn/',
        'rule': '<a target="_blank" href="(?P<link>[^"]*)">(?P<title>[^( </)]*)[^"]*"[^>]*>(?P<date>\d*-\d*-\d*)',
        'coding': 'utf-8'
    }
    test(dic)


def test_jwc():
    dic = {
        'subject_EN': 'snnu_jwc',
        'subject_CN': '教务处主页',
        'url': 'http://jwc.snnu.edu.cn/news_more.xhm?lm=2',
        'url_main': 'http://jwc.snnu.edu.cn/html/news_view.xhm?newsid=',
        'rule': 'newsid=(?P<link>\d*)" [^ ]* title="(?P<title>[^(">)]*)[^<]*[^(]*\((?P<date>\d*/\d*/\d*)',
        'coding': 'gbk'
    }
    test(dic)


def test_xsc():
    dic = {
        'subject_EN': 'snnu_xsc',
        'subject_CN': '学生处主页',
        'url': 'http://www.xsc.snnu.edu.cn/Announcements.asp',
        'url_main': 'http://www.xsc.snnu.edu.cn/Announcements.asp?id=144&bh=',
        'rule': 'gk3">(?P<date>\d*-\d*-\d*)[^;]*;[^;]*;[^;]*;[^;]*;bh=(?P<link>\d*)[^>]*>(?P<title>[^</]*)',
        'coding': 'gbk'
    }
    test(dic)


def test_lib():
    dic = {
        'subject_EN': 'snnu_lib',
        'subject_CN': '图书馆主页',
        'url': 'http://www.lib.snnu.edu.cn/action.do?webid=w-d-bggg-l',
        'url_main':  'http://www.lib.snnu.edu.cn/action.do?webid=w-l-showmsg&gtype=a&pid=',
        'rule':  'pid=(?P<link>\d*)[\s\S]{20,57}>(?P<title>[^<]*)</[af][\S\s]{18,70}(?P<date>\d{4}-\d*-\d*)',
        'coding': 'utf-8'
    }
    test(dic)


def test_clxy():
    dic = {
        'subject_EN': 'snnu_clxy',
        'subject_CN': '材料院',
        'url': 'http://clxy.snnu.edu.cn/home/list/?bh=008',
        'url_main':  'http://clxy.snnu.edu.cn/Home/show/',
        'rule': 'show[/](?P<link>\d*)"[\s\S]{1,}?"(?P<title>[\s\S]{1,}?)"[^<]{1,}?</a>[\S\s]{1,200}<td align="center">[^\d]*(?P<date>\d*-\d*-\d*)',
        'coding': 'utf-8'
    }
    test(dic)


def main():
    test_index()
    test_css()
    test_jwc()
    test_xsc()
    test_lib()
    test_clxy()

if __name__ == '__main__':
    main()
