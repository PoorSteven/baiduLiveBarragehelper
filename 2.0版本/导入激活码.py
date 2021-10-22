# -*- coding: utf-8 -*-
# @Time : 2020/11/16 2:44
# @Author : Steven
# @QQ : 2621228281
# @Email : 2621228281@qq.com
# @File : 导入激活码.py
# @Software: PyCharm

import pymysql
import time
import uuid
import pymysql
import datetime

now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 获取本地mac地址
def get_mac_address():
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])

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

jihuoma_listv = open('激活码年卡.txt','r',encoding='utf-8').readlines()

local_cdkey = open('LiveSetting.ini','r',encoding='utf-8').readlines()[2].replace('CDkey:','')

def daoru_cdkey():

    for jihuoma in jihuoma_listv:
        cdkey = jihuoma.strip('\n')
        # 插入数据库
        sql = "INSERT INTO BaiduMacYear (cdkey) VALUE ('{jihuoma}')".format(jihuoma=cdkey)
        try:
            cursor.execute(sql)
            con.commit()
            print('>>>数据入库成功！')
        except:
            con.rollback()

# 检测本地激活码
def Detection_cdkey():

    local_cdkey = open('LiveSetting.ini', 'r', encoding='utf-8').readlines()[2].replace('CDkey:', '').strip('\n')
    # 判断本地是否存在激活码
    if len(local_cdkey) == 55 :

        cursor.execute('SELECT COUNT(cdkey),mac from BaiduMacForever WHERE cdkey = "{local_cdkey}"'.format(local_cdkey=local_cdkey))
        result = cursor.fetchone()
        # print(type(result[0]))
        #新激活码写入Mac地址和激活时间
        if result[0] == 1 and  result[1] == None:
            print('激活码本地正常')
            print(now_time)
            print(get_mac_address())
            #判断Mac地址是否存在
            #Mac地址写入数据库，时间写入数据库
            sql = 'UPDATE BaiduMacForever SET mac="{mac}",datetime="{datetime}" WHERE cdkey = "{local_cdkey}"'.format(mac=get_mac_address(),datetime=now_time, local_cdkey=local_cdkey)

            try:
                cursor.execute(sql)
                con.commit()
                print('>>>数据入库成功！')

            except:
                print('>>>数据入库失败！')
                con.rollback()
        #程序激活码Mac地址正确时，运行程序
        elif result[0] == 1 and  result[1] == get_mac_address() :
            print('激活码已被激活')
            print('程序运行')

        elif result[1] != get_mac_address() :
            print('激活码已被锁定')

        else:
            print('激活码错误！')

    elif 0 < len(local_cdkey) < 55 or len(local_cdkey) > 55 :
        print('本地激活码错误！')
        
    else:
        print('本地没有激活码！')

#增加一天时间
def sql_fail_time():
    today = datetime.datetime.now()
    #当前时间增加一天
    offset = datetime.timedelta(days=30)
    re_date = (today + offset).strftime('%Y-%m-%d %H:%M:%S')
    return re_date

demo_time = '2020-12-18 17:17:18'
#
# print(demo_time > sql_fail_time())
# 
# if demo_time > sql_fail_time():
#     print('激活码失效')
# else:
#     print('激活码可用')
def time_stamp(time_data):
    timeArray = time.strptime(time_data, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp



print(type(time_stamp(demo_time)))


date_time = sql_fail_time() 
# print(date_time)
