'''
@author: QiZhao
@contact: zhaoqi99@outlook.com
@since: 2018-05-07
@license: GNU GPLv3
@version: 0.3.0
@LastModifiedBy: QiZhao
@LastModifiedDate: 2018-10-24
'''
import twilio
from twilio.rest import Client
from email.mime.text import MIMEText
import smtplib
from tool import Log_Write
import configs
import requests
import json
import time

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
        '+8615012345678 短信已经发送'
        '+8615012345678 短信发送失败，请检查你的账号是否有效或网络是否良好!'

    send_number应已经在twilio上验证过
    msg中不能包含敏感词，否则短信会被运营商拦截
    '''

    # 从twilio上获取
    account_sid = configs.ACCOUNT_ID
    auth_token = configs.AUTH_TOKEN
    twilio_number = configs.TWILIO_NUMBER

    log_send_sms = ''
    client = Client(account_sid, auth_token)
    send_number_list = send_number.split(',')  # 多个号码的发送
    for send_number in send_number_list:
        try:
            # 修复由于最后一个元素的结尾多出一个换行导致的日志记录混乱的问题
            if(send_number == send_number_list[-1]):
                send_number = send_number[0:-1]
#                print(send_number)
            client.messages.create(
                to=send_number, from_=twilio_number, body=msg)
#             print('短信已经发送！')
            log_send_sms += send_number + ' ' + '短信已经发送!  '
        except ConnectionError:
            #             print('发送失败，请检查你的账号是否有效或网络是否良好！')
            log_send_sms += send_number + ' ' + '短信发送失败，请检查你的账号是否有效或网络是否良好!'
        except twilio.base.exceptions.TwilioRestException:
            log_send_sms += send_number + ' ' + '短信发送失败,手机号码尚未经过验证，请联系作者进行验证!'
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
            例如：'example@qq.com 邮件发送成功！'
            'example@qq.com 邮件发送失败，请检查你的账号是否有效或网络是否良好！'
            'example1@qq.com,example2@qq.com 邮件发送成功！'
    '''
    from_addr = configs.FROM_ADDR  # 发件人的邮件地址
    password = configs.PASSWORD  # 非QQ密码，应为SMTP服务授权码，可在QQ邮件设置的账户选项中获取

    msg = MIMEText(txt)
    msg['Subject'] = subject  # 邮件主题
    msg['From'] = configs.FROM_ADDR  # 使用QQ邮箱发送时，此处必须与from_addr一致
    # 使用其他邮箱的情况尚未测试
    msg['To'] = to_addr_str
    # ['example1@qq.com','example2@qq.com']
    to_addr_list = to_addr_str.split(',')

    smtp = smtplib.SMTP_SSL()
    # 一般端口为25,QQ邮箱端口为465
    smtp.connect(configs.EMAIL_SERVER, configs.EMAIL_PORT)
    smtp.login(from_addr, password)

    log_send_email = ''
    try:
        smtp.sendmail(from_addr, to_addr_list, msg.as_string())
#         print('邮件发送成功！')
        log_send_email = to_addr_str[0:-1] + ' 邮件发送成功！'
    except ConnectionError:
        #         print('发送失败，请检查你的账号是否有效或网络是否良好！')
        log_send_email = to_addr_str[0:-1] + ' ' + '邮件发送失败，请检查你的账号是否有效或网络是否良好！'
    except Exception as e:
        log_send_email=to_addr_str[0:-1] + ' ' +e.message
    smtp.quit()
    return log_send_email

# 获取微信access_token
# TODO 每两小时token会过期，一天大概只能获取2000次
def get_token():
    payload_access_token={
        'grant_type': configs.GRANT_TYPE,
        'appid': configs.APPID,
        'secret': configs.SECRET
    }
    token_url='https://api.weixin.qq.com/cgi-bin/token'
    try:
        r=requests.get(token_url,params=payload_access_token)
        dict_result= (r.json())
        #log_send_wechat = '获取token成功'
        return dict_result['access_token']
    except ConnectionError:
        raise Exception('获取token失败，请检查获取上限或网络')


# 发送消息给订阅号(订阅号由get_token决定
def send_to_wechat(str='default_words!'):
    pay_send_all={
        "filter":{
            "is_to_all": True
        },
        "text":{
            "content":str
        },
        "msgtype":"text"
    }
    try:
        url="https://api.weixin.qq.com/cgi-bin/message/mass/sendall?access_token="+get_token()
        jsonstr = json.dumps(pay_send_all,ensure_ascii=False,indent = 2 ) ; # 转换到json，注意处理中文的unicode
        headers = {'content-type': 'text/json','charset':'utf-8'} # 加http header，命令以utf-8解析
        r=requests.post(url=url,data=jsonstr.encode('utf-8') , headers=headers )
        # result=r.json()
        log_send_wechat = '微信发送成功'
    except Exception:
        log_send_wechat = '微信发送失败'
    return log_send_wechat

def Send(msgs, subject, send_number, to_addr_str, message_type,flag=True):
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
        message_type: 类型(通知/新闻)
        flag: 一个可选变量，用来决定是否在发送日志中记录此次发送信息，默认为True(记录)
    '''
    log_send = []
#     log_send=['test\n']    # Only for test

    for msg in msgs:
        temp="{}有新{},快去看看吧\n标题:{}\n时间:{}\n查看:{}".format(
            subject,message_type,msg['title'],msg['date'],msg['link'])
        log_send_sms = []
        log_send_email = []
        log_send_wechat = []
        log_send_sms.append(Send_sms(send_number, temp))
        log_send_email.append(Send_email(temp, to_addr_str, subject+message_type+'更新'+tool.time_text()))
        log_send_wechat.append(send_to_wechat(temp))
        log_send.append(log_send_sms)
        log_send.append(log_send_email)
        log_send.append(log_send_wechat)
    if(flag == True):
        Log_Write('Send', log_send)
