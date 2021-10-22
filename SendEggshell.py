# -*- coding: utf-8 -*-
# @Time : 2021-05-14 0:48
# @Author : Steven
# @QQ : 2621228281
# @Email : 2621228281@qq.com
# @File : SendEggshell.py
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
from threading import Thread

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from tkinter import messagebox


class Eggshell():

    def __init__(self, zan, zanFirst, zanLast, share, shareFirst, shareLast, follow, followFirst, followLast, roomID,
                 ckPath):
        self.roomID = roomID
        self.ckPath = ckPath
        self.zan = zan
        self.zanFirst = zanFirst
        self.zanLast = zanLast
        self.share = share
        self.shareFirst = shareFirst
        self.shareLast = shareLast
        self.follow = follow
        self.followFirst = followFirst
        self.followLast = followLast

    # 获取时间戳
    def get_time(self):
        shijiancuo = time.time()
        return shijiancuo

    # 获取随机cookies
    def get_choice_cookies(self):
        with open(self.ckPath, 'r', encoding='utf-8')as f:
            ckLists = f.readlines()
        cookie = ckLists[random.randint(0, len(ckLists) - 1)].strip('\n')
        # print(cookies)
        return cookie

    # 封装弹幕点赞
    def zan_pack_msg(self):

        Cookie = self.get_choice_cookies()
        content_type = 'mix_zan'
        timestamp = str(int(self.get_time() * 1000))
        sign = self.str_MD5(content_type, timestamp)
        self.request_msg(Cookie, sign, timestamp, content_type)
        self.zan_delay()

    # 封装弹幕分享
    def share_pack_msg(self):
        Cookie = self.get_choice_cookies()
        content_type = 'mix_share'
        timestamp = str(int(self.get_time() * 1000))
        sign = self.str_MD5(content_type, timestamp)
        self.request_msg(Cookie, sign, timestamp, content_type)
        self.share_delay()

    # 封装弹幕关注
    def follow_pack_msg(self):
        Cookie = self.get_choice_cookies()
        content_type = 'mix_follow_anchor'
        timestamp = str(int(self.get_time() * 1000))
        sign = self.str_MD5(content_type, timestamp)
        self.request_msg(Cookie, sign, timestamp, content_type)
        self.follow_delay()

    # 获取signmd5值/点赞分享关注算法破解
    def str_MD5(self, content_type, timestamp):
        str = 'appname=haokancfrom=1022344hcontent_type={content_type}extRequest=from=1000575vim_sdk_version=7150036network=1_0room_id={room_id}sdk_version=4.3.3sid=8676_1-8915_3-8941_2-9040_1-9076_1-9088_1-9092_3-9100_1-9106_1-9108_1-9126_2-9128_1-9146_1-9149_2-9151_1-9153_2-9176_2-9185_2-9193_2-9201_2-9207_3-9224_1-9231_1-9235_2-9247_3-9251_1-9267_2-9248_4-9269_1-9278_2-9292_2-9294_4-9297_3-9298_2-9303_3-9310_1-9317_1-9329_1-9332_3-9340_1-9353_2-9357_1-9360_1-9364_4-9365_1-101_9-200_9-100_9-181_9-140_9-201_9-120_9-160_9-102_9-103_9timestamp={timestamp}tpl=ua=500_900_android_6.3.5.10_166uid=_aHViYPD2f0qa-uOgu28a0a6vilau28WYuvT8_ukH88j9WMtp8vnRwraAuser_id=1342904541ut=Pro 7 Plus_6.0.1_23_Meizuzid=EUAk_80SRqc-4OotI1R1j3LDMtspUHyUMLaN20o6cFyWvE0sj7M_B5_6o9ITABh-BoyamUMQbVlMfiw6G_v4N9d-Z7Gr_vGtDnXHeFYF911Ytiebaclient!!!'.format(
            content_type=content_type, room_id=self.roomID, timestamp=timestamp)
        # print(str)
        # 创建Md5对象
        create_md5 = hashlib.md5()
        create_md5.update(str.encode(encoding='utf-8'))
        result = create_md5.hexdigest().upper()
        # print(result)
        return result

    # 弹幕分享点赞转发
    def request_msg(self, Cookie, sign, timestamp, content_type):

        url = 'http://tiebac.baidu.com/bdlive/msg/sendOperationMsg?appname=haokan&sid=8676_1-8915_3-8941_2-9040_1-9076_1-9088_1-9092_3-9100_1-9106_1-9108_1-9126_2-9128_1-9146_1-9149_2-9151_1-9153_2-9176_2-9185_2-9193_2-9201_2-9207_3-9224_1-9231_1-9235_2-9247_3-9251_1-9267_2-9248_4-9269_1-9278_2-9292_2-9294_4-9297_3-9298_2-9303_3-9310_1-9317_1-9329_1-9332_3-9340_1-9353_2-9357_1-9360_1-9364_4-9365_1-101_9-200_9-100_9-181_9-140_9-201_9-120_9-160_9-102_9-103_9&ut=Pro+7+Plus_6.0.1_23_Meizu&ua=500_900_android_6.3.5.10_166&zid=EUAk_80SRqc-4OotI1R1j3LDMtspUHyUMLaN20o6cFyWvE0sj7M_B5_6o9ITABh-BoyamUMQbVlMfiw6G_v4N9d-Z7Gr_vGtDnXHeFYF911Y&uid=_aHViYPD2f0qa-uOgu28a0a6vilau28WYuvT8_ukH88j9WMtp8vnRwraA&cfrom=1022344h&from=1000575v&network=1_0'

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'tiebac.baidu.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.11.0',
            'Cookie': Cookie
        }
        data = 'im_sdk_version=7150036&sign={sign}&sdk_version=4.3.3&timestamp={timestamp}&room_id={room_id}&extRequest=&user_id=1342904541&content_type={content_type}&tpl='.format(
            sign=sign, timestamp=timestamp, room_id=self.roomID, content_type=content_type)

        response = requests.post(url, headers=headers, data=data)
        if 'mix_zan' == content_type:
            print('账号正在进行直播间弹幕点赞')
            time.sleep(1)
            print('>' * 40)
            # print('\n')
        elif 'mix_share' == content_type:
            print('账号正在进行直播间弹幕分享')
            time.sleep(1)
            print('>' * 40)
            # print('\n')
        elif 'mix_follow_anchor' == content_type:
            print('账号正在进行直播间弹幕关注')
            time.sleep(1)
            print('>' * 40)
            # print('\n')
        # print(response.text)
        if response.status_code == 200:

            if 'success' in response.text:
                print('弹幕发送成功！')
                print('>' * 40)
                # print('\n')
            else:
                print('弹幕发送失败！')
                # print('>'*40)

    # 点赞延迟间隔
    def zan_delay(self):
        delay1 = int(self.zanFirst)
        delay2 = int(self.zanLast)
        random_time = random.randint(delay1, delay2)
        print('关注点赞的延迟间隔为：', random_time)
        print('\n')
        # self.time_sleep(random_time)
        time.sleep(random_time)

    # 分享延迟间隔
    def share_delay(self):
        delay1 = int(self.shareFirst)
        delay2 = int(self.shareLast)
        random_time = random.randint(delay1, delay2)
        # time.sleep(random_time)
        print('关注分享的延迟间隔为：', random_time)
        print('\n')
        # self.time_sleep(random_time)
        time.sleep(random_time)

    # 关注延迟间隔
    def follow_delay(self):
        delay1 = int(self.followFirst)
        delay2 = int(self.followLast)
        random_time = random.randint(delay1, delay2)
        # time.sleep(random_time)
        print('关注延迟的延迟间隔为：', random_time)
        print('\n')
        # self.time_sleep(random_time)
        time.sleep(random_time)

    # 彩蛋发送选择
    def send_caidan(self):
        # 获取开启彩蛋的数据
        # print(self.zan,self.share,self.follow)
        # print('\n')
        print('>' * 45)
        # print(caidan)
        if self.zan == 'True' and self.share == 'True' and self.follow == 'True':
            print('点赞、分享、关注开启')
            print('>' * 45)
            print('\n')
            threads1 = [Thread(target=self.zan_pack_msg), Thread(target=self.share_pack_msg),
                        Thread(target=self.follow_pack_msg)]
            for thread1 in threads1:
                thread1.start()
                thread1.join()


        elif self.zan == 'True' and self.share == 'True' and self.follow != 'True':
            print('点赞、分享开启')
            print('>' * 45)
            print('\n')
            threads2 = [Thread(target=self.zan_pack_msg), Thread(target=self.share_pack_msg)]
            for thread2 in threads2:
                thread2.start()
                thread2.join()


        elif self.zan == 'True' and self.share != 'True' and self.follow == 'True':
            print('点赞、关注开启')
            print('>' * 45)
            print('\n')
            threads3 = [Thread(target=self.zan_pack_msg), Thread(target=self.follow_pack_msg)]
            for thread3 in threads3:
                thread3.start()
                thread3.join()


        elif self.zan != 'True' and self.share == 'True' and self.follow == 'True':
            print('分享、关注开启')
            print('>' * 45)
            print('\n')
            threads4 = [Thread(target=self.share_pack_msg), Thread(target=self.follow_pack_msg)]
            for thread4 in threads4:
                thread4.start()
                thread4.join()


        elif self.zan != 'True' and self.share != 'True' and self.follow == 'True':
            print('关注开启')
            print('>' * 45)
            print('\n')
            thread5 = Thread(target=self.follow_pack_msg)
            thread5.start()
            thread5.join()


        elif self.zan == 'True' and self.share != 'True' and self.follow != 'True':
            print('点赞开启')
            print('>' * 45)
            print('\n')
            thread6 = Thread(target=self.zan_pack_msg)
            thread6.start()
            thread6.join()


        elif self.zan != 'True' and self.share == 'True' and self.follow != 'True':
            print('分享开启')
            print('>' * 45)
            print('\n')
            thread7 = Thread(target=self.share_pack_msg)
            thread7.start()
            thread7.join()

        else:
            print('不开启')
            print('对不起您没有选择彩蛋功能，请停止发送彩蛋！')
            print('>' * 45)
            print('\n')

    # 无线循环
    def sendRun(self):

        while True:
            self.send_caidan()


