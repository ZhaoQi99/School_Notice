# encoding='utf-8'
'''
@author: QiZhao
@contact: zhaoqi99@outlook.com
@since: 2018-09-19
@license: GNU GPLv3
@version: 0.2.1
@LastModifiedBy: QiZhao
@LastModifiedDate: 2018-10-27
'''
# show config
SCHOOL_NAME = ''
VERSION = ''
AUTHOR_NAME = ''
AUTHOR_EMAIL = ''

# twillo config
ACCOUNT_ID = ''
AUTH_TOKEN = ''
TWILIO_NUMBER = ''

# send_email config
FROM_ADDR = ""
PASSWORD = ""
EMAIL_PORT = 0
EMAIL_SERVER = ''

# Log Config
LOG_ENABLED = True

# spider config
SPIDER_CONFIG = [
    {
        'subject_EN': '',
        'subject_CN': '',
        'url': '',
        'url_main': '',
        'rule': '',
        'coding': ''
    },
    {
        'subject_EN': '',
        'subject_CN': '',
        'url': '',
        'url_main': '',
        'rule': '',
        'coding': ''
    }
]

# we_chat config

GRANT_TYPE = 'client_credential'
APPID = ' '
SECRET = ' ' 

# mysql config
TARGET_IP=''
SQL_USERNAME=''
SQL_PASSWORD=''
DATABASE_NAME=''
