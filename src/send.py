# encoding='utf-8' 
import twilio
'''
Created on Mar 7, 2018

@author: QiZhao
@license: GNU GPLv3
@version: 0.2.0
'''
from twilio.rest import Client 
from email.mime.text import MIMEText
import smtplib
from tool import Log_Write
import configs

def Send_sms(send_number, msg):
    '''
    向手机号码为send_number的人发送内容为msg的短信
    支持多个手机号码的发送
    Args:
        send_number: 短信接收者的手机号码
        msg: 要发送的文本内容，类型为字符串
        
    Returns:
        经过处理的含短信接收者手机号码以及发送结果的日志信息，类型为字符串
        例如:
        '+8615012345678 短信已经发送\n'
        '+8615012345678 短信发送失败，请检查你的账号是否有效或网络是否良好!\n'
        
    send_number应已经在twilio上验证过
    msg中不能包含敏感词，否则短信会被运营商拦截
    '''
    
    # 从twilio上获取
    account_sid = configs.ACCOUNT_ID
    auth_token = configs.AUTH_TOKEN
    twilio_number = configs.TWILIO_NUMBER

    log_send_sms = ''
    client = Client(account_sid, auth_token)
    send_number_list = send_number.split(',')   # 多个号码的发送
    for send_number in send_number_list: 
        try:
            # 修复由于最后一个元素的结尾多出一个换行导致的日志记录混乱的问题
            if(send_number==send_number_list[-1]):
                send_number=send_number[0:-1]
#                print(send_number)
            client.messages.create(to=send_number, from_=twilio_number, body=msg)
#             print('短信已经发送！')
            log_send_sms += send_number + ' ' + '短信已经发送!  ' 
        except ConnectionError:
#             print('发送失败，请检查你的账号是否有效或网络是否良好！')
            log_send_sms += send_number + ' ' + '短信发送失败，请检查你的账号是否有效或网络是否良好!'
        except twilio.base.exceptions.TwilioRestException:
            log_send_sms+=send_number+' '+'短信发送失败,手机号码尚未经过验证，请联系作者进行验证!'
    return log_send_sms
    
def Send_email(txt, to_addr_str, subject):
    '''
    向to_addr_str中的邮箱地址发送主题为subject，正文部分为txt的邮件
    支持多人同时发送
    Args:
        txt: 要发送的邮件的正文部分，类型为字符串
        to_add_str: 收件人的邮箱地址，多个邮箱地址之间应以','分割，类型为字符串
            例如：'example@qq.com','example1@qq.com,example2@qq.com'
        subject: 邮件主题
        
    Returns:
        log_send_email: 经过处理的含收件人邮箱地址以及发送结果的日志信息，类型为字符串
            例如：'example@qq.com 邮件发送成功！\n'
            'example@qq.com 邮件发送失败，请检查你的账号是否有效或网络是否良好！\n'
            'example1@qq.com,example2@qq.com 邮件发送成功！\n'
    '''
    from_addr = configs.FROM_ADDR  # 发件人的邮件地址
    password = configs.PASSWORD # 非QQ密码，应为SMTP服务授权码，可在QQ邮件设置的账户选项中获取
    
    msg = MIMEText(txt)
    msg['Subject'] = subject  # 邮件主题
    msg['From'] = configs.FROM_ADDR  # 使用QQ邮箱发送时，此处必须与from_addr一致
                                    # 使用其他邮箱的情况尚未测试
    msg['To'] = to_addr_str
    to_addr_list = to_addr_str.split(',')  # ['example1@qq.com','example2@qq.com']
    
    smtp = smtplib.SMTP_SSL() 
    smtp.connect(configs.EMAIL_SERVER,configs.EMAIL_PORT)  # 一般端口为25,QQ邮箱端口为465
    smtp.login(from_addr, password)
    
    log_send_email = ''
    try:
        smtp.sendmail(from_addr, to_addr_list, msg.as_string())
#         print('邮件发送成功！')
        log_send_email = to_addr_str[0:-1]+' 邮件发送成功！'
    except ConnectionError:
#         print('发送失败，请检查你的账号是否有效或网络是否良好！')
        log_send_email = to_addr_str[0:-1] + ' ' + '邮件发送失败，请检查你的账号是否有效或网络是否良好！'
     
    smtp.quit()
    return log_send_email



def Send(msgs, subject, send_number,to_addr_str,flag=1):
    '''
    向手机号码为send_number的人发送通知信息
    向to_addr_str中的邮箱地址发送主题为subject的通知信息
    支持是否写入日志记录的选择               
                                    
    Args:
        msgs: 存储要发送的内容的列表，且该列表的每个元素为字典，
            列表元素中的字典必须包含三个键值对,且key必须为'title','link','date'，
            例如：[{'title':'关于xxx的通知','date':'2017-03-10','link':'http://xxxx.com'},
        {'title':'关于xxx的通知','date':'2017-03-10','link':'http://xxxx.com'}]
        subject: 要发送的邮件主题
        send_number: 短信接收者的手机号码
        to_addr_str: 收件人的邮箱地址，多个邮箱地址之间应以','分割，类型为字符串
            例如：'example@qq.com','example1@qq.com,example2@qq.com'
        flag: 一个可选变量，用来决定是否在发送日志中记录此次发送信息，默认为1(记录)
    '''
    temp = ''
    log_send = []
#     log_send=['test\n']    # Only for test

    for msg in msgs:
        temp = subject + '有新通知了,快去看看吧' + '\n' + '标题:' + msg['title']\
         + '\n' + '时间:' + msg['date'] + '\n' + '查看:' + msg['link']
        log_send_sms=[]
        log_send_email=[]
        log_send_sms.append(Send_sms(send_number, temp))
        log_send_email.append(Send_email(temp, to_addr_str, subject + '更新通知'))
  
        log_send.append(log_send_sms)
        log_send.append(log_send_email)
    if(flag == 1):
        Log_Write('Send', log_send)
