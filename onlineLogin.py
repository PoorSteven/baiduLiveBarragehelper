# -*- coding: utf-8 -*-
# @Time : 2021-05-01 2:12
# @Author : Steven
# @QQ : 2621228281
# @Email : 2621228281@qq.com
# @File : onlineLogin.py
# @Software: PyCharm
import sys
import os
import re
import random
import urllib3
import time
import datetime
import requests
import uuid
import hashlib
import pymysql
# import images
from tkinter import messagebox
import tkinter as tk

root = tk.Tk()
root.withdraw()  # ****实现主窗口隐藏
root.lift()
root.attributes("-topmost", True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



# 连接MySQL数据库
con = pymysql.connect(
    host='121.42.229.227',
    db='baidumac',
    user='baidumac',
    passwd='h940834918',
    port=3306,
    charset='utf8'
)
# 获取游标
cursor = con.cursor()


# 在线人气协议类
class onlinePopul():
    # 初始化获取CK列表
    def __init__(self, ckLists):
        # self.ckLists = ckLists
        self.ckLists = ckLists

    # 获取房间ID
    def get_room_id(self):
        if os.path.isfile('setting.ini') == True:
            url = open('setting.ini', 'r', encoding='utf-8').readlines()[0]
            url = url.split('&')[0]
            room_id = re.findall(r'room_id=(.*)', url)[0]
            # print('获取房间ID:'+room_id)
            return room_id
        else:
            messagebox.showinfo("提示", "请先保存配置文件，然后在使用！")
            exit()

    #登陆时间间隔
    def onlineTime(self):
        with open('.ini/onlinetime.ini','r',encoding='utf-8')as f:
            onlineTime = f.readline().strip()

        return onlineTime

    # 人气协议新线程函数入口
    def onlineThread(self):
        roomID = self.get_room_id()
        cknum = 0
        onlineTime = self.onlineTime()
        print('时间间隔：',onlineTime)
        for cookie in self.ckLists:

            userData = self.get_login(cookie)
            time.sleep(int(onlineTime))
            # print(userData)
            userName = userData[0]
            if userData[1] == 1:
                cknum += 1
                userInfo = '是'
                print('=' * 45)
                print('账号名：{userName}    |||    是否登录：{userInfo}'.format(userName=userName, userInfo=userInfo))
                print('=' * 45)
                print('登陆成功！')
                print('=' * 45)

                print(f'当前登陆账号的数量为：{cknum} 个')
                print('\n')
                with open('.ini/onlinenum.ini', 'w', encoding='utf-8')as f:
                    f.write(str(cknum))
                    f.close()
            elif userData[1] == 0:
                print('账号名：{userName}    |||    是否登录：{userInfo}'.format(userName=userName, userInfo=userInfo))
                print('=' * 45)
                print('账号异常！可能已经失效！')
                print('=' * 45)
                print('\n')

            else:
                print('=' * 45)
                print('网络异常波动>>>>>>>>>>>>>>！')
                print('=' * 45)



        messagebox.showinfo("提示", f"百度CK账号登录成功：{cknum}个，请刷新登录数量查看！")
        print('=' * 45)
        print('所有CK账号登陆完毕，请等待5~20秒直播间延迟刷新！')
        print('=' * 45)
        print('现在您可以关闭子窗口！')

    # 单账号登陆
    def get_login(self, cookie):
        roomID = self.get_room_id()
        print(f'当前房间账号ID为：{roomID}')
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'mbd.baidu.com',
            'Referer': 'https://live.baidu.com/',
            'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'Sec-Fetch-Dest': 'script',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
            'Cookie': cookie
        }
        # print(room_id)
        information_url = 'https://mbd.baidu.com/searchbox?cmd=371&action=star&service=bdbox&osname=pc&data=%7B%22data%22%3A%7B%22room_id%22%3A%22'+roomID+'%22%2C%22replay_slice%22%3A0%2C%22nid%22%3A%22%22%2C%22device_id%22%3A%22pc-'+self.ran_tag_str(32)+'%22%2C%22source_type%22%3A0%7D%7D&_='+str(int(self.get_time() * 1000))

        #information_url = 'https://mbd.baidu.com/searchbox?cmd=371&action=star&service=bdbox&osname=pc&data=%7B%22data%22%3A%7B%22room_id%22%3A%22'+roomID+'%22%2C%22replay_slice%22%3A0%2C%22nid%22%3A%22%22%2C%22device_id%22%3A%22pc-'+self.ran_tag_str(32)+'%22%2C%22source_type%22%3A0%7D%7D&_='+str(int(self.get_time() * 1000))




        information = requests.get(url=information_url, headers=headers, verify=False)
        if information.status_code == 200:

            reults = information.json()
            # print(reults)
            userName = reults['data']['371']['users']['nick_name']
            userInfo = reults['data']['371']['user_info']['is_login']


        else:
            userName = 'Null'
            userInfo = 0
            print('CK账号失效！')

        return userName, userInfo

    # 随机ID
    def ran_tag_str(self, num):
        # 随机变量
        suiji = 'abcdefghijklmnopqrstuvwxyz0123456789'
        salt = ''
        for i in range(num):
            i = random.choice(suiji)
            salt += i
        return salt

    # 获取时间戳
    def get_time(self):
        shijiancuo = time.time()
        return shijiancuo

    # 增加时间
    def sql_fail_time(self, day):
        today = datetime.datetime.now()
        # 当前时间增加一天
        offset = datetime.timedelta(days=day)
        re_date = (today + offset).strftime('%Y-%m-%d %H:%M:%S')
        return re_date

    # 时间戳对比时间
    def time_stamp(self, time_data):
        timeArray = time.strptime(time_data, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp

    # 获取当前时间
    def get_now_time(self):
        a = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return a

    # 获取时间戳
    def get_time(self):
        shijiancuo = time.time()
        return shijiancuo


if __name__ == '__main__':


    if os.path.isfile('CK.txt') == True:

        with open('CK.txt', 'r', encoding='utf-8')as f:
            # 去换行符
            ckLists = [x.strip() for x in f.readlines() if x.strip() != '']
            print('=' * 45)
            print(f'一共{len(ckLists)}个账号等待连接直播间！')
            print('=' * 45)
            print('即将准备登陆账号>>>>>>>>>>>>>>>>>>>>>>>>')
            time.sleep(3)
            print('=' * 45)
    # 循环登陆账号

    if os.path.isfile('setting.ini') == True:
        try:
            online_login = onlinePopul(ckLists).onlineThread()
        except:
            pass
    else:
        messagebox.showinfo("提示", "请先保存配置文件，然后在使用！")
        sys.exit()
    time.sleep(1)

    sys.exit()