if __name__ == '__main__':
    #获取运行pid进程
    get_pid = os.getpid()
    print(f'程序pid:{get_pid}')
    with open('.ini/SendEggshellPID.ini','w',encoding='utf-8')as p:
        p.write(f'{get_pid}')
        p.close()

    if os.path.isfile('.ini/Eggshell.ini') == True:
        with open('.ini/Eggshell.ini', 'r', encoding='utf-8')as f:

            data = f.readlines()
            # print(data)
            zan = data[0].strip()
            zanFirst = data[1].strip()
            zanLast = data[2].strip()
            share = data[3].strip()
            shareFirst = data[4].strip()
            shareLast = data[5].strip()
            follow = data[6].strip()
            followFirst = data[7].strip()
            followLast = data[8].strip()
            roomID = data[9].strip()
            ckPath = data[10].strip()
        print('=' * 45)
        print('欢迎使用百度直播弹幕助手>>>>----彩蛋功能')
        print('=' * 45)
        time.sleep(1)
        Eggshell = Eggshell(zan, zanFirst, zanLast, share, shareFirst, shareLast, follow, followFirst, followLast,
                            roomID, ckPath)

        Eggshell.sendRun()
        sys.exit()

    else:
        messagebox.showinfo("提示", "请打开主程序后在使用！")
        sys.exit()
