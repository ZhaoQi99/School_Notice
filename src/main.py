# encoding='utf-8'
'''
@author: QiZhao
@contact: zhaoqi99@outlook.com
@since: 2018-05-08
@license: GNU GPLv3
@version: 0.3.0
@LastModifiedBy: QiZhao
@LastModifiedDate: 2018-10-27
'''
import configs
from spider import Spider
import time
from tool import Mkdir, Mkfile, Log_Write
import os
from traceback import format_exc
import send
def Init():
    '''首次使用时，程序初始化'''
    Mkdir('Log')
    Mkdir('Data')
    Mkfile('Log/' + 'Exception_log.log')
        
    File_Path = os.getcwd() + '\\Data\\user.md'
    if not os.path.exists(File_Path):  # 不存在user.md文件
        Mkfile('Data/' + 'user.md')

        f_obj = open(File_Path, 'w')
        print('请输入短信接受者的电话号码(加国际区号,多个电话号码之间以,分隔),如:+8615012345678')
        send_number = input()
        print('请输入收件人的邮件地址(多个邮件地址之间以,分隔),如:example.com')
        to_addr_str = input()
        time_interval = input('请输入检查更新的时间间隔(单位:秒):')
        f_obj.write(send_number)
        f_obj.write('\n')
        f_obj.write(to_addr_str)
        f_obj.write('\n')
        f_obj.write(time_interval)
        f_obj.close()


def Show_right():
    '''显示程序版权声明'''
    print(configs.SCHOOL_NAME + '校园通知自动提醒' + ' ' + configs.VERSION)
    print('版权所有 (c) ' + configs.AUTHOR_NAME + '  保留所有权利。 ')
    print('本程序仅供学习和研究使用,不得用于任何商业用途.')
    print('如您在使用中遇到任何问题,可联系作者邮箱: ' + configs.AUTHOR_EMAIL)
    print('请按回车键继续......', end='')
    print('---------------------------------------------------')
    print(configs.SCHOOL_NAME + '校园通知自动提醒程序启动!')


def main():
    if configs.SHOW_RIGHT:
        Show_right()
    Init()
    f_obj = open('Data' + '/user.md')
    send_number = f_obj.readline()
    to_addr_str = f_obj.readline()
    time_interval = (int)(f_obj.readline())
    f_obj.close()

    while(True):
        for dic in configs.SPIDER_CONFIG:
            try:
                status, new_data = Spider(dic, configs.LOG_ENABLED)
                if status >= 1:
                    send.Send(new_data, dic['department_CN'], 
                              send_number, to_addr_str, dic['type'],configs.LOG_ENABLED)
            except Exception as e:
                print('Exception: ', e)
                Error_log = '异常信息如下:\n' + format_exc() + '-' * 70 + '\n'
                Log_Write('Exception', Error_log, 0)
            finally:
                print('-' * 51)
        time.sleep(time_interval)


if __name__ == '__main__':
    main()
