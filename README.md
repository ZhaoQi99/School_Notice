<div align="right">Language: :us:
<a title="Chinese" href="README.zh-CN.md">:cn:</a></div>

# School_Notice

---

[![Build Status](https://travis-ci.org/ZhaoQi99/School_Notice.svg?branch=master)](https://travis-ci.org/ZhaoQi99/School_Notice)
[![Release](https://img.shields.io/github/release/ZhaoQi99/School_Notice.svg)](https://github.com/ZhaoQi99/School_Notice/releases)
[![License](https://img.shields.io/github/license/ZhaoQi99/School_Notice.svg)](https://github.com/ZhaoQi99/School_Notice/blob/master/LICENSE)
[![GitHub forks](https://img.shields.io/github/forks/ZhaoQi99/School_Notice.svg)](https://github.com/ZhaoQi99/School_Notice/network)
[![GitHub stars](https://img.shields.io/github/stars/ZhaoQi99/School_Notice.svg)](https://github.com/ZhaoQi99/School_Notice/stargazers) 

## Introduction
An application of using python to check notifications update for various campus website,and send SMS reminder,email reminder.

## features
- [x] Notification update SMS reminder
- [x] Notification update email reminder
- [x] Simultaneous reminders for multiple people
- [x] Send log、check udate log 
- [x] log function optional
- [ ] The department which each user need to be reminded is optional
- [x] Database storage／file storge

## Dependencies
* [Python](http://www.python.org/)
* `pip install twilio`

## Using script
1. Using command to clone the the repository to local folder
`git clone https://github.com/ZhaoQi99/School_Notice.git`
2. Apply for [Twilio](https://www.twilio.com/) Free trial account
3. Edit the `configs.py` file to modify the configuration file.
4. Run the `main.py` file

## Configuration
You can (and should) modify a couple of settings. if you do not need to use the twilio/Mail reminder feature, keep the default.

### Send Email Config
Fill in the sender's e-mail address, password, port, and SMTP server address in turn
```
FROM_ADDR = ""
PASSWORD = ""
EMAIL_PORT = 0
EMAIL_SERVER = ''
```
### Twillo Config
The following parameters can be found on the personal information page of the Twilio account.
```
ACCOUNT_ID = ''
AUTH_TOKEN = ''
TWILIO_NUMBER = ''
```

### Show Config
Content which is displayed in the window，including: school Name, script version, author name, author email
```
SCHOOL_NAME = ''
VERSION = ''
AUTHOR_NAME = ''
AUTHOR_EMAIL = ''
```

### Log Config
Whether logs can be logged in the log file, which is true by default
```
LOG_ENABLED = True
```

### Save Type Config
The　type of storging data,including file storge,mysql storge
```
SAVE_TYPE = 'MYSQL'
SAVE_TYPE = 'File'
```
### Show Right Config
Whether show the information of copyright.
```
SHOW_RIGHT = False
```

### Spider Config
Crawler  configuration，including: department type (EN), department type (CN), "more notifications " page link, link public part, regular expression, Web page encoding format,type(notice/news)
department_EN: File name of data file
department_CN： Used to display in logs, message headers
**Warning: There must be three groups in the regular expression, which the name must be ` link,date,title`**
Such as:`info/1085/(?P<link>\d+\.htm)" target="_blank">(?P<title>[\s\S]{5,100})（(?P<date>\d*-\d*-\d*)）`
```python
SPIDER_CONFIG = [
	{
	    'department_EN': '',
	    'department_CN': '',
	    'url': '',
	    'url_main': '',
	    'rule': '',
	    'coding': '',
	    'type': '' 
	},
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
```
Here is an example about crawler configuration:
#### Example
```python
SPIDER_CONFIG = [
    {
        'department_EN': 'snnu_index',
        'department_CN': '学校主页',
        'url': 'http://www.snnu.edu.cn/tzgg.htm',
        'url_main': 'http://www.snnu.edu.cn/info/1085/',
        'rule': 'info/1085/(?P<link>\d+\.htm)" target="_blank">(?P<title>[\s\S]{5,100})（(?P<date>\d*-\d*-\d*)）',
        'coding': 'utf-8',
        'type': '通知'
    },
    {
        'department_EN': 'snnu_index',
        'department_CN': '学校主页',
        'url': 'http://www.snnu.edu.cn/sdxw.htm',
        'url_main': 'http://www.snnu.edu.cn/info/1084/',
        'rule': 'info/1084/(?P<link>\d+.htm)" target="_blank" title="(?P<title>[^"]+?)"><[^<]+?<[^<]+?<[^<]+?<p class="qh-wide-pushtime">(?P<date>\d*-\d*-\d*)',
        'coding': 'utf-8',
        'type': '新闻' 
    }
]
```
## Packaging exe(Windows)
1. Install  pywin32
`pip install pywin32`
2.  Install Pyinstaller
`pip install PyInstaller`
3. (optional)Move the program icon to the current folder, renamed ' Logo.ico 
4.  Using `pyinstaller` package program
`pyinstaller -F main.py`Or`pyinstaller -F -i logo.ico main.py`
5. Go to the Dist folder and you can see the Main.exe
`cd dist`

## Contributors

Thanks goes to these wonderful people ([emoji key](https://github.com/kentcdodds/all-contributors#emoji-key)):

| [<img src="https://avatars3.githubusercontent.com/u/7782671?v=4" width="100px;"/><br /><sub><b>Keyi Xie</b></sub>](https://xiekeyi98.github.io/)<br />[💻](https://github.com/ZhaoQi99/School_Notice/commits?author=xiekeyi98 "Code") [📖](https://github.com/ZhaoQi99/School_Notice/commits?author=xiekeyi98 "Documentation")| [<img src="https://avatars3.githubusercontent.com/u/40024866?v=4" width="100px;"/><br /><sub><b>jhy</b></sub>](https://Small-funny.github.io/)<br />[💻](https://github.com/ZhaoQi99/School_Notice/commits?author=Small-funny "Code") [📖](https://github.com/ZhaoQi99/School_Notice/commits?author=Small-funny "Documentation")|
| :---: | :---: |

## License & Author
* Author:Qi Zhao([zhaoqi99@outlook.com](mailto:zhaoqi99@outlook.com))
* License:[GNU General Public License v3.0](https://github.com/ZhaoQi99/School_Notice/blob/master/LICENSE)