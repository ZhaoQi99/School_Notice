# encoding='utf-8' 
'''
Created on Mar 8, 2018

@author: QiZhao
@license: GNU GPLv3
@version: 0.1.0
'''
import spider
import time
from tool import Mkdir, Mkfile
import os

def Init():
    '''首次使用时，程序初始化'''
    Mkdir('Data')
    Mkdir('Log')
    
    File_Path=os.getcwd()+'\\Data\\user.md'
    if not os.path.exists(File_Path):   # 不存在user.md文件
        Mkfile('Data\\' + 'user.md')
        
        f_obj=open(File_Path,'w')
        print('请输入短信接受者的电话号码(加国际区号),如:+8615012345678')
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

def main():
    print('学校通知自动提醒程序启动!')
    Init()
    
    f_obj=open('Data'+'\\user.md')
    send_number=f_obj.readline()
    to_addr_str=f_obj.readline()
    time_interval=(int)(f_obj.readline())
    f_obj.close()
    
    while(True):
        spider.Spider_snnu_index(send_number, to_addr_str)
        spider.Spider_snnu_css(send_number, to_addr_str)
        spider.Spider_snnu_jwc(send_number, to_addr_str)
        spider.Spider_snnu_xsc(send_number, to_addr_str)
        spider.Spider_snnu_lib(send_number, to_addr_str)
        print('---------------------------------------------------')
        time.sleep(time_interval)

if __name__ == '__main__':
    main()
