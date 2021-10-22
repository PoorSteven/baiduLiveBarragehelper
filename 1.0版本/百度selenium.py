# coding:utf-8
import random,time,warnings,os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tkinter import Tk
from tkinter import messagebox
root = Tk()
root.withdraw() #****实现主窗口隐藏

lujin_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

def choice_cookie():
    suiji_cookies = cookies_list[random.randint(0,len(cookies_list)-1)]
    return eval(suiji_cookies)

def baidu_pinlun(cookies,text,zhibo_url):
    warnings.simplefilter('ignore', DeprecationWarning)
    chrome_options = Options()
    # 设置chrome浏览器无界面模式
    chrome_options.add_argument('--headless') # 无头
    chrome_options.add_argument("--mute-audio")  # 静音
    path = r'chromedriver.exe'
    driver = webdriver.Chrome(executable_path=path,chrome_options=chrome_options)
    # driver.maximize_window()
    driver.set_window_size(1920, 1080)
    driver.get(zhibo_url)
    title = driver.find_element_by_xpath('//*[@id="app-pc"]/div/div[1]/div[1]/div[1]/span[1]').text
    print('======================================================================')
    print('当前直播间标题：' + title)
    print('======================================================================')
    name = driver.find_element_by_xpath('//*[@id="app-pc"]/div/div[1]/div[1]/div[2]/span').text
    print('当前直播间的作者为：'+name)
    print('======================================================================')
    driver.delete_all_cookies()#清楚cookies
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(1)
    driver.get(zhibo_url)
    driver.find_element_by_xpath('//*[@id="app-pc"]/div/div/div[2]/div/div[3]/div/input').send_keys(text)#利用Xptah获取输入框定位地址
    time.sleep(1)
    print('======================================================================')
    print('当前评论广告语：' + text)
    print('======================================================================')
    driver.find_element_by_xpath('//*[@id="app-pc"]/div/div/div[2]/div/div[3]/button').click()#点击按钮
    time.sleep(1)
    driver.quit()


if __name__ == '__main__':
    text_list = '直播打卡'
    cookies_list = [{'domain': '.baidu.com', 'expiry': 4196684721, 'httpOnly': False, 'name': 'MBD_AT', 'path': '/',
                     'secure': False, 'value': '0'},
                    {'domain': '.mbd.baidu.com', 'httpOnly': False, 'name': 'x-logic-no', 'path': '/', 'secure': False,
                     'value': '2'},
                    {'domain': '.baidu.com', 'expiry': 1636220699, 'httpOnly': False, 'name': 'BAIDUID', 'path': '/',
                     'secure': False, 'value': 'CB5EB62A391B8FEF05D4DEC7DB76243B:FG=1'},
                    {'domain': '.baidu.com', 'expiry': 1863884720, 'httpOnly': True, 'name': 'BDUSS', 'path': '/',
                     'secure': False,
                     'value': 'hDfndDVHVyd2xXZWt0cUVmT09ZS3JLODVHMnl0UC1NdEVwVWxiZ0J1bXNHTTFmSUFBQUFBJCQAAAAAAAAAAAEAAADJoIhZa2R1enl1YW41OTkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKyLpV-si6Vfaz'},
                    {'domain': 'mbd.baidu.com', 'expiry': 1636220699, 'httpOnly': False, 'name': 'userDeviceId',
                     'path': '/', 'secure': False, 'value': 'xoULtR1604684696'}]

    jihuoma = open(lujin_path+r'\\激活码.txt', 'r').readline()
    shiyongma = 'SUYHjo9CVy3smf4iF7kXzDulnhrMb2621228281'

    if shiyongma == jihuoma:
        print('               ***欢迎使用Steven开发的百度直播评论小脚本！***\n' + '使用之前首先安装最新谷歌浏览器，版本为 86.0.4240.183（正式版本），不然无法成功运行该程序\n' + '如有疑问请联系Steven QQ：2621228281')
        zhibo_url = open(lujin_path+r'\\直播间评论设置.txt', 'r', encoding='utf-8').readlines()[0].replace('地址：', '')
        yanchi = int(open(lujin_path+r'\\直播间评论设置.txt', 'r', encoding='utf-8').readlines()[1].replace('延迟：', ''))
        mun = 0
        while mun <= 5:

            text_list  = text_list.strip('\n')
            cookies = cookies_list
            try:
                baidu_pinlun(cookies, text_list, zhibo_url)
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                print('广告发送成功！！！！！')
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                print('\n')
                time.sleep(yanchi)
            except:
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                print('广告发送失败！！！！！')
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                print('\n')
            mun += 1

    else:
        # print('请联系Steven QQ：2621228281 购买激活码')
        ##提示信息框
        messagebox.showinfo("提示", "欢迎使用百度直播弹幕评论试用版！该版本仅供测试使用，只为确保您的电脑可以正常运行本软件，并可以成功发布广告弹幕或者人气弹幕！")
        messagebox.showinfo("提示", "使用软件之前首先安装文件夹中谷歌浏览器，版本为 86.0.4240.183")
        messagebox.showinfo("提示", "无限制版本请联系Steven QQ：2621228281 购买激活码！")
        with open(lujin_path+r'\\激活码.txt','a',encoding='utf-8') as f:
            f.write(shiyongma)
            f.close()
