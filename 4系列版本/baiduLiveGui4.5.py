# -*- coding: utf-8 -*-
# @Time : 2021-04-15 17:12
# @Author : Steven
# @QQ : 2621228281
# @Email : 2621228281@qq.com
# @File : baiduLiveGui.py
# @Software: PyCharm
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIcon
from threading import Thread
import baiduLiveUi
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

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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



#UI主线程
class BaiduLive(QMainWindow):
    #初始化
    def __init__(self):
        super(BaiduLive, self).__init__()
        # 导入百度GUi界面设置icon图标
        # 初始化UI
        self.initUI()
        #窗口居中
        self.center()

        # 载入配置
        self.load_setting()
        #保存配置事件绑定
        self.ui.saveButton.clicked.connect(self.get_saveButton_click)
        #ck 导入绑定
        self.ui.ckButton.clicked.connect(self.ck_import)
        #ck 列表清除
        self.ui.ckClearButton.clicked.connect(self.ck_clear)
        #ads 导入绑定
        self.ui.adsButton.clicked.connect(self.ads_import)
        #ads 列表清除
        self.ui.adsClearButton.clicked.connect(self.ads_clear)
        #single 导入绑定
        self.ui.singleButton.clicked.connect(self.single_import)
        #single 清空
        self.ui.singleClearButton.clicked.connect(self.single_clear)
        #single_line 清空
        self.ui.oneClearButton.clicked.connect(self.single_line_Clear)
        #single_line 清空
        self.ui.oneClearButton_2.clicked.connect(self.single_line_Clear2)
        #single_line 清空
        self.ui.oneClearButton_3.clicked.connect(self.single_line_Clear3)
        #链接直播间点击按钮绑定
        self.ui.liveUrlbutton.clicked.connect(self.link_live_click)
        #登陆直播点击按钮绑定
        self.ui.loginButton.clicked.connect(self.onlineThread)
        self.ui.loginNumButton.clicked.connect(self.loginNum_thead)

        #发送弹幕评论 事件绑定
        self.ui.sendButton.clicked.connect(self.get_sendButton_click)
        #停止弹幕评论 事件绑定
        self.ui.stopButton.clicked.connect(self.stopButton_thread)

        #彩蛋发送 事件绑定
        self.ui.sendCaidan.clicked.connect(self.get_sendCaidan_click)
        #彩蛋停止  事件绑定
        self.ui.stopCaidan.clicked.connect(self.stopCaidan_thread)

        #即时弹幕发送
        self.ui.instantSendButon.clicked.connect(self.instant_send)
        #即时弹幕停止
        self.ui.instantStopButton.clicked.connect(self.instant_stop)

        #绑定随机选择一个CK
        self.ui.choiceCKButton.clicked.connect(self.get_ck_name)
        #绑定随机选择一个CK
        self.ui.choiceCKButton_2.clicked.connect(self.get_ck_name_2)
        #绑定随机选择一个CK
        self.ui.choiceCKButton_3.clicked.connect(self.get_ck_name_3)
        #绑定单账号列表框选中
        self.ui.singleList.doubleClicked.connect(self.pitch_single)

        #绑定onesendbutton
        self.ui.oneSendButton.clicked.connect(self.oneSendButton_click)
        #绑定onesendbutton
        self.ui.oneSendButton_2.clicked.connect(self.oneSendButton_click2)
        #绑定onesendbutton
        self.ui.oneSendButton_3.clicked.connect(self.oneSendButton_click3)


        try:
            self.get_version()
            self.get_announcement()
        except:
            pass


    #UI导入，设置窗口居中
    def initUI(self):

        self.ui = baiduLiveUi.Ui_MainWindow()
        self.ui.setupUi(self)

    # 初始化内容展现
    def get_announcement(self):
        response = requests.get('http://www.pyseoer.com/baidutext.txt')
        text = response.content.decode('utf-8')
        self.printf(text)
        QApplication.processEvents()

    #文本显示输出
    def printf(self,mypstr):
        try:
            self.ui.textBrowser.append(mypstr)  # 在指定的区域显示提示信息
            self.ui.cursor = self.ui.textBrowser.textCursor()
            self.ui.textBrowser.moveCursor(self.ui.cursor.End)  # 光标移到最后，这样就会自动显示出来
            QApplication.processEvents()  # 一定加上这个功能，不然有卡顿
        except:
            self.printf('出现异常！')

    #延迟发送
    def time_sleep(self,delay):
        self.timeThread = timeThread(delay)
        self.printf('进行{}秒延迟发送>>>>'.format(delay))
        self.printf('\n')
        self.timeThread.run()

    # 控制窗口显示在屏幕中心的方法
    def center(self):
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    #保存配置事件
    def get_saveButton_click(self):
        print('保存配置')
        ck_list = self.get_all_ck()
        ads_list = self.get_all_ads()
        single_list = self.get_all_single()
        room_url = self.ui.roomUrl.text()
        ck_path = 'CK.txt'
        ads_path = 'ADS.txt'
        single_path = 'Single.txt'
        cdkey = self.ui.jihuoma.text()
        cdkey_button = self.ui.keyGroup.checkedButton().text()
        # blackbox = self.ui.blackBoxGroup.checkedButton().text()
        if os.path.isfile('CK.txt') == True:
            os.remove('CK.txt')
        if os.path.isfile('ADS.txt') == True:
            os.remove('ADS.txt')
        if os.path.isfile('Single.txt') == True:
            os.remove('Single.txt')

        for ck in ck_list:
            with open(ck_path,'a',encoding='utf-8')as d:
                d.write(ck+'\n')
                d.close()
        for ads in ads_list:
            with open(ads_path,'a',encoding='utf-8')as b:
                b.write(ads+'\n')
                b.close()
        for single in single_list:
            with open(single_path,'a',encoding='utf-8')as b:
                b.write(single+'\n')
                b.close()



        with open('setting.ini','w',encoding='utf-8')as f:
            f.write(
                room_url+'\n'
                +ck_path+'\n'
                +ads_path+'\n'
                +cdkey+'\n'
                +cdkey_button+'\n'
                +single_path

            )
            f.close()
            self.printf('=' * 25)
            self.printf('setting.ini文件生成成功！')
            self.printf('='*25)
            print('保存配置成功!')

    #载入配置
    def load_setting(self):
        print('载入配置')
        if os.path.isfile('setting.ini') == True:
            print('文件存在')

            try:
                with open('setting.ini','r',encoding='utf-8')as f:
                    data = f.readlines()
                    # print(data)
                    ck_path = data[1].strip()
                    ads_path = data[2].strip()
                    room_url = data[0].strip()
                    cdkey = data[3].strip()
                    cdkey_button = data[4].strip()
                    single_path = data[5].strip()


                self.ui.roomUrl.setText(room_url)
                self.ui.jihuoma.setText(cdkey)

                if cdkey_button == '天卡':
                    self.ui.dayButton.setChecked(True)
                elif cdkey_button == '周卡':
                    self.ui.weekButton.setChecked(True)
                elif cdkey_button == '月卡':
                    self.ui.monthButton.setChecked(True)
                elif cdkey_button == '季卡':
                    self.ui.querterButton.setChecked(True)

                with open(ck_path,'r',encoding='utf-8')as ck:
                    #去换行符
                    ck_lists = [x.strip() for x in ck.readlines() if x.strip() != '']
                    self.ui.ckList.addItems(ck_lists)
                    self.ui.ck_num.setText(str(len(ck_lists)))

                with open(ads_path, 'r', encoding='utf-8')as ads:
                    # 去换行符
                    ads_lists = [x.strip() for x in ads.readlines() if x.strip() != '']
                    self.ui.adsList.addItems(ads_lists)
                    self.ui.ads_num.setText(str(len(ads_lists)))

                with open(single_path, 'r', encoding='utf-8')as single:
                    # 去换行符
                    single_lists = [x.strip() for x in single.readlines() if x.strip() != '']
                    self.ui.singleList.addItems(single_lists)
                    self.ui.single_num.setText(str(len(single_lists)))
            except:
                pass

    #软件版本获取
    def get_version(self):
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
        }
        response = requests.get('http://www.pyseoer.com/BaiduLiveVersion.txt',headers=headers)
        online_vsersion = response.text.replace('Version=','')
        local_vserion=self.ui.softVserion.text()
        if online_vsersion != local_vserion:
            self.ui.softVserion.setText('软件有最新版本！！！')
        QApplication.processEvents()

    #导入CK数据到列表
    def ck_import(self):
        try:
            # 选择获取CK路径
            filepath, _ = QFileDialog.getOpenFileName(self, '导入文件', os.path.abspath(os.curdir),'Text Files (*.txt);;All Files (*)')
            with open(filepath,'r',encoding='utf-8')as f:
                #去换行符
                ck_lists = [x.strip() for x in f.readlines() if x.strip() != '']
                #提示CK数量
                QMessageBox.information(self, '操作成功', '一共导入{}个CK账号'.format(len(ck_lists)))

        except:
            # 提示CK数量
            QMessageBox.information(self, '操作失败', '导入CK账号失败！')
            ck_lists = []
        # 导入到列表框中
        self.ui.ckList.clear()
        self.ui.ckList.addItems(ck_lists)
        self.ui.ck_num.setText(str(len(ck_lists)))
        QApplication.processEvents()
        return filepath

    #导入ADS数据到列表
    def ads_import(self):
        try:
            # 选择获取CK路径
            filepath,_ = QFileDialog.getOpenFileName(self,'导入文件',os.path.abspath(os.curdir),'ext Files (*.txt);;All Files (*)')

            with open(filepath,'r',encoding='utf-8')as f:
                #去换行符
                ads_lists = [x.strip() for x in f.readlines() if x.strip() != '']
                #提示CK数量
                QMessageBox.information(self, '操作成功', '一共导入{}个评论语'.format(len(ads_lists)))
        except:
            # 提示ADS数量
            QMessageBox.information(self, '操作失败', '导入ADS账号失败！')
            ads_lists = []
        # 导入到列表框中
        self.ui.adsList.clear()
        self.ui.adsList.addItems(ads_lists)
        self.ui.ads_num.setText(str(len(ads_lists)))
        QApplication.processEvents()
        return filepath

    #导入single单账号评论数据到列表
    def single_import(self):
        try:
            # 选择获取CK路径
            filepath,_ = QFileDialog.getOpenFileName(self,'导入文件',os.path.abspath(os.curdir),'ext Files (*.txt);;All Files (*)')

            with open(filepath,'r',encoding='utf-8')as f:
                #去换行符
                single_lists = [x.strip() for x in f.readlines() if x.strip() != '']
                #提示CK数量
                QMessageBox.information(self, '操作成功', '一共导入{}个评论语'.format(len(single_lists)))
        except:
            # 提示ADS数量
            QMessageBox.information(self, '操作失败', '导入评论失败！')
            single_lists = []
        # 导入到列表框中
        self.ui.singleList.clear()
        self.ui.singleList.addItems(single_lists)
        self.ui.single_num.setText(str(len(single_lists)))
        QApplication.processEvents()
        return filepath

    #single列表框清空
    def single_clear(self):
        self.ui.singleList.clear()
        self.ui.single_num.setText('0')

    #ck列表框清空
    def ck_clear(self):
        self.ui.ckList.clear()
        self.ui.ck_num.setText('0')

    #oneclear single_line 清空
    def single_line_Clear(self):
        self.ui.single_line.setText('')

    #oneclear single_line 清空
    def single_line_Clear2(self):
        self.ui.single_line_2.setText('')

    #oneclear single_line 清空
    def single_line_Clear3(self):
        self.ui.single_line_3.setText('')

    #ads列表框清空
    def ads_clear(self):
        self.ui.adsList.clear()
        self.ui.ads_num.setText('0')

    #获取所有的弹幕评论语
    def get_all_ads(self):
        ads_list = []
        count = self.ui.adsList.count()
        for i in range(count):
            ads_list.append(self.ui.adsList.item(i).text())
        return ads_list

    #获取所有的CK号
    def get_all_ck(self):
        ck_list = []
        count = self.ui.ckList.count()
        for i in range(count):
            ck_list.append(self.ui.ckList.item(i).text())
        return ck_list

    def get_all_single(self):
        single_list = []
        count = self.ui.singleList.count()
        for i in range(count):
            single_list.append(self.ui.singleList.item(i).text())
        return single_list

    # 获取随机cookies
    def get_choice_cookies(self):
        cookies_list = []
        count = self.ui.ckList.count()
        for i in range(count):
            cookies_list.append(self.ui.ckList.item(i).text())
        cookies = cookies_list[random.randint(0, len(cookies_list) - 1)].strip('\n')
        # print(cookies)
        return cookies

    # 增加时间
    def sql_fail_time(self,day):
        today = datetime.datetime.now()
        # 当前时间增加一天
        offset = datetime.timedelta(days=day)
        re_date = (today + offset).strftime('%Y-%m-%d %H:%M:%S')
        return re_date

    # 时间戳对比时间
    def time_stamp(self,time_data):
        timeArray = time.strptime(time_data, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp

    #获取房间ID
    def get_room_id(self):
        url = self.ui.roomUrl.text().strip()
        url = url.split('&')[0]
        room_id = re.findall(r'room_id=(.*)', url)[0]
        print('获取房间ID:'+room_id)
        return room_id

    #随机选择一个CK 获取账号名称
    def get_ck_name(self):
        try:
            ck_lists = self.get_all_ck()
            choice_ck = random.choice(ck_lists).strip()
            room_id = self.get_room_id()
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Host': 'mbd.baidu.com',
                'Referer': 'http://live.baidu.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4462.0 Safari/537.36',
                'Cookie': choice_ck
            }
            information_url = 'http://mbd.baidu.com/searchbox?'
            params = {
                'cmd': '371',
                'action': 'star',
                'service': 'bdbox',
                'osname': 'pc',
                'data': '{"data":{"room_id":"' + room_id + '","device_id":"pc-' + self.ran_tag_str(
                    32) + '","source_type":0}}',
                '_': str(int(self.get_time() * 1000)),
                # 'callback': '__jsonp_callback_0__'
            }
            information = requests.get(url=information_url, headers=headers, params=params)
            if information.status_code == 200:
                reults = information.json()
                # print(reults)
                userName = reults['data']['371']['users']['nick_name']
                print(userName)
                self.ui.ckName.setText(userName)
                with open('.ini/oneTrainSend.ini', 'w', encoding='utf-8') as f:
                    f.write(room_id+'\n'+choice_ck)
                    f.close()
        except:
            QMessageBox.information(self,'错误提示','配置文件错误！')

    #随机选择一个CK 获取账号名称
    def get_ck_name_2(self):
        try:
            ck_lists = self.get_all_ck()
            choice_ck = random.choice(ck_lists).strip()
            room_id = self.get_room_id()
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Host': 'mbd.baidu.com',
                'Referer': 'http://live.baidu.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4462.0 Safari/537.36',
                'Cookie': choice_ck
            }
            information_url = 'http://mbd.baidu.com/searchbox?'
            params = {
                'cmd': '371',
                'action': 'star',
                'service': 'bdbox',
                'osname': 'pc',
                'data': '{"data":{"room_id":"' + room_id + '","device_id":"pc-' + self.ran_tag_str(
                    32) + '","source_type":0}}',
                '_': str(int(self.get_time() * 1000)),
                # 'callback': '__jsonp_callback_0__'
            }
            information = requests.get(url=information_url, headers=headers, params=params)
            if information.status_code == 200:
                reults = information.json()
                # print(reults)
                userName = reults['data']['371']['users']['nick_name']
                print(userName)
                self.ui.ckName_2.setText(userName)
                with open('.ini/oneTrainSend2.ini', 'w', encoding='utf-8') as f:
                    f.write(room_id+'\n'+choice_ck)
                    f.close()
        except:
            QMessageBox.information(self,'错误提示','配置文件错误！')

    #随机选择一个CK 获取账号名称
    def get_ck_name_3(self):
        try:
            ck_lists = self.get_all_ck()
            choice_ck = random.choice(ck_lists).strip()
            room_id = self.get_room_id()
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Host': 'mbd.baidu.com',
                'Referer': 'http://live.baidu.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4462.0 Safari/537.36',
                'Cookie': choice_ck
            }
            information_url = 'http://mbd.baidu.com/searchbox?'
            params = {
                'cmd': '371',
                'action': 'star',
                'service': 'bdbox',
                'osname': 'pc',
                'data': '{"data":{"room_id":"' + room_id + '","device_id":"pc-' + self.ran_tag_str(
                    32) + '","source_type":0}}',
                '_': str(int(self.get_time() * 1000)),
                # 'callback': '__jsonp_callback_0__'
            }
            information = requests.get(url=information_url, headers=headers, params=params)
            if information.status_code == 200:
                reults = information.json()
                # print(reults)
                userName = reults['data']['371']['users']['nick_name']
                print(userName)
                self.ui.ckName_3.setText(userName)
                with open('.ini/oneTrainSend3.ini', 'w', encoding='utf-8') as f:
                    f.write(room_id+'\n'+choice_ck)
                    f.close()
        except:
            QMessageBox.information(self,'错误提示','配置文件错误！')

    #选中单账号的列表框内容
    def pitch_single(self):
        text = self.ui.singleList.currentItem().text()
        # print(text)
        if self.ui.onechoice1.isChecked():
            self.ui.single_line.setText(text)
        elif self.ui.onechoice2.isChecked():
            self.ui.single_line_2.setText(text)
        elif self.ui.onechoice3.isChecked():
            self.ui.single_line_3.setText(text)

    #单账号单词发送点击
    def oneSendButton_click(self):
        # 检测激活码有效性
        CDKEY = self.Detection_cdkey()
        print(CDKEY)
        if CDKEY == 'OK':
            ckName = self.ui.ckName.text()
            if ckName != 'null':
                text = self.ui.single_line.text()
                if text != '':
                    with open('.ini/choiceCK.ini', 'w', encoding='utf-8') as f:
                        f.write('\n' + text)
                        f.close()
                    self.printf('='*25)
                    self.printf(f'正在发送内容：{text}')
                    self.printf('=' * 25)

                    oneSend = 'choiceCK.exe'
                    os.startfile(oneSend)
                    self.ui.single_line.setText('')

                else:
                    QMessageBox.information(self, '软件提示', '请先写入需要发送的弹幕语，在选择发送！')
            else:
                QMessageBox.information(self, '软件提示', '请先选择一个CK账号，在选择发送！')
        else:
            QMessageBox.information(self,'激活码失效','对不起，您的激活码已经失效！')

    #单账号单词发送点击
    def oneSendButton_click2(self):
        # 检测激活码有效性
        CDKEY = self.Detection_cdkey()
        print(CDKEY)
        if CDKEY == 'OK':
            ckName = self.ui.ckName_2.text()
            if ckName != 'null':
                text = self.ui.single_line_2.text()
                if text != '':
                    with open('.ini/choiceCK2.ini', 'w', encoding='utf-8') as f:
                        f.write('\n' + text)
                        f.close()
                    self.printf('='*25)
                    self.printf(f'正在发送内容：{text}')
                    self.printf('=' * 25)

                    oneSend = 'choiceCK2.exe'
                    os.startfile(oneSend)
                    self.ui.single_line_2.setText('')

                else:
                    QMessageBox.information(self, '软件提示', '请先写入需要发送的弹幕语，在选择发送！')
            else:
                QMessageBox.information(self, '软件提示', '请先选择一个CK账号，在选择发送！')
        else:
            QMessageBox.information(self,'激活码失效','对不起，您的激活码已经失效！')

    #单账号单词发送点击
    def oneSendButton_click3(self):
        # 检测激活码有效性
        CDKEY = self.Detection_cdkey()
        print(CDKEY)
        if CDKEY == 'OK':
            ckName = self.ui.ckName_3.text()
            if ckName != 'null':
                text = self.ui.single_line_3.text()
                if text != '':
                    with open('.ini/choiceCK3.ini', 'w', encoding='utf-8') as f:
                        f.write('\n' + text)
                        f.close()
                    self.printf('='*25)
                    self.printf(f'正在发送内容：{text}')
                    self.printf('=' * 25)

                    oneSend = 'choiceCK3.exe'
                    os.startfile(oneSend)
                    self.ui.single_line_3.setText('')

                else:
                    QMessageBox.information(self, '软件提示', '请先写入需要发送的弹幕语，在选择发送！')
            else:
                QMessageBox.information(self, '软件提示', '请先选择一个CK账号，在选择发送！')
        else:
            QMessageBox.information(self,'激活码失效','对不起，您的激活码已经失效！')

     # 房间信息获取
    def get_web_information(self):
        try:
            room_id = self.get_room_id()
                # print(cookie)
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
                'data': '{"data":{"room_id":"'+room_id+'","device_id":"pc-'+self.ran_tag_str(32)+'","source_type":0}}',
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
            # user_name = ['data']['371']['users']['nick_name']
            # userName = reults['data']['371']['users']['nick_name']
            # userInfo = reults['data']['371']['user_info']['is_login']
            # print(user_name)
            with open('hoster.jpg','wb') as f:
                response = requests.get(image_url).content
                f.write(response)
                f.close()

            QApplication.processEvents()

        except:
            self.printf('房间连接异常！请检查网络')

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

    #获取房间信息
    def link_live_info(self,roomID):
        # roomID = self.get_room_id()
        # print(roomID)
        get_roomInfo = linkLiveClick(roomID)
        roomInfo = get_roomInfo.get_web_information()
        print(roomInfo)
        return roomInfo

    #点击链接直播间后，展示图片 房间ID 主播昵称
    def link_live_click(self):
        try:
            if 'room_id' in self.ui.roomUrl.text():
                roomID = self.get_room_id()
                # print(room_id)
                roomData = self.link_live_info(roomID)
                # print(room_data)
                name = roomData[1]
                # 名字显示在直播间信息中
                self.ui.nickName.setText(name)
                # 房间ID显示在直播间信息中
                self.ui.roomID.setText(roomID)
                # 直播头像显示在直播间信息中
                self.ui.roomico.setPixmap(QPixmap('hoster.jpg'))

                QMessageBox.information(self, '连接成功', '连接百度服务器成功，请继续设置CK、弹幕、发送配置')
                self.ui.liveUrlbutton.setEnabled(False)

            else:
                QMessageBox.information(self, '连接失败', '请重新查看一下直播间URL是否复制正确！')
            QApplication.processEvents()
        except:
            pass

    #点击登陆直播间，人气协议
    def online_popul_click(self):
        if os.path.isfile('.ini/onlinenum.ini') == True:
            os.remove('.ini/onlinenum.ini')
        # 检测激活码有效性
        CDKEY = self.Detection_cdkey()
        print(CDKEY)
        try:
            if CDKEY == 'OK':
                onlineLogin = 'onlineLogin.exe'
                LoginBaidu = os.startfile(onlineLogin)
                self.ui.loginButton.setEnabled(False)
                self.ui.loginNumButton.setEnabled(True)
        except:
            pass

    def loginNum_thead(self):
        thread = Thread(target=self.get_login_num)
        thread.start()

    def get_login_num(self):
        try:
            with open('.ini/onlinenum.ini','r',encoding='utf-8') as f:
                self.ui.loginNum.setText(f.readlines()[0].strip())
        except:
            pass

    #人气协议新线程函数入口
    def onlineThread(self):
        thread = Thread(target=self.online_popul_click)
        thread.start()
        thread.join()

    #即时弹幕评论线程
    def instant_send_thread(self):
        thread = Thread(target=self.instant_send)
        thread.start()

    #即时弹幕发送
    def instant_send(self):
        if os.path.isfile('InstantComments.exe') == False:
            QMessageBox.information(self, '操作失败', '软件缺少即时弹幕发送组件，请联系Steven获取')
            sys.exit()
        # 检测激活码有效性
        CDKEY = self.Detection_cdkey()
        print(CDKEY)
        if CDKEY == 'OK':
            try:
                comment = self.ui.instantADS.text()
                delay = self.ui.instantDelay.text()
                room_id = self.get_room_id()
                ckPath = 'CK.txt'
                self.printf('即时弹幕评论开启>>>>>>>>>>>>>')
                self.printf('='*25)
                self.ui.instantSendButon.setText('正在发送')
                self.ui.instantSendButon.setEnabled(False)
                self.ui.instantStopButton.setEnabled(True)

                if os.path.isfile('.ini/instantComments.ini') == True:
                    os.remove('.ini/instantComments.ini')

                with open('.ini/instantComments.ini','a',encoding='utf-8')as f:
                    f.write(comment+'\n'+delay+'\n'+ckPath+'\n'+room_id)
                    f.close()

                InstantComments = 'InstantComments.exe'
                os.startfile(InstantComments)


            except:
                pass

    #即时发送停止
    def instant_stop(self):
        try:
            with open('.ini/InstantCommentsPID.ini', 'r', encoding='utf-8')as f:
                PID = f.read().strip()
            os.system('taskkill /f /pid %s' % PID)
            os.remove('.ini/instantComments.ini')
        except:
            pass
        self.ui.instantSendButon.setText('发送')
        self.ui.instantSendButon.setEnabled(True)
        self.ui.instantStopButton.setEnabled(False)
        self.printf('即时弹幕关闭>>>>>>>>>>>>>')

    # 创建停止弹幕子线程
    def stopButton_thread(self):
        thread = Thread(target=self.get_stopButton_click)
        thread.start()

    #停止发送
    def get_stopButton_click(self):
        try:
            with open('.ini/SendCommentsPID.ini','r',encoding='utf-8')as f:
                PID = f.read().strip()
            os.system('taskkill /f /pid %s' % PID)
            os.remove('.ini/sendComments.ini')
        except:
            pass
        self.ui.stopButton.setEnabled(False)
        self.ui.sendButton.setEnabled(True)
        self.ui.sendButton.setText('发送弹幕')
        self.printf('弹幕发送即将停止>>>>>>>>>>')

    #发送事件绑定
    def get_sendButton_click(self):
        try:
            # 检测激活码有效性
            CDKEY = self.Detection_cdkey()
            print(CDKEY)
            if CDKEY == 'OK':
                self.ui.sendButton.setText('正在发送')
                self.ui.sendButton.setEnabled(False)
                self.ui.stopButton.setEnabled(True)
                if os.path.isfile('SendComments.exe') == False:
                    QMessageBox.information(self, '操作失败', '软件缺少弹幕发送运行组件，请联系Steven获取')

                ckPath = 'CK.txt'
                adsPath ='ADS.txt'
                roomID = self.get_room_id()
                cycles = self.ui.xunhuan.text()
                delayFirst = self.ui.adsDelay1.text()
                delayLast = self.ui.adsDelay2.text()
                if os.path.isfile('.ini/sendComments.ini') == True:
                    os.remove('.ini/sendComments.ini')

                with open('.ini/sendComments.ini','a',encoding='utf-8')as f:
                    f.write(ckPath+'\n'+adsPath+'\n'+roomID+'\n'+cycles+'\n'+delayFirst+'\n'+delayLast)
                    f.close()
                sendComments = 'SendComments.exe'
                os.startfile(sendComments)
                print('组件开启成功！')
            else:

                QMessageBox.information(self,'激活码失效','对不起，您的激活码已经失效！')
        except:
            QMessageBox.information(self, '组件错误', '发送组件有问题！')

    #停止彩蛋发送线程
    def stopCaidan_thread(self):
        thread = Thread(target=self.get_stopCaidan_click)
        thread.start()

    #彩蛋停止点击事件
    def get_stopCaidan_click(self):
        try:
            with open('.ini/SendEggshellPID.ini', 'r', encoding='utf-8')as f:
                PID = f.read().strip()
            os.system('taskkill /f /pid %s' % PID)
            os.remove('.ini/Eggshell.ini')
        except:
            pass

        self.ui.sendCaidan.setText('发送彩蛋')
        self.ui.sendCaidan.setEnabled(True)
        self.ui.stopCaidan.setEnabled(False)
        self.printf('=' * 25)
        self.printf('彩蛋弹幕即将停止>>>>>>>>>')
        self.printf('=' * 25)

    #开启彩蛋发送线程
    def sendCaidan_thread(self):
        thread = Thread(target=self.get_sendCaidan_click)
        thread.start()

    #彩蛋发送点击事件
    def get_sendCaidan_click(self):
        # 检测激活码有效性
        CDKEY = self.Detection_cdkey()
        print(CDKEY)
        if CDKEY == 'OK':
            if os.path.isfile('SendEggshell.exe') == False:
                QMessageBox.information(self, '错误提示', '发送彩蛋组件丢失，请联系Steven获取！')
                sys.exit()
            try:
                self.ui.sendCaidan.setText('正在发送')
                self.ui.sendCaidan.setEnabled(False)
                self.ui.stopCaidan.setEnabled(True)
                self.printf('=' * 25)
                self.printf('软件开始发送彩蛋')
                self.printf('=' * 25)
                ckPath = 'CK.txt'
                # adsPath = 'ADS.txt'
                roomID = self.get_room_id()
                if self.ui.zanCheck.isChecked():
                    zancheck = 'True'
                else:
                    zancheck = 'False'

                if self.ui.shareCheck.isChecked():
                    sharecheck = 'True'
                else:
                    sharecheck = 'False'

                if self.ui.followCheck.isChecked():
                    followcheck = 'True'
                else:
                    followcheck = 'False'

                zanFisrt = self.ui.zanDelay1.text()
                zanLast = self.ui.zanDelay2.text()
                shareFisrt = self.ui.shareDelay1.text()
                shareLast = self.ui.shareDelay2.text()
                followFirst = self.ui.followDelay1.text()
                followLast = self.ui.followDelay2.text()

                if os.path.isfile('.ini/Eggshell.ini') == True:
                    os.remove('.ini/Eggshell.ini')

                with open('.ini/Eggshell.ini','a',encoding='utf-8')as f:
                    f.write(zancheck+'\n'+zanFisrt+'\n'+zanLast+'\n'+sharecheck+'\n'+shareFisrt+'\n'+shareLast+'\n'+followcheck+'\n'+followFirst+'\n'+followLast+'\n'+roomID+'\n'+ckPath)
                    f.close()

                SendEggshell = 'SendEggshell.exe'
                os.startfile(SendEggshell)
            except:
                pass

        else:
            QMessageBox.information(self,'激活码失效','对不起，您的激活码已经过期失效！')

    # 获取本地mac地址
    def get_mac_address(self):
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])

    #判断激活码类型
    def cdkey_type(self):
        text = self.ui.keyGroup.checkedButton().text()
        return text

    # 检测本地激活码
    def Detection_cdkey(self):

        local_cdkey = self.ui.jihuoma.text().strip()
        cdkey_type = self.cdkey_type()

        if cdkey_type == '天卡':
            sql_fail_time = self.sql_fail_time(1)
            data_table = 'BaiduMacDay'
        elif cdkey_type == '周卡':
            sql_fail_time = self.sql_fail_time(7)
            data_table = 'BaiduMacWeek'
        elif cdkey_type == '月卡':
            sql_fail_time = self.sql_fail_time(30)
            data_table = 'BaiduMacMonth'
        elif cdkey_type == '季卡':
            sql_fail_time = self.sql_fail_time(120)
            data_table = 'BaiduMacQuerter'
        print(cdkey_type)
        # 判断本地是否存在激活码
        if len(local_cdkey) == 55:
            cursor.execute(
                'SELECT COUNT(cdkey),mac,failtime from {data_table} WHERE cdkey = "{local_cdkey}"'.format(
                    data_table=data_table, local_cdkey=local_cdkey))
            result = cursor.fetchone()
            # 新激活码写入Mac地址和激活时间
            if result[0] == 1 and result[1] == None:
                # 判断Mac地址是否存在
                # Mac地址写入数据库，时间写入数据库
                sql = 'UPDATE {data_table} SET mac="{mac}",datetime="{datetime}",failtime="{failtime}" WHERE cdkey = "{local_cdkey}"'.format(
                    data_table=data_table, mac=self.get_mac_address(), datetime=self.get_now_time(),
                    failtime=sql_fail_time, local_cdkey=local_cdkey)

                try:
                    cursor.execute(sql)
                    con.commit()
                    # 窗口显示激活码到期时间
                    self.ui.failtime.setText(sql_fail_time)

                    local_cdkey_msg = 'OK'
                    print('激活码正确！')

                except:
                    # print('>>>无法连接服务器，确认网络是否正常！')
                    self.printf('>>>无法连接服务器，确认网络是否正常')
                    con.rollback()
            # 程序激活码Mac地址正确时，运行程序
            elif result[0] == 1 and result[1] == self.get_mac_address() and self.time_stamp(
                    self.get_now_time()) < self.time_stamp(result[2]):

                local_cdkey_msg = 'OK'
                self.ui.failtime.setText(sql_fail_time)
                print('激活码正确！')

            elif result[1] != None and result[1] != self.get_mac_address():
                local_cdkey_msg = 'error'

                self.printf('>>>:该激活码以绑定其他电脑，激活码重复使用已记录，记录三次后，自动删除激活码协议，请勿在其他电脑上使用该激活码！')

            elif self.time_stamp(self.get_now_time()) > self.time_stamp(result[2]):
                local_cdkey_msg = 'error'

                self.printf('>>>:激活码使用到期！购买激活码请联系Steven QQ：2621228281')
            else:
                local_cdkey_msg = 'error'

                self.printf('>>>:激活码错误，请核对后再进行输入！购买激活码请联系Steven QQ：2621228281')


        elif 1 < len(local_cdkey) < 55 or len(local_cdkey) > 55:
            local_cdkey_msg = 'error'

            self.printf('>>>:激活码错误，请核对后再进行输入！如未购买激活码请联系Steven QQ：2621228281')
            # print('本地激活码错误！')

        elif len(local_cdkey) == 0:
            local_cdkey_msg = 'error'

            self.printf('>>>:没有输入激活码，请购买请激活码后使用程序！购买联系Steven QQ：2621228281')
        else:
            local_cdkey_msg = 'error'

            self.printf('>>>:激活码错误，请购买请激活码后使用程序！购买联系Steven QQ：2621228281')

            # print('本地没有激活码！')
        QApplication.processEvents()
        return local_cdkey_msg



