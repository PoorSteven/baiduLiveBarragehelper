# coding:utf-8
import random,time,warnings,os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tkinter as tk
from tkinter import messagebox
import uuid
import pymysql

root = tk.Tk()
root.withdraw() #****实现主窗口隐藏

lujin_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

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

def choice_cookie(cookies_list):
    suiji_cookies = cookies_list[random.randint(0,len(cookies_list)-1)]
    return eval(suiji_cookies)

def baidu_pinlun(cookies,text,zhibo_url):
    warnings.simplefilter('ignore', DeprecationWarning)
    chrome_options = Options()
    # 设置chrome浏览器无界面模式
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--mute-audio")  # 静音
    path = r'chromedriver.exe'
    driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
    driver.set_window_size(1920, 1080)
    # driver.maximize_window()
    driver.get(zhibo_url)
    time.sleep(1)
    title = driver.find_element_by_xpath('//*[@id="app-pc"]/div/div[1]/div[1]/div[1]/span[1]').text
    print('======================================================================')
    print('☛当前直播间标题：' + title)
    print('======================================================================')
    name = driver.find_element_by_xpath('//*[@id="app-pc"]/div/div[1]/div[1]/div[2]/span').text
    print('☛当前直播间的作者为：'+name)
    print('======================================================================')
    time.sleep(1)
    driver.delete_all_cookies()#清楚cookies
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get(zhibo_url)
    time.sleep(2)
    # print(driver.get_cookies())
    driver.find_element_by_xpath('//*[@id="app-pc"]/div/div/div[2]/div/div[3]/div/input').send_keys(text)#利用Xptah获取输入框定位地址
    time.sleep(1)
    print('======================================================================')
    print('☛当前评论广告语：' + text)
    print('======================================================================')
    driver.find_element_by_xpath('//*[@id="app-pc"]/div/div/div[2]/div/div[3]/button').click()#点击按钮
    time.sleep(1)
    driver.quit()

#获取所有激活码列表
def get_all_jihuoma():
    jihuoma_list = []
    cursor.execute('SELECT jihuoma from baidumac')
    results = cursor.fetchall()
    # print(results)
    for row in results:
        jihuoma = row[0]
        jihuoma_list.append(jihuoma)
    return jihuoma_list

def run_baidu_pinlun(cookies_list,text_list):
    print(
        '                  ***欢迎使用Steven开发的百度直播评论小脚本！***\n\n' + '使用之前首先安装最新谷歌浏览器，版本为 86.0.4240.111（正式版本），不然无法成功运行该程序\n' + '运行之前请先设置广告语和直播间评论设置，广告语一行一个，直播间评论第一行为直播间地址，第二行为评论延迟时间！\n' + '如有疑问请联系Steven QQ：2621228281\n')
    time.sleep(1)
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
    while True:
        # print('循环开始')
        for text in text_list:
            text = text.strip('\n')
            cookies = choice_cookie(cookies_list)
            try:
                # cookies = choice_cookie(cookies_list)
                baidu_pinlun(cookies, text, zhibo_url)
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                print('☺广告发送成功！！！！！')
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                print('\n')
                time.sleep(yanchi)
            except:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                print('☹广告发送失败！！！！！')
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                print('\n')

if __name__ == '__main__':
    text_list = open(lujin_path+r'\\广告语.txt', encoding='utf-8').readlines()
    cookies_list = open(lujin_path+r'\\CK.txt', encoding='utf-8').readlines()

    jihuoma = open(lujin_path+r'\\激活码.txt', 'r').readline()
    zhibo_url = open(lujin_path+r'\\直播间评论设置.txt', 'r', encoding='utf-8').readlines()[0].replace('地址：', '')
    yanchi = int(open(lujin_path+r'\\直播间评论设置.txt', 'r', encoding='utf-8').readlines()[1].replace('延迟：', ''))
    jihuoma_list = get_all_jihuoma()
    mac = get_mac_address()

    # 判断本地是否存在激活码
    if jihuoma in jihuoma_list:
        # 判断激活码中是否存mac信息，如果没有添加，如果有直接激活码已经绑定
        cursor.execute('SELECT mac FROM baidumac WHERE jihuoma = "{jihuoma}"'.format(jihuoma=jihuoma))
        result = cursor.fetchall()
        for row in result:
            if row[0] == None or row[0] == '':
                # 如果没有mac数据，插入数据库
                sql = 'UPDATE baidumac SET mac="{mac}" WHERE jihuoma = "{jihuoma}"'.format(mac=mac, jihuoma=jihuoma)
                try:
                    cursor.execute(sql)
                    con.commit()
                    run_baidu_pinlun(cookies_list,text_list)
                except:
                    con.rollback()

            elif row[0] == mac:
                run_baidu_pinlun(cookies_list,text_list)

            else:
                messagebox.showinfo("提示","该激活码以绑定其他电脑，激活码重复使用已记录，记录三次后，自动删除激活码协议，请勿在其他电脑上使用该激活码！")
    else:
        ##提示信息框
        messagebox.showinfo("提示","您的软件还未激活")
        messagebox.showinfo("提示","请联系Steven QQ：2621228281 购买激活码！")
