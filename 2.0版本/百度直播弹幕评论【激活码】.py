# -*- coding: utf-8 -*-
# @Time : 2020/11/15 22:15
# @Author : Steven
# @QQ : 2621228281
# @Email : 2621228281@qq.com
# @File : 百度直播弹幕评论.py
# @Software: PyCharm

import requests
import time
import datetime
import os
import json
import uuid
import re
import random
import pymysql
import tkinter as tk
from tkinter import messagebox
import uuid
import hashlib

lujin_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

root = tk.Tk()
root.withdraw() #****实现主窗口隐藏

#连接MySQL数据库
con = pymysql.connect(
    host = '121.42.229.227',
    db = 'baidumac',
    user = 'baidumac',
    passwd = 'h940834918',
    port = 3306,
    charset = 'utf8'
)
#获取游标
cursor = con.cursor()

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Host': 'mbd.baidu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4321.2 Safari/537.36'
}

#点赞分享关注弹幕类型
def Content_type():
    list = ['mix_zan','mix_share','mix_follow_anchor']
    choice = random.choice(list)
    # print(choice)
    return choice

#获取signmd5值
def str_MD5(content_type,room_id,timestamp):
    str = 'appname=haokancfrom=1022344hcontent_type={content_type}extRequest=from=1000575vim_sdk_version=7150036network=1_0room_id={room_id}sdk_version=4.3.3sid=8676_1-8915_3-8941_2-9040_1-9076_1-9088_1-9092_3-9100_1-9106_1-9108_1-9126_2-9128_1-9146_1-9149_2-9151_1-9153_2-9176_2-9185_2-9193_2-9201_2-9207_3-9224_1-9231_1-9235_2-9247_3-9251_1-9267_2-9248_4-9269_1-9278_2-9292_2-9294_4-9297_3-9298_2-9303_3-9310_1-9317_1-9329_1-9332_3-9340_1-9353_2-9357_1-9360_1-9364_4-9365_1-101_9-200_9-100_9-181_9-140_9-201_9-120_9-160_9-102_9-103_9timestamp={timestamp}tpl=ua=500_900_android_6.3.5.10_166uid=_aHViYPD2f0qa-uOgu28a0a6vilau28WYuvT8_ukH88j9WMtp8vnRwraAuser_id=1342904541ut=Pro 7 Plus_6.0.1_23_Meizuzid=EUAk_80SRqc-4OotI1R1j3LDMtspUHyUMLaN20o6cFyWvE0sj7M_B5_6o9ITABh-BoyamUMQbVlMfiw6G_v4N9d-Z7Gr_vGtDnXHeFYF911Ytiebaclient!!!'.format(content_type=content_type,room_id=room_id,timestamp=timestamp)
    # print(str)
    #创建Md5对象
    create_md5 = hashlib.md5()
    create_md5.update(str.encode(encoding='utf-8'))
    result = create_md5.hexdigest().upper()
    # print(result)
    return result

#获取当前时间
def get_now_time():
    a = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    return a

# 获取本地mac地址
def get_mac_address():
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])

