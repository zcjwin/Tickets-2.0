
import request_tickets_spider
from threading import Thread
from selenium_tickets_spider import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets
import sys, os, re
import random


eventDateList = []
gra = BuyUrbtix()

class GAKEY(QDialog):
    def __init__(self):
        super(QDialog,self).__init__()
        self.setGeometry(230, 260, 300, 460)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(115, 400, 70, 30)
        self.setWindowTitle("输入信用卡信息")
        self.pushButton.setText("确定")
        self.pushButton.clicked.connect(self.set_credit_card)

        self.lineEdit_1 = QtWidgets.QLineEdit(self)
        self.lineEdit_1.setGeometry(QtCore.QRect(100, 80, 171, 30))

        self.lineEdit_2 = QtWidgets.QLineEdit(self)
        self.lineEdit_2.setGeometry(QtCore.QRect(100, 150, 171, 30))

        self.combox_1 = QtWidgets.QComboBox(self)
        self.combox_1.setGeometry(QtCore.QRect(100, 220, 171, 30))
        self.combox_1.addItems(["2019","2020","2021","2022","2023","2024","2025","2026","2027","2028","2099"])

        self.combox_2 = QtWidgets.QComboBox(self)
        self.combox_2.setGeometry(QtCore.QRect(100, 290, 171, 30))
        self.combox_2.addItems(["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])

        self.label_1 = QtWidgets.QLabel(self)
        self.label_1.setGeometry(QtCore.QRect(30, 80, 60, 30))
        self.label_1.setText("信用卡号:")

        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(30, 150, 60, 30))
        self.label_2.setText("安全码号:")

        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(30, 220, 60, 30))
        self.label_3.setText("到期年份:")

        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(30, 290, 60, 30))
        self.label_4.setText("到期月份:")

        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(100, 340, 171, 30))
        self.label_5.setStyleSheet("color:red;font-size:18px")

    def set_credit_card(self):
        cardNum = self.lineEdit_1.text()
        cardPwd = self.lineEdit_2.text()
        validityYear = self.combox_1.currentText()
        validityMorth = self.combox_2.currentText()
        dataCard = (cardNum, cardPwd, validityYear, validityMorth)
        print(dataCard)
        if cardNum and cardPwd:
            self.close()
        else:
            self.label_5.setText("内容不允许为空！")


