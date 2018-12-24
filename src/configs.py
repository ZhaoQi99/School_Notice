# encoding='utf-8'
'''
@author: QiZhao
@contact: zhaoqi99@outlook.com
@since: 2018-09-19
@license: GNU GPLv3
@version: 0.3.0
@LastModifiedBy: QiZhao
@LastModifiedDate: 2018-12-24
'''
# show right
SHOW_RIGHT=False

# save type
# File/MySQL
SAVE_TYPE='MYSQL'

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
        'department_EN': '',
        'department_CN': '',
        'url': '',
        'url_main': '',
        'rule': '',
        'coding': '',
        'type': ''
    }
]

# we_chat config

GRANT_TYPE = 'client_credential'
APPID = ' '
SECRET = ' ' 

# mysql config
TARGET_IP='localhost'
SQL_USERNAME=''
SQL_PASSWORD=''
DATABASE_NAME=''
