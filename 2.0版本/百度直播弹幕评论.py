# -*- coding: utf-8 -*-
# @Time : 2020/11/15 22:15
# @Author : Steven
# @QQ : 2621228281
# @Email : 2621228281@qq.com
# @File : 百度直播弹幕评论.py
# @Software: PyCharm

import requests
import time
import os
import json
import uuid
import re
import random
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#广告发送请求
def get_resquests(headers,room_id,text):

    live_url = 'https://mbd.baidu.com/searchbox?cmd=366&action=liveshow&service=bdbox&osname=baiduboxapp&data=%7B%22data%22%3A%7B%22roomid%22%3A%22'+room_id+'%22%2C%22device_id%22%3A%22'+str(ran_tag_str(16))+'%22%2C%22source_type%22%3A1%2C%22text%22%3A%22'+text+'%22%2C%22timestamp%22%3A'+str(int(get_time()))+'%7D%7D'


    data = {
        'cmd': '366',
        'action': 'star',
        'service': 'bdbox',
        'osname': 'pc',
        'data': '{"data":{"roomid":"'+room_id+'","device_id":"","source_type":1,"text":"'+text+'","timestamp":'+str(int(get_time()))+'}}',
    }

    response = requests.post(live_url,headers=headers,verify=False)
    results = json.loads(response.text)
    if results["errno"] == '0' :
        time.sleep(1)
        print('当前广告语为：' + text)
        print('==============================================================')
        time.sleep(1)
        print('>>>>>>>>>>>>>>>>>>>>>>广告发送成功！>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print('==============================================================')
        print('\n')

    else:
        print('==============================================================')
        print('>>>>>>>>>>>>>>>>>>>>>>广告发送失败！>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print('==============================================================')
        print('\n')

#随机生成

#随机ID
def ran_tag_str(num):
    #随机变量
    suiji = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    salt = ''
    for i in range(num):
        salt += random.choice(suiji)
    return salt

#房间信息获取
def get_web_information(room_id,headers):

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'mbd.baidu.com',
        'Referer': 'http://live.baidu.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4462.0 Safari/537.36',
        'Cookie': 'BAIDUID=CCBD6886BFA1A34A92EC5BFF49CC3E51:FG=1; BIDUPSID=CCBD6886BFA1A34A92EC5BFF49CC3E51; PSTM=1605065139; MBD_AT=0; userDeviceId=fhc6ij1605452779; BAIDUID_BFESS=CCBD6886BFA1A34A92EC5BFF49CC3E51:FG=1; x-logic-no=2'
    }
    # print(room_id)
    information_url = 'http://mbd.baidu.com/searchbox?'

    params = {
        'cmd': '371',
        'action': 'star',
        'service': 'bdbox',
        'osname': 'h5pre',
        'data': '{"data":{"room_id":"'+room_id+'","device_id":"pc-'+ran_tag_str(32)+'","source_type":0}}',
        '_': str(int(get_time()*1000)),
        # 'callback': '__jsonp_callback_0__'
    }

    information = requests.get(url=information_url, headers=headers, params=params)

    reults = information.json()

    # fans_num = reults['data']['371']['host']['fans']
    # image_url = reults['data']['371']['host']['image']['image_33']
    name = reults['data']['371']['host']['name']
    # print(name)
    online_users = reults['data']['371']['online_users']
    title = reults['data']['371']['video']['title']
    # print(title)
    print('▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼')
    print('当前直播间标题：'+title)
    print('==============================================================')
    time.sleep(1)
    print('当前直播间作者：'+name+'   ▎▎ '+'当前真实在线人数为： ' + online_users)
    print('==============================================================')
    time.sleep(1)
    # print('当前小号名称为：' + nick_name.encode('utf8').decode('unicode_escape'))
    # print('==============================================================')

#开头广告
def get_ads():
    print(
        '                       ***欢迎使用全新Steven百度直播评论小脚本！***\n\n' + '运行之前请先设置广告语和直播间评论设置，广告语一行一个，直播间评论第一行为直播间地址，第二行为评论延迟时间！\n\n' + '名称为：【 LiveSetting.ini 】的ini配置文件为直播间配置文件\n\n' + '名称为：【ADS.txt】的为广告语' + '名称为：【 CK.txt 】的为CK业务号' + '如有疑问请联系Steven QQ：2621228281\n')
    time.sleep(5)
    print('※※※※※ 软件即将开始运行 ※※※※※')
    print('▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼')
    print('√ 广告语是否设置完成？')
    print('√ 直播间ID是否设置完成？')
    print('√ 延迟是否设置完成？')
    print('√ CK评论业务号是否设置完成？')
    print('▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲')
    print('\n')
    print('★★★★★★★友情 提示★★★★★★★')
    print('如若确认无误，软件在5秒后开始运行，\n有一项设置没有完成，软件无法正常运行，\n请关闭软件设置好后再打开运行！')
    print('★★★★★★★★★★★★★★★★★★★')
    time.sleep(5)
    print('\n')
    print('☯☯☯☯☯')
    print('评论开始')
    print('☯☯☯☯☯')
    print('☯:您可以把软件最小化窗口开播了！')

#获取时间戳
def get_time():
    shijiancuo = time.time()
    return shijiancuo

#获取随机cookieS
def get_choice_cookies(cookies_list):
    cookies = cookies_list[random.randint(0,len(cookies_list)-1)].strip('\n')
    # print(cookies)
    return cookies

if __name__ == '__main__':
    ADS_list = open('ADS.txt', 'r', encoding='utf-8').readlines()
    room_id = open('LiveSetting.ini', 'r', encoding='utf-8').readlines()[0].replace('RoomID：', '').strip()
    dalay = open('LiveSetting.ini', 'r', encoding='utf-8').readlines()[1].replace('Delay：', '')
    cookies_list = open('CK.txt', 'r', encoding='utf-8').readlines()
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Host': 'mbd.baidu.com',
        'Origin': 'http://mbd.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4321.2 Safari/537.36'
    }
    get_ads()
    #获取房间ID
    # room_id = get_room_id(roomurl)
    while True:
        for ads in ADS_list:
            ads = ads.strip('\n')
            try:
                headers['Cookie'] = get_choice_cookies(cookies_list)
                # 获取直播间信息，作者和标题等！
                get_web_information(room_id,headers)
                #广告发送请求fran_tag_str
                get_resquests(headers,room_id,ads)
                print('▶▶▶:进入延迟倒计时，请耐心等待！！！')
                time.sleep(int(dalay))

            except :
                print('==============================================================')
                print('>>>>>>>>>>>>>>>>>>>>>>广告发送失败！>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                print('==============================================================')
                print('\n')