#链接直播间展示图片的类
class linkLiveClick():
    #初始化房间ID
    def __init__(self,roomID):
        self.roomID = roomID

    # 房间信息获取
    def get_web_information(self):
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
        information_url = 'http://mbd.baidu.com/searchbox?'
        params = {
            'cmd': '371',
            'action': 'star',
            'service': 'bdbox',
            'osname': 'h5pre',
            'data': '{"data":{"room_id":"' + self.roomID + '","device_id":"pc-' + self.ran_tag_str(32) + '","source_type":0}}',
            '_': str(int(self.get_time() * 1000)),
            # 'callback': '__jsonp_callback_0__'
        }

        information = requests.get(url=information_url, headers=headers, params=params)

        reults = information.json()
        fans_num = reults['data']['371']['host']['fans']
        image_url = reults['data']['371']['host']['image']['image_33']
        name = reults['data']['371']['host']['name']
        online_users = reults['data']['371']['online_users']
        title = reults['data']['371']['video']['title']
        # user_name = ['data']['371']['users']['nick_name']
        # userName = reults['data']['371']['users']['nick_name']
        # userInfo = reults['data']['371']['user_info']['is_login']
        # print(user_name)
        with open('hoster.jpg', 'wb') as f:
            response = requests.get(image_url).content
            f.write(response)
            f.close()

        QApplication.processEvents()
        return title, name, online_users, fans_num

    # 获取时间戳
    def get_time(self):
        shijiancuo = time.time()
        return shijiancuo

    # 随机ID
    def ran_tag_str(self,num):
        # 随机变量
        suiji = 'abcdefghijklmnopqrstuvwxyz0123456789'
        salt = ''
        for i in range(num):
            i = random.choice(suiji)
            salt += i
        return salt

class timeThread(QThread):
    def __init__(self,delay):
        super(timeThread, self).__init__()
        self.delay = delay
    def run(self):
        time.sleep(self.delay)
        # self.sleep(self.delay)


if __name__ == '__main__':
    app=0#
    # 每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数。
    app = QApplication(sys.argv)
    #绑定窗口
    window = BaiduLive()
    # 显示在屏幕上
    window.show()
    QApplication.processEvents()
    # 系统exit()方法确保应用程序干净的退出
    # 的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替
    sys.exit(app.exec_())

