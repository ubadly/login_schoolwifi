#!/usr/bin/env python
# -*- coding:utf-8 -*-


# 导入模块
import requests
import re
import sys
import json
from time import sleep
import base64
import os
import configparser
import getpass

############
os.system('color E6')
os.system('mode con cols=68 lines=20')
os.system('title 统院校园网第三方简易客户端3.0')



# 获取wlanuserip
try:
    html = requests.get('http://baidu.com')
    userip = re.findall(r'wlanuserip=(.*?)&wlan', html.text)[0]
except:
    print ('网络已连接！\n如果没有网络请检查是否已经连接到校园网\n或者检测是否开启了代理')
    t = input('按Enter退出...')
    sys.exit(0)

# 请求链接
url = 'http://111.7.172.99:8246/eportal/InterFace.do?method=login'


# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    'Referer': 'http://111.7.172.99:8246/eportal/index.jsp?wlanuserip=' + userip + '&wlanacname=AC&ssid=BJ-HNTY&nas_ip=117.158.206.178&flag=location',
    'Connection': 'keep-alive',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}
#配置账号信息文件
def setini():
    conf = configparser.ConfigParser()
    if os.path.exists('C:/Users/xg_user.ini'):
        conf.read('C:/Users/xg_user.ini')
        username = conf['user']['username']
        password = conf['user']['password']
        login(username,password)
    else:
        username = str(base64.b64encode(input('校园网账号：').encode('utf-8')),'utf-8')
        password = str(base64.b64encode(getpass.getpass('校园网密码[密码不会显示，输完回车即可]：').encode('utf-8')),'utf-8')
        conf['user'] = {
            'username':username,
            'password':password
        }
        with open('C:/Users/xg_user.ini','w') as file:
            conf.write(file)
        login(username, password)



# 登录
def login(username,password):
    #h获取账号密码

    # 校园网账号
    username = base64.b64decode(username)
    # 校园网密码
    password = base64.b64decode(password)


    # 设置表格数据
    data = {
        'userId': username,
        'password': password,
        'service': 'internet',
        'queryString': 'wlanuserip%3D' + userip + '%26wlanacname%3DAC%26ssid%3DBJ-HNTY%26nas_ip%3D117.158.206.178%26flag%3Dlocation',
        'operatorPwd': '',
        'operatorUserId': '',
        'validcode': '',
        'passwordEncrypt': 'false',
    }

    # 模拟首次登录
    response = requests.post(url, data=data, headers=headers)
    # 获取请求的返回值
    response.encoding = 'utf-8'
    result = response.json()
    if '"result":"fail"' in response.text:
        print('账号或密码错误！！')
        t = input('按Enter重新输入...')
        t = os.system('cls')
        os.remove('C:/Users/xg_user.ini')
        setini()
    else:
        userIndex = str(result['userIndex'])
        requests.post('http://111.7.172.99:8246/eportal/InterFace.do?method=getOnlineUserInfo',data={'userIndex':userIndex},headers=headers)
        sleep(3)
        response = requests.post('http://111.7.172.99:8246/eportal/InterFace.do?method=getOnlineUserInfo',data={'userIndex':userIndex},headers=headers)
        response.encoding = 'utf-8'
        user = response.text
        user = json.loads(user)
        tips = user['welcomeTip']
        userName = user['userName']
        userPackage = user['userPackage']
        userGroup = user['userGroup']
        userPhone = user['userId']
        requests.post('http://111.7.172.99:8246/eportal/success.jsp?userIndex=' + userIndex + '&keepaliveInterval=0', data=data,headers=headers)
        os.system('cls')
        print('=========================%s======================='%userGroup)
        print('%s,%s'%(userName,tips))
        print('你的手机号是：%s'%userPhone)
        print('校园网套餐是：%s'%userPackage)
        print('本地登录IP：' + userip)
        print('你的账号ID：' + userIndex[-12:-1])
        print('\n\n如果上方提示IP和ID后面都有对应的值则登录成功，反之失败！')
        print('如果想要切换账号只需要把C:/Users/xg_user.ini文件删除即可')
        print('============================Power By LuSao==========================')
        t = input('按Enter退出...')
        sys.exit(0)
if __name__ == '__main__':
    setini()