class Ui_MainWindow(QMainWindow):

    threads = []
    def __init__(self):
        super(QMainWindow,self).__init__()
        # self.gakey = gakey
        # self.gakey.show()

        self.buy_succeed_count = 0
        self.loginecordThread = Thread(target=self.output_login_status)  # 开启登录日志监控
        self.registerRecordThread = Thread(target=self.output_register_record)  # 开启购买日志监控
        self.buyRecordThread = Thread(target=self.output_buy_record)  # 开启注册日志监控
        self.threads.append(self.loginecordThread)
        self.threads.append(self.registerRecordThread)
        self.threads.append(self.buyRecordThread)
        self.loginecordThread.setDaemon(True)
        self.registerRecordThread.setDaemon(True)
        self.buyRecordThread.setDaemon(True)
        self.loginecordThread.start()
        self.registerRecordThread.start()
        self.buyRecordThread.start()

    def setupUi(self, MainWindow):
        # MainWindow.setStyleSheet("#MainWindow{background-color: yellow}")
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 478)
        MainWindow.setMinimumSize(640, 478)
        MainWindow.setMaximumSize(640, 478)
        # MainWindow.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint) 
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 631, 461))
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

        # 登录按钮
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(230, 60, 121, 61))
        self.pushButton.setObjectName("pushButton")
        # 登录日志输出
        self.label_0 = QtWidgets.QLabel(self.tab)
        self.label_0.setGeometry(QtCore.QRect(30, 180, 54, 12))
        self.label_0.setObjectName("label_0")

        # 注册日志
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.tab)
        self.textBrowser_2.setGeometry(QtCore.QRect(30, 200, 561, 221))
        self.textBrowser_2.setObjectName("textBrowser_2")


        # 登录页面
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")

        self.tabWidget.addTab(self.tab, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")

        self.lineEdit = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit.setGeometry(QtCore.QRect(90, 30, 171, 31))
        self.lineEdit.setObjectName("lineEdit")

        # 查询商品名称
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 30, 58, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.search_1)


        self.label = QtWidgets.QLabel(self.tab_2)
        self.label.setGeometry(QtCore.QRect(30, 80, 54, 12))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setGeometry(QtCore.QRect(30, 130, 54, 12))
        self.label_2.setObjectName("label_2")

        self.comboBox = QtWidgets.QComboBox(self.tab_2)
        self.comboBox.setGeometry(QtCore.QRect(90, 120, 191, 31))
        self.comboBox.setObjectName("comboBox")
        # self.comboBox.currentText()

        self.comboBox_2 = QtWidgets.QComboBox(self.tab_2)
        self.comboBox_2.setGeometry(QtCore.QRect(90, 70, 459, 31))
        self.comboBox_2.setObjectName("comboBox_2")

        # 选择数量
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setGeometry(QtCore.QRect(300, 40, 54, 12))
        self.label_3.setObjectName("label_3")

        self.lineEdit_1 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_1.setGeometry(QtCore.QRect(355, 32, 51, 27))
        self.lineEdit_1.setObjectName("lineEdit_1")

        # 购买成功数量
        self.label_6 = QtWidgets.QLabel(self.tab_2)
        self.label_6.setGeometry(QtCore.QRect(450, 40, 54, 12))
        self.label_6.setObjectName("label_6")

        self.label_7 = QtWidgets.QLabel(self.tab_2)
        self.label_7.setGeometry(QtCore.QRect(500, 40, 54, 12))
        self.label_7.setObjectName("label_7")
        self.label_7.setStyleSheet("font-size:16px;color:red") # 设置字体颜色


        # 购买按钮 当所有条件选择完之后点击
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_3.setGeometry(QtCore.QRect(30, 160, 54, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.search_2)

        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setGeometry(QtCore.QRect(30, 210, 54, 12))
        self.label_4.setObjectName("label_4")

        # 购买日志输出
        self.textBrowser_1 = QtWidgets.QTextBrowser(self.tab_2)
        self.textBrowser_1.setGeometry(QtCore.QRect(30, 230, 521, 192))
        self.textBrowser_1.setObjectName("textBrowser")
        # 添加显示数据
        # self.textBrowser_1.append('购买日志')

        # 抢票中心页面
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # 账号注册页面
        self.tabWidget.addTab(self.tab_3, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # 银行卡信息输入页面
        self.tabWidget.addTab(self.tab_4, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # 点击注册按钮
        self.pushButton_4 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_4.setGeometry(QtCore.QRect(230, 60, 121, 61))
        self.pushButton_4.setObjectName("pushButton")

        # 注册日志输出
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.tab_3)
        self.textBrowser_3.setGeometry(QtCore.QRect(30, 200, 561, 221))
        self.textBrowser_3.setObjectName("textBrowser_3")

        self.label_5 = QtWidgets.QLabel(self.tab_3)
        self.label_5.setGeometry(QtCore.QRect(30, 180, 54, 12))
        self.label_5.setObjectName("label_5")


        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "城市售票网-抢票"))
        self.pushButton.setText(_translate("MainWindow", "点击登录"))
        self.pushButton.clicked.connect(self.login)
        # self.pushButton.clicked.connect(self.set_credit_card)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "账号登录"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "抢购中心"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "账号注册"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "输入卡号"))
        self.label_0.setText(_translate("MainWindow", "登录日志:"))
        self.pushButton_2.setText(_translate("MainWindow", "搜索名称"))
        self.pushButton_3.setText(_translate("MainWindow", "点击购买"))
        self.pushButton_4.setText(_translate("MainWindow", "点击注册"))
        self.label.setText(_translate("MainWindow", "选择场次:"))
        self.label_2.setText(_translate("MainWindow", "选择价格:"))
        self.label_3.setText(_translate("MainWindow", "购买数量:"))
        self.label_4.setText(_translate("MainWindow", "购买日志:"))
        self.label_5.setText(_translate("MainWindow", "注册日志:"))
        self.label_6.setText(_translate("MainWindow", "已购买:"))
        self.label_7.setText(_translate("MainWindow", "0"))


    # 点击登录执行
    def login(self):
        ipList = [""]
        # ipList = request_tickets_spider.get_ip_list(10)
        self.textBrowser_2.append("开始登陆，请等待...")
        userinfo_list = []
        with open('infomation.txt', 'rt',  encoding='utf-8') as f:
            info_record = re.findall("'loginId': '(.*?)'", f.read())
            for loginId in info_record:
                userinfo_list.append(loginId)
        # 多线程
        for thr in userinfo_list[:1]:
            grabber = BuyUrbtix()
            ip = random.choice(ipList)
            Thread_name = Thread(target=grabber.openSite, args=(thr,ip))
            self.threads.append(Thread_name)
            Thread_name.setDaemon(True)
            Thread_name.start()

        # self.threads[0].start()

    # 日志更新
    def output_login_status(self):
        # 登录成功输出
        while True:
            # 登陆日志
            login_record_list = login_record()
            if login_record_list:
                for i in login_record_list:
                    self.textBrowser_2.append(i)
                    login_record_list.remove(i)
            time.sleep(0.1)

    # 购买日志
    def output_buy_record(self):
        buy_record_list = buy_record()
        if buy_record_list:
            for i in buy_record_list:
                if "购买成功" in i:
                    self.buy_succeed_count += 1
                    self.label_7.setText(str(self.buy_succeed_count))
                self.textBrowser_1.append(i)
                buy_record_list.remove(i)
        time.sleep(0.1)

    # 注册日志
    def output_register_record(self):
        register_record_list = register_record()
        if register_record_list:
            for i in register_record_list:
                self.textBrowser_3.append(i)
                register_record_list.remove(i)
        time.sleep(0.1)

    # 点击搜索按钮执行
    def search_1(self):
        Thread_name = Thread(target=self.refresh)
        self.threads.append(Thread_name)
        Thread_name.start()

    # 把信息刷新到界面
    def refresh(self):
        self.comboBox_2.clear()
        self.comboBox.clear()
        try:
            if self.lineEdit.text():
                global eventDateList
                keyword = self.lineEdit.text()
                eventDateList = request_tickets_spider.get_date_url(keyword)
                for i,eventDateName in enumerate(eventDateList):
                    self.comboBox_2.addItem(eventDateName['eventDateName'], i)
                    self.comboBox_2.setCurrentIndex(0)
                for i,price in enumerate(eventDateList[0]['priceList']):
                    self.comboBox.addItem(str(price), i)# 价格
                    self.comboBox.setCurrentIndex(0)
            else:
                sys.exit()
        except:
            sys.exit("")

    # 购买条件选择后点击执行
    def search_2(self):
        my_attr['selPrice'] = self.comboBox.currentIndex()
        selDateName = self.comboBox_2.currentText()
        my_attr['selNum'] = 3
        for event in eventDateList:
            if selDateName == event["eventDateName"]:
                my_attr['selSeatUrl'] = event["eventUrl"]
                self.textBrowser_1.append("请您耐心等待...")

    #点击注册执行并打印注册 
    def register(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # 创建一个QApplication，也就是你要开发的软件app
    MainWindow = QtWidgets.QMainWindow()    # 创建一个QMainWindow，用来装载你需要的各种组件、控件
    # gakey = GAKEY()
    ui = Ui_MainWindow()                     # ui是你创建的ui类的实例化对象
    ui.setupUi(MainWindow)                  # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow
    MainWindow.show()                       # 执行QMainWindow的show()方法，显示这个QMainWindow
    sys.exit(app.exec_())

