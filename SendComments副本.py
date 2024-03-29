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
import tkinter as tk
from tkinter import messagebox
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
root = tk.Tk()
root.withdraw() #****实现主窗口隐藏
root.lift()
root.attributes("-topmost", True)

class BaiduComments():
    def __init__(self,cycles,delayFirst,delayLast,ckPath,adsPath,roomID):
        self.cycles = cycles
        self.delayFirst = delayFirst
        self.delayLast = delayLast
        self.ckPath = ckPath
        self.adsPath = adsPath
        self.roomID = roomID

    #获取所有CK账号
    def get_all_ck(self):
        with open(self.ckPath, 'r', encoding='utf-8')as f:
            ckLists = f.readlines()
            f.close()
        return ckLists

    #获取所有ADS
    def get_all_ads(self):
        with open(self.adsPath,'r',encoding='utf-8')as f:
            adsLists = f.readlines()
        return adsLists

    # 发送配置
    def send_run(self):
        ads_list = self.get_all_ads()
        num = 0
        while int(self.cycles) > num:
            num += 1

            for comment in ads_list:

                Cookie = self.get_choice_cookies()
                # print(Cookie)
                self.show_send_information()
                self.send_comments(comment.strip(), Cookie)
                print('▶▶▶:进入延迟倒计时，请耐心等待！！！')
                self.comments_delay()



        print('本次弹幕大循环发送，结束！！>>>>>>>>>>>')
        # input('按任意键退出！')
        messagebox.showinfo("提示", "本次弹幕大循环发送结束！，请点击停止")
        sys.exit()

    #发送评论展示发送情况
    def show_send_information(self):

        data = self.get_web_information()
        # print(data)
        print('◈'*35)
        time.sleep(1)
        print('直播间标题：{}'.format(data[0]))
        time.sleep(1)
        print('='*40)
        time.sleep(1)
        print('主播名称：{name} ☯ 在线观看人数：{online_ueser} ☯ 关注人数：{follow}'.format(name=data[1],online_ueser=data[2],follow=data[3]))
        time.sleep(1)
        print('='*40)
        time.sleep(1)

    #发送评论弹幕
    def send_comments(self,comment,Cookie):
        # print(comment,Cookie)
        try:
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Host': 'mbd.baidu.com',
                'Referer': 'https://live.baidu.com/',
                'sec-ch-ua-mobile': '?1',
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/13.0 MQQBrowser/10.1.1 Mobile/15B87 Safari/604.1 QBWebViewUA/2 QBWebViewType/1 WKType/1',
                'Cookie': Cookie
            }

            url = 'https://mbd.baidu.com/searchbox?'
            params = {
                'cmd': '366',
                'action': 'star',
                'service': 'bdbox',
                'osname': 'ios',
                'data': '{"data": {"roomid": "'+self.roomID+'", "device_id": "'+self.ran_tag_str(32)+'", "source_type": 1,"text": "'+comment+'"}}',
                '_': str(int(self.get_time()*1000))
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

                else:
                    print('弹幕发送失败！协议连接不上，查看网络是否断开')
                    print('=' * 40)

            else:
                print('弹幕发送失败！CK账号有部分可能失效')
                print('=' * 40)

        except:
            print('弹幕发送失败！CK账号有部分可能失效')
            print('=' * 40)

    # 评论延迟间隔
    def comments_delay(self):
        delay1 = int(self.delayFirst)
        delay2 = int(self.delayLast)
        random_time = random.randint(delay1,delay2)
        time.sleep(random_time)
        # self.time_sleep(random_time)

    # 获取随机cookies
    def get_choice_cookies(self):
        ckLists = self.get_all_ck()
        cookie = ckLists[random.randint(0, len(ckLists) - 1)].strip('\n')
        return cookie

     # 房间信息获取
    def get_web_information(self):
        try:
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
                'data': '{"data":{"room_id":"'+self.roomID+'","device_id":"pc-'+self.ran_tag_str(32)+'","source_type":0}}',
                '_': str(int(self.get_time()*1000)),
                # 'callback': '__jsonp_callback_0__'
            }

            information = requests.get(url=information_url, headers=headers, params=params)

            reults = information.json()

            fans_num = reults['data']['371']['host']['fans']
            image_url = reults['data']['371']['host']['image']['image_33']
            name = reults['data']['371']['host']['name']
            online_users = reults['data']['371']['online_users']
            title = reults['data']['371']['video']['title']

        except:
            print('房间连接异常！请检查网络')

        return title,name,online_users,fans_num

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
    #获取运行pid进程
    get_pid = os.getpid()
    print(f'程序pid:{get_pid}')
    with open('.ini/SendCommentsPID.ini','w',encoding='utf-8')as p:
        p.write(f'{get_pid}')
        p.close()

    if os.path.isfile('CK.txt') == True:
        with open('CK.txt', 'r', encoding='utf-8')as f:
            # 去换行符
            ckLists = [x.strip() for x in f.readlines() if x.strip() != '']
            print('=' * 45)
            print(f'一共{len(ckLists)}个账号随机进行发送评论！')
            print('='*45)
            print('即将准备发送评论>>>>>>>>>>>>>>>>>>>>>>>>')
            time.sleep(2)
            print('=' * 45)

    if os.path.isfile('.ini/sendComments.ini') == True:
        with open('.ini/sendComments.ini','r',encoding='utf-8')as f:
            data = f.readlines()
            print(data)
            ckPath = data[0].strip()
            adsPath = data[1].strip()
            roomID = data[2].strip()
            cycles = data[3].strip()
            delayFirst = data[4].strip()
            delayLast = data[5].strip()

        baiduComments = BaiduComments(cycles,delayFirst,delayLast,ckPath,adsPath,roomID)

        baiduComments.send_run()
        sys.exit()
    else:
        messagebox.showinfo("提示", "请打开主程序后在使用！")
        sys.exit()