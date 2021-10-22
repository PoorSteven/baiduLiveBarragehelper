# -*- coding: utf-8 -*-
# @Time : 2021-03-12 15:47
# @Author : Steven
# @QQ : 2621228281
# @Email : 2621228281@qq.com
# @File : 百度点赞分享关注弹幕.py
# @Software: PyCharm
import re
import requests
import time
import random
import hashlib

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

#点赞分享关注弹幕类型
def Content_type():
    list = ['mix_zan','mix_share','mix_follow_anchor']
    choice = random.choice(list)
    # print(choice)
    return choice

#获取时间戳
def get_time():
    shijiancuo = int(time.time()*1000)

    return str(shijiancuo)

#获取随机cookieS
def get_choice_cookies(cookies_list):
    cookies = cookies_list[random.randint(0,len(cookies_list)-1)].strip('\n')
    # print(cookies)
    return cookies

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
    else:
        print('弹幕发送失败！')

if __name__ == '__main__':
    room_id = open('LiveSetting.ini','r',encoding='utf-8').readlines()[0].replace('RoomID：','').strip()
    Delay = open('LiveSetting.ini','r',encoding='utf-8').readlines()[1].replace('Delay：','').strip()
    Cookies_list = open('CK.txt', 'r', encoding='utf-8').readlines()
    print(room_id)
    while True:
        Cookie = get_choice_cookies(Cookies_list)
        content_type = Content_type()
        timestamp = get_time()
        sign = str_MD5(content_type, room_id, timestamp)

        if (int(timestamp) % 2) == 0:

            request_msg(Cookie, sign, room_id,timestamp,content_type)
        print('▶▶▶:进入延迟倒计时，请耐心等待！！！')
        print('\n')
        time.sleep(int(Delay))

    python3: input("please input any key to exit!")





















