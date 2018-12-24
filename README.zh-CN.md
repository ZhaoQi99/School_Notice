<div align="right">语言: <a title="英语" href="README.md">:us:</a>
:cn:</div>

# 校园通知

---

[![Build Status](https://travis-ci.org/ZhaoQi99/School_Notice.svg?branch=master)](https://travis-ci.org/ZhaoQi99/School_Notice)
[![Release](https://img.shields.io/github/release/ZhaoQi99/School_Notice.svg)](https://github.com/ZhaoQi99/School_Notice/releases)
[![License](https://img.shields.io/github/license/ZhaoQi99/School_Notice.svg)](https://github.com/ZhaoQi99/School_Notice/blob/master/LICENSE)
[![GitHub forks](https://img.shields.io/github/forks/ZhaoQi99/School_Notice.svg)](https://github.com/ZhaoQi99/School_Notice/network)
[![GitHub stars](https://img.shields.io/github/stars/ZhaoQi99/School_Notice.svg)](https://github.com/ZhaoQi99/School_Notice/stargazers) 

## 简介
应用Python对校园各类网站的通知更新进行短信，邮件提醒。

## 功能
- [x] 通知更新短信提醒
- [x] 通知更新邮件提醒
- [x] 多人同时进行提醒
- [x] 发送日志、更新检查日志 
- [x] 日志功能可选
- [ ] 每个用户要提醒的部门可选
- [x] 数据库存储/文件存储

## 依赖项
* [Python](http://www.python.org/)
* `pip install twilio`

## 使用脚本
1. 使用命令克隆项目至本地
`git clone https://github.com/ZhaoQi99/School_Notice.git`
2. 申请[Twilio](https://www.twilio.com/)免费试用账号
3. 编辑`configs.py`文件，修改配置文件。
4. 运行`main.py`文件

## 配置
您可以 (应该) 修改以下几个设置，如果不需要使用Twilio/邮件提醒功能，请保持默认。

### Send Email Config
依次填入发件人邮箱地址，密码，发送端口，发送邮件的smtp服务器地址
```
FROM_ADDR = ""
PASSWORD = ""
EMAIL_PORT = 0
EMAIL_SERVER = ''
```
### Twillo Config
在Twilio账号的个人信息页，可以找到以下几个参数
```
ACCOUNT_ID = ''
AUTH_TOKEN = ''
TWILIO_NUMBER = ''
```

### Show Config
在窗口中显示的内容，包括：学校姓名，脚本版本，作者姓名，作者邮箱
```
SCHOOL_NAME = ''
VERSION = ''
AUTHOR_NAME = ''
AUTHOR_EMAIL = ''
```
### Log Config
是否在日志文件中记录日志，默认为True
```
LOG_ENABLED = True
```
### Save Type Config
数据存储类型,分为文件存储，数据库存储
```
SAVE_TYPE = 'MYSQL'
SAVE_TYPE = 'File'
```
### Show Right Config
是否显示版权信息
```
SHOW_RIGHT = False
```

### Spider Config
爬虫的相关配置，包括:部门名称(EN)，部门名称(CN)中，"更多通知"页的链接，链接的公共部分，正则表达式，网页编码格式，类型(通知/新闻）
department_EN：数据文件的文件名
department_CN：用于在日志、邮件标题中显示
**警告:正则表达式中必须有三个分组，且名称必须为`link,date,title`**
如:`info/1085/(?P<link>\d+\.htm)" target="_blank">(?P<title>[\s\S]{5,100})（(?P<date>\d*-\d*-\d*)）`

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
这里有一个爬虫配置的例子:
#### 例子
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
## 打包exe(Windows)
1. 安装pywin32
`pip install pywin32`
2. 安装Pyinstaller
`pip install PyInstaller`
3. (可选)移动程序图标至当前文件夹，命名为`logo.ico`
4. 使用`pyinstaller`打包程序
`pyinstaller -F main.py`或者`pyinstaller -F -i logo.ico main.py`
5. 进入dist文件夹，可以看到main.exe
`cd dist`

## 贡献者

感谢所有对本项目做出过贡献的开发者([emoji key](https://github.com/kentcdodds/all-contributors#emoji-key)):

| [<img src="https://avatars3.githubusercontent.com/u/7782671?v=4" width="100px;"/><br /><sub><b>Keyi Xie</b></sub>](https://xiekeyi98.github.io/)<br />[💻](https://github.com/ZhaoQi99/School_Notice/commits?author=xiekeyi98 "Code") [📖](https://github.com/ZhaoQi99/School_Notice/commits?author=xiekeyi98 "Documentation")| [<img src="https://avatars3.githubusercontent.com/u/40024866?v=4" width="100px;"/><br /><sub><b>jhy</b></sub>](https://Small-funny.github.io/)<br />[💻](https://github.com/ZhaoQi99/School_Notice/commits?author=Small-funny "Code") [📖](https://github.com/ZhaoQi99/School_Notice/commits?author=Small-funny "Documentation")|
| :---: | :---: |

## 开源协议 & 作者
* 作者:Qi Zhao([zhaoqi99@outlook.com](mailto:zhaoqi99@outlook.com))
* 开源协议:[GNU General Public License v3.0](https://github.com/ZhaoQi99/School_Notice/blob/master/LICENSE)