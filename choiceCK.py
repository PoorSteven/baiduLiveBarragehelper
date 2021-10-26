# -*- coding: utf-8 -*-
# @Time : 2021-05-13 21:12
# @Author : Steven
# @QQ : 2621228281
# @Email : 2621228281@qq.com
# @File : SendComments.py
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

from tkinter import messagebox
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import tkinter as tk
root = tk.Tk()
root.withdraw() #****实现主窗口隐藏
root.lift()
root.attributes("-topmost", True)

class BaiduComments():
    def __init__(self,comment,cookie,roomID):
        self.comment = comment
        self.cookie = cookie
        self.roomID = roomID

    #发送评论弹幕
    def send_comments(self):
        # print(comment,Cookie)
        try:
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Host': 'mbd.baidu.com',
                'Referer': 'https://live.baidu.com/',
                'sec-ch-ua-mobile': '?0',
                # 'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/13.0 MQQBrowser/10.1.1 Mobile/15B87 Safari/604.1 QBWebViewUA/2 QBWebViewType/1 WKType/1',
                'Cookie': Cookie
            }

            url = 'https://mbd.baidu.com/searchbox?'
            params = {
                'cmd': '366',
                'action': 'star',
                'service': 'bdbox',
                'osname': 'ios',
                # 'data': '{"data": {"roomid": "'+self.roomID+'", "device_id": "'+self.ran_tag_str(32)+'", "source_type": 1,"text": "'+comment+'"}}',
                'data': '{"data":{"roomid":"' + self.roomID + '","device_id":"' + self.ran_tag_str(
                    32) + '","source_type":1,"biz":{"roomid":"' + self.roomID + '"},"text":"' + comment + '","jt":"' + self.ran_tag_str(
                    471) + '|10|' + self.ran_tag_str(32) + '"}}',
                '_': str(int(self.get_time() * 1000))
                # callback: __jsonp_callback_1__
            }
            response = requests.get(url,headers=headers,params=params,verify=False)

            if response.status_code == 200:
                result = response.json()
                # print(result)
                if result['errno'] == '0':
                    # print('发送成功！')
                    print('弹幕语为：'+comment)
                    print('='*40)
                    print('发送成功！')
                    print('=' * 40)
                    messagebox.showinfo("成功提示", f"弹幕评论语：{comment},发送成功！")

                else:
                    print('弹幕发送失败！协议连接不上，查看网络是否断开')
                    print('=' * 40)

            else:
                print('弹幕发送失败！CK账号有部分可能失效')
                print('=' * 40)

        except:
            print('弹幕发送失败！CK账号有部分可能失效')
            print('=' * 40)

    # 随机ID
    def ran_tag_str(self,num):
        # 随机变量
        suiji = 'abcdefghijklmnopqrstuvwxyz0123456789'
        salt = ''
        for i in range(num):
            i = random.choice(suiji)
            salt += i
        return salt

    # 获取当前时间
    def get_now_time(self):
        a = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return a

    # 获取时间戳
    def get_time(self):
        shijiancuo = time.time()
        return shijiancuo


if __name__ == '__main__':
    if os.path.isfile('.ini/oneTrainSend.ini') == True:
        with open('.ini/oneTrainSend.ini','r',encoding='utf-8')as f:
            data = f.readlines()
            roomID = data[0].strip()
            cookie = data[1].strip()
        with open('.ini/choiceCK.ini','r',encoding='utf-8')as d:
            comment = d.read().strip()

        baiduComments = BaiduComments(comment,cookie,roomID)

        baiduComments.send_comments()
        sys.exit()
    else:
        messagebox.showinfo("提示", "请打开主程序后在使用！")
        sys.exit()


