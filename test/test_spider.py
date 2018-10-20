'''
Created on Oct 8, 2018

@author: QiZhao
'''
from spider import *
from traceback import format_exc
from tool import *
from test_configs import *
from configs import LOG_ENABLED


def test_re_group():
    url = 'http://www.lib.snnu.edu.cn/action.do?webid=w-d-bggg-l'
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    rule = 'pid=(?P<link>\d*)[\s\S]{20,57}>(?P<title>[^<]*)</[af][\S\s]{18,70}(?P<date>\d{4}-\d*-\d*)'
    pattern = re.compile(rule, re.S)
    m = pattern.finditer(data)
    for mm in m:
        print(mm.groupdict())


def test_Spider_data_1():
    url = 'http://www.lib.snnu.edu.cn/action.do?webid=w-d-bggg-l'
    rule = 'pid=(?P<link>\d*)[\s\S]{20,57}>(?P<title>[^<]*)</[af][\S\s]{18,70}(?P<date>\d{4}-\d*-\d*)'
    data_use = Spider_data(url, rule)
    print(data_use)


def test_Spider_data_2():
    url = 'http://www.xsc.snnu.edu.cn/Announcements.asp'
    rule = 'gk3">(?P<date>\d*-\d*-\d*)[^;]*;[^;]*;[^;]*;[^;]*;bh=(?P<link>\d*)[^>]*>(?P<title>[^</]*)'
    data_use = Spider_data(url, rule, 'gbk')
    print(data_use)


def test_dict_oper():
    url = 'http://www.xsc.snnu.edu.cn/Announcements.asp'
    rule = 'gk3">(?P<date>\d*-\d*-\d*)[^;]*;[^;]*;[^;]*;[^;]*;bh=(?P<link>\d*)[^>]*>(?P<title>[^</]*)'
    data_use = Spider_data(url, rule, 'gbk')
    for item_dict in data_use:
        item_dict['link'] += 'test'
    print(data_use)


def test_Data_processing():
    url = 'http://www.xsc.snnu.edu.cn/Announcements.asp'
    rule = 'gk3">(?P<date>\d*-\d*-\d*)[^;]*;[^;]*;[^;]*;[^;]*;bh=(?P<link>\d*)[^>]*>(?P<title>[^</]*)'
    data = Spider_data(url, rule, 'gbk')
    status, new_data = Data_processing('test', data, "Main")
    print(status)
    print(new_data)


def test_spider_config():
    print(SPIDER_CONFIG)
    for dic in SPIDER_CONFIG:
        print(dic)
        for key in dic:
            print(key + ':' + dic[key] + ',', end='')


def test_Spider():
    spider_list = SPIDER_CONFIG
    for dic in spider_list:
        try:
            status, data = Spider(dic['url'], dic['url_main'], dic['rule'], dic['subject_CN'],
                                  dic['subject_EN'], dic['coding'], LOG_ENABLED)
            print(status)
            print(data)
        except Exception as e:
            print('Exception: ', e)
            Error_log = '异常信息如下:\n' + format_exc() + '-' * 70 + '\n'
            Log_Write('Exception', Error_log, 0)
        finally:
            print('-' * 51)


def main():
    Mkdir('Log')
    Mkdir('Data')
    Mkfile('Log/' + 'Exception_log.log')
    sqlhelper.CreateDatabase('database')
    test_re_group()
    test_Spider_data_1()
    test_Spider_data_2()
    test_dict_oper()
    test_Data_processing()
    test_spider_config()
    test_Spider()


if __name__ == '__main__':
    main()
