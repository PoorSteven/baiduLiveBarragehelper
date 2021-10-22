# -*- coding: utf-8 -*-
# @Time : 2021-04-15 3:11
# @Author : Steven
# @QQ : 2621228281
# @Email : 2621228281@qq.com
# @File : BaiduOnlineDemo.py
# @Software: PyCharm
import time
import requests


CK_lists = open('CK.txt','r').readlines()

for ck in CK_lists:



    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': ck.strip(),
        'Host': 'live.baidu.com',
        'Referer': 'https://live.baidu.com/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }

    url = 'https://live.baidu.com/m/media/pclive/pchome/live.html?room_id=4356092290'

    response = requests.get(url,headers=headers,verify=False)

    print(response.text)

