# encoding='utf-8' 
'''
Created on Mar 8, 2018

@author: QiZhao
@license: GNU GPLv3
@version: 0.1.5
'''
import spider
import time
from tool import Mkdir, Mkfile,Log_Write
import os
from traceback import format_exc

def Init():
    '''首次使用时，程序初始化'''
    Mkdir('Log')
    Mkdir('Data')
    Mkfile('Log\\' + 'Exception_log.log')
    
    File_Path=os.getcwd()+'\\Data\\user.md'
    if not os.path.exists(File_Path):   # 不存在user.md文件
        Mkfile('Data\\' + 'user.md')
        
        f_obj=open(File_Path,'w')
        print('请输入短信接受者的电话号码(加国际区号,多个电话号码之间以,分隔),如:+8615012345678')
        send_number=input()
        print('请输入收件人的邮件地址(多个邮件地址之间以,分隔),如:example.com')
        to_addr_str=input()
        time_interval=input('请输入检查更新的时间间隔(单位:秒):')
        f_obj.write(send_number)
        f_obj.write('\n')
        f_obj.write(to_addr_str)
        f_obj.write('\n')
        f_obj.write(time_interval)        
        f_obj.close()

def Show_right():
    '''显示程序版权声明'''
    print('陕师大校园通知自动提醒'+' '+'V0.1.5')
    print('版权所有 (c) QiZhao  保留所有权利。 ')
    print('本程序仅供学习和研究使用,不得用于任何商业用途.')
    print('如您在使用中遇到任何问题,可联系作者邮箱: zhaoqi99@outlook.com')
    print('请按回车键继续......',end='')
    input()
    print('---------------------------------------------------')
    print('陕师大校园通知自动提醒程序启动!')
    
def main():
    Show_right()
    Init()
    f_obj=open('Data'+'\\user.md')
    send_number=f_obj.readline()
    to_addr_str=f_obj.readline()
    time_interval=(int)(f_obj.readline())
    f_obj.close()
    
    while(True):
        try:
            spider.Spider_snnu_index(send_number, to_addr_str)
            spider.Spider_snnu_css(send_number, to_addr_str)
            spider.Spider_snnu_xsc(send_number, to_addr_str)
            spider.Spider_snnu_lib(send_number, to_addr_str)
            spider.Spider_snnu_jwc(send_number, to_addr_str)        
        except Exception as e:
            print('Exception: ', e)
            Error_log='异常信息如下:\n'+format_exc()+'-'*70+'\n'
            Log_Write('Exception', Error_log, 0)
#             print_exc(file=open('Log\\'+'Exception_log.log','a'))
        finally:
            print('-'*51)
            time.sleep(time_interval)

if __name__ == '__main__':
    main()