#广告发送请求
def get_resquests(headers,room_id,text):

    live_url = 'http://mbd.baidu.com/searchbox?cmd=366&action=liveshow&service=bdbox&osname=baiduboxapp&data=%7B%22data%22%3A%7B%22roomid%22%3A%22'+room_id+'%22%2C%22device_id%22%3A%22'+str(ran_tag_str(16))+'%22%2C%22source_type%22%3A1%2C%22text%22%3A%22'+text+'%22%2C%22timestamp%22%3A'+str(int(get_time()))+'%7D%7D'

    data = {
        'cmd': '366',
        'action': 'liveshow',
        'service': 'bdbox',
        'osname': 'baiduboxapp',
        'data': '{"data":{"roomid":"'+room_id+'","device_id":"","source_type":1,"text":"'+text+'","timestamp":'+str(int(get_time()))+'}}',
    }

    response = requests.post(live_url,headers=headers,data=data)
    results = json.loads(response.text)
    # print(results)
    if results["errno"] == '0' :
        time.sleep(1)
        print('当前广告语为：' + text)
        print('==============================================================')
        time.sleep(1)
        print('>>>>>>>>>>>>>>>>>>>>>>广告发送成功！>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print('==============================================================')

        print('\n')
        time.sleep(random.randint(0,2))
        if (int(get_time()) % 2) == 0:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            print('※※※※※※※※※※※   彩蛋功能展现   ※※※※※※※※※※※')
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            pack_msg()

    # else:
    #     print('==============================================================')
    #     print('>>>>>>>>>>>>>>>>>>>>>>广告发送失败！>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    #     print('==============================================================')
    #     print('\n')

#随机ID
def ran_tag_str(num):
    #随机变量
    suiji = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    salt = ''
    for i in range(num):
        i = random.choice(suiji)
        salt += i
    return salt

#房间信息获取
def get_web_information(room_id,headers):

    information_url = 'http://mbd.baidu.com/searchbox?cmd=149&action=star&service=bdbox&osname=baiduboxapp&data={%22room_id%22:%22'+room_id+'%22,%22device_id%22:%22'+str(ran_tag_str(16))+'%22,%22source_type%22:1,%22source_from_type%22:1,%22_%22:'+str(int(get_time()))+'}&_='+str(int(get_time()*1000))+'&callback=__jsonp_callback_0__'

    # print(information_url)
    information = requests.get(information_url,headers=headers)
    title = re.findall(r'"title":"(.*?)",', information.text)[0]
    name = re.findall(r'name":"(.*?)",', information.text)[0]
    #nick_name = re.findall(r'nick_name":"(.*?)",', information.text)[1]
    online_users = re.findall(r'"real_online_users":"(.*?)",', information.text)[0]
    print('▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼')
    print('当前直播间标题：'+title.encode('utf8').decode('unicode_escape'))
    print('=============================================================')
    time.sleep(1)
    print('当前直播间作者：'+name.encode('utf8').decode('unicode_escape')+'   ▎▎ '+'当前真实在线人数为： ' + online_users.encode('utf8').decode('unicode_escape'))
    print('==============================================================')
    time.sleep(1)
    # print('当前小号名称为：' + nick_name.encode('utf8').decode('unicode_escape'))
    # print('==============================================================')

#开头广告
def get_ads():
    print(
        '                       ***欢迎使用全新Steven百度直播弹幕小助手2.0！***\n\n' + '运行之前请先设置广告语和直播间评论设置，\n\n广告语一行一个，直播间评论第一行为直播间地址ID，第二行为评论延迟时间！\n\n' + '名称为：【 LiveSetting.ini 】的ini配置文件为直播间配置文件\n\n' + '名称为：【ADS.txt】的为广告语\n\n' + '名称为：【 CK.txt 】的为CK业务号\n\n' + '如有疑问请联系Steven QQ：2621228281\n')
    time.sleep(5)
    print('※※※※※ 软件即将开始运行 ※※※※※')
    print('▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼')
    print('√ 广告语是否设置完成？')
    print('√ 直播间地址是否设置完成？')
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

#增加一天时间
def sql_fail_time():
    today = datetime.datetime.now()
    #当前时间增加一天
    offset = datetime.timedelta(days=120)
    re_date = (today + offset).strftime('%Y-%m-%d %H:%M:%S')
    return re_date

#时间戳对比时间
def time_stamp(time_data):
    timeArray = time.strptime(time_data, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


# 检测本地激活码
def Detection_cdkey():
    local_cdkey = open(lujin_path+'\\LiveSetting.ini', 'r', encoding='utf-8').readlines()[2].replace('CDkey：', '').strip('\n')
    # print(local_cdkey)
    # 判断本地是否存在激活码
    if len(local_cdkey) == 55:

        cursor.execute('SELECT COUNT(cdkey),mac,failtime from BaiduMacQuerter WHERE cdkey = "{local_cdkey}"'.format(
            local_cdkey=local_cdkey))
        result = cursor.fetchone()
        # 新激活码写入Mac地址和激活时间
        if result[0] == 1 and result[1] == None:
            # 判断Mac地址是否存在
            # Mac地址写入数据库，时间写入数据库
            sql = 'UPDATE BaiduMacQuerter SET mac="{mac}",datetime="{datetime}",failtime="{failtime}" WHERE cdkey = "{local_cdkey}"'.format(
                mac=get_mac_address(), datetime=get_now_time(), failtime=sql_fail_time(), local_cdkey=local_cdkey)

            try:
                cursor.execute(sql)
                con.commit()
                # print('>>>数据入库成功！')
                run_baidu_comment()

            except:
                print('>>>无法连接服务器，确认网络是否正常！')

                con.rollback()
        # 程序激活码Mac地址正确时，运行程序
        elif result[0] == 1 and result[1] == get_mac_address() and time_stamp(get_now_time()) < time_stamp(result[2]):
            run_baidu_comment()

        elif result[1] != None and result[1] != get_mac_address():
            messagebox.showinfo("提示", "该激活码以绑定其他电脑，激活码重复使用已记录，记录三次后，自动删除激活码协议，请勿在其他电脑上使用该激活码！")

        elif time_stamp(get_now_time()) > time_stamp(result[2]) :
            messagebox.showinfo("提示", "激活码使用到期！购买激活码请联系Steven QQ：2621228281")
        else:
            messagebox.showinfo("提示", "激活码错误，请核对后再进行输入！购买激活码请联系Steven QQ：2621228281")


    elif 1 < len(local_cdkey) < 55 or len(local_cdkey) > 55:
        messagebox.showinfo("提示", "本地激活码错误，请核对后再进行输入！如未购买激活码请联系Steven QQ：2621228281")
        # print('本地激活码错误！')

    else:
        messagebox.showinfo("提示", "本地没有激活码，请购买请激活码后重新打开程序！购买联系Steven QQ：2621228281")
        # print('本地没有激活码！')

def run_baidu_comment():
    get_ads()
    while True :
        for ads in ADS_list:
            ads = ads.strip('\n')
            try:
                headers['Cookie'] = get_choice_cookies(cookies_list)
                # 获取直播间信息，作者和标题等！
                get_web_information(room_id,headers)
                #广告发送请求
                get_resquests(headers,room_id,ads)
                print('▶▶▶:进入延迟倒计时，请耐心等待！！！')
                print('\n')
                time.sleep(int(dalay))
            except :
                print('==============================================================')
                print('>>>>>>>>>>>>>>>>>>>>>>广告发送失败！！>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                print('==============================================================')
                print('\n')

#弹幕分享点赞转发
def request_msg(Cookie,sign,room_id,timestamp,content_type):

    url = 'http://tiebac.baidu.com/bdlive/msg/sendOperationMsg?appname=haokan&sid=8676_1-8915_3-8941_2-9040_1-9076_1-9088_1-9092_3-9100_1-9106_1-9108_1-9126_2-9128_1-9146_1-9149_2-9151_1-9153_2-9176_2-9185_2-9193_2-9201_2-9207_3-9224_1-9231_1-9235_2-9247_3-9251_1-9267_2-9248_4-9269_1-9278_2-9292_2-9294_4-9297_3-9298_2-9303_3-9310_1-9317_1-9329_1-9332_3-9340_1-9353_2-9357_1-9360_1-9364_4-9365_1-101_9-200_9-100_9-181_9-140_9-201_9-120_9-160_9-102_9-103_9&ut=Pro+7+Plus_6.0.1_23_Meizu&ua=500_900_android_6.3.5.10_166&zid=EUAk_80SRqc-4OotI1R1j3LDMtspUHyUMLaN20o6cFyWvE0sj7M_B5_6o9ITABh-BoyamUMQbVlMfiw6G_v4N9d-Z7Gr_vGtDnXHeFYF911Y&uid=_aHViYPD2f0qa-uOgu28a0a6vilau28WYuvT8_ukH88j9WMtp8vnRwraA&cfrom=1022344h&from=1000575v&network=1_0'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'tiebac.baidu.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.11.0',
        'Cookie' : Cookie
    }
    data = 'im_sdk_version=7150036&sign={sign}&sdk_version=4.3.3&timestamp={timestamp}&room_id={room_id}&extRequest=&user_id=1342904541&content_type={content_type}&tpl='.format(sign=sign,timestamp=timestamp,room_id=room_id,content_type=content_type)

    response = requests.post(url,headers=headers,data=data)
    if 'mix_zan' == content_type:
        print('账号正在进行直播间弹幕点赞')
        time.sleep(1)
        print('>>>>>>>>>>>>>>>>>>>>>>')
    elif 'mix_share' == content_type:
        print('账号正在进行直播间弹幕分享')
        time.sleep(1)
        print('>>>>>>>>>>>>>>>>>>>>>>')
    elif 'mix_follow_anchor' == content_type:
        print('账号正在进行直播间弹幕关注')
        time.sleep(1)
        print('>>>>>>>>>>>>>>>>>>>>>>')
    # print(response.text)
    if 'success' in response.text:
        print('弹幕发送成功！')
        print('>>>>>>>>>>>>>>>>>>>>>>')
    else:
        print('弹幕发送失败！')
        print('>>>>>>>>>>>>>>>>>>>>>>')

#封装弹幕分享点赞转发
def pack_msg():
    Cookie = get_choice_cookies(cookies_list)
    content_type = Content_type()
    timestamp = str(int(get_time()*1000))
    sign = str_MD5(content_type, room_id, timestamp)
    request_msg(Cookie, sign, room_id, timestamp, content_type)

if __name__ == '__main__':
    ADS_list = open(lujin_path+'\\ADS.txt', 'r', encoding='utf-8').readlines()
    room_id = open(lujin_path+'\\LiveSetting.ini', 'r', encoding='utf-8').readlines()[0].replace('RoomID：', '').strip()
    # print(room_id)
    dalay = open(lujin_path+'\\LiveSetting.ini', 'r', encoding='utf-8').readlines()[1].replace('Delay：', '')
    cookies_list = open(lujin_path+'\\CK.txt', 'r', encoding='utf-8').readlines()

    # pack_msg()
    #检测激活码后运行程序
    Detection_cdkey()
    python3: input("please input any key to exit!")