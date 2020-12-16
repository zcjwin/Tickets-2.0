import ctypes
import win32con
import request_spider
from selenium_tickets_spider import *
from threading import Thread
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import sys, time, re
import datetime

SESSION_DATA = False
SHOW_S_P = False

class Worker(QThread):

    valueChanged = pyqtSignal(int)  # 值变化信号
    handle = -1

    def run(self):
        global SESSION_DATA,EXIT_COND
        try:
            self.handle = ctypes.windll.kernel32.OpenThread(  # @UndefinedVariable
                win32con.PROCESS_ALL_ACCESS, False, int(QThread.currentThreadId()))
        except Exception as e:
            print('get thread handle failed', e)
        # print('thread id', int(QThread.currentThreadId()))
        # 循环发送信号
        while True:
            if SESSION_DATA:
                self.valueChanged.emit(1024)
                SESSION_DATA = False
            time.sleep(0.1)

    def exit_thread(self):
        os._exit(122)


class Ui_MainWindow(QMainWindow):

    threads = []
    keywordJudge = ''
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        # self.ex = Example()

        self.buy_succeed_count = 0
        for func in [self.output_buy_record, self.output_login_status,self.output_register_record]:
            thr = Thread(target=func)
            thr.setDaemon(True)
            thr.start()

        # 子线程
        self._thread = Worker(self)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.valueChanged.connect(ex.create_c)
        self._thread.start()

    def setupUi(self, MainWindow):
        # MainWindow.setStyleSheet("#MainWindow{background-color: yellow}")
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 478)
        # MainWindow.setMinimumSize(640, 478)
        # MainWindow.setMaximumSize(640, 478)
        # 取消最大化
        MainWindow.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        # 固定窗口大小
        MainWindow.setFixedSize(self.width(), self.height())
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
        self.pushButton.setGeometry(QtCore.QRect(200, 110, 120, 30))
        self.pushButton.setObjectName("pushButton")

        # 登陆个数输入框
        self.lineEdit_tab = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_tab.setGeometry(QtCore.QRect(318, 111, 120, 28))
        self.lineEdit_tab.setPlaceholderText("  请输入登陆个数")

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
        self.label_3.setGeometry(QtCore.QRect(300, 40, 70, 12))
        self.label_3.setObjectName("label_3")

        # 数量输入框
        self.lineEdit_1 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_1.setGeometry(QtCore.QRect(375, 32, 51, 27))
        self.lineEdit_1.setObjectName("lineEdit_1")

        # 购买成功数量
        self.label_6 = QtWidgets.QLabel(self.tab_2)
        self.label_6.setGeometry(QtCore.QRect(450, 40, 54, 12))
        self.label_6.setObjectName("label_6")

        self.label_7 = QtWidgets.QLabel(self.tab_2)
        self.label_7.setGeometry(QtCore.QRect(500, 40, 54, 12))
        self.label_7.setObjectName("label_7")
        self.label_7.setStyleSheet("font-size:16px;color:red") # 设置字体颜色

        self.label_8 = QtWidgets.QLabel(self.tab_2)
        self.label_8.setGeometry(QtCore.QRect(300, 130, 100, 12))
        self.label_8.setObjectName("label_8")

        self.lineEdit_8 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_8.setGeometry(QtCore.QRect(415, 122, 51, 27))
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.lineEdit_8.setText('4')

        # 购买按钮 当所有条件选择完之后点击
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_3.setGeometry(QtCore.QRect(30, 160, 54, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.search_2)

        # 退出程序按钮
        self.pushButton_quit = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_quit.setGeometry(QtCore.QRect(460, 160, 54, 31))
        self.pushButton_quit.setObjectName("pushButton_quit")
        self.pushButton_quit.clicked.connect(self.exit_quit)

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

        # 点击注册按钮
        self.pushButton_4 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_4.setGeometry(QtCore.QRect(200, 110, 120, 30))
        self.pushButton_4.setObjectName("pushButton")

        # 注册个数输入框
        self.lineEdit_tab3 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_tab3.setGeometry(QtCore.QRect(318, 111, 120, 28))
        self.lineEdit_tab3.setPlaceholderText("  请输入注册个数")

        # 注册日志输出
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.tab_3)
        self.textBrowser_3.setGeometry(QtCore.QRect(30, 200, 561, 221))
        self.textBrowser_3.setObjectName("textBrowser_3")

        self.label_5 = QtWidgets.QLabel(self.tab_3)
        self.label_5.setGeometry(QtCore.QRect(30, 180, 54, 12))
        self.label_5.setObjectName("label_5")

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "城市售票网-抢票"))
        self.pushButton.setText(_translate("MainWindow", "点击登录"))
        self.pushButton.clicked.connect(self.login)
        self.pushButton_4.clicked.connect(self.register)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "账号登录"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "抢购中心"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "账号注册"))
        self.label_0.setText(_translate("MainWindow", "登录日志:"))
        self.pushButton_2.setText(_translate("MainWindow", "搜索名称"))
        self.pushButton_3.setText(_translate("MainWindow", "点击购买"))
        self.pushButton_quit.setText(_translate("MainWindow", "退出程序"))
        self.pushButton_4.setText(_translate("MainWindow", "点击注册"))
        self.label.setText(_translate("MainWindow", "已择场次:"))
        self.label_2.setText(_translate("MainWindow", "已择价格:"))
        self.label_3.setText(_translate("MainWindow", "购买总数量:"))
        self.label_4.setText(_translate("MainWindow", "购买日志:"))
        self.label_5.setText(_translate("MainWindow", "注册日志:"))
        self.label_6.setText(_translate("MainWindow", "已购买:"))
        self.label_7.setText(_translate("MainWindow", "0"))
        self.label_8.setText(_translate("MainWindow", "每个账号购买数量:"))
        self.textBrowser_3.setText("")
        self.textBrowser_2.setText("")
        self.textBrowser_1.setText("")

        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    # 点击登录执行
    def login(self):
        try:
            regiterSum = int(self.lineEdit_tab.text())
        except Exception as err:
            res = QMessageBox.question(self, '提示', '请输入正整数！', QMessageBox.Ok)  # 提示框
            return
        ipList = [""]
        # ipList = request_tickets_spider.get_ip_list(10)
        self.textBrowser_2.append("开始登陆，请等待...")
        userinfo_list = []
        with open('infomation.txt', 'rt',  encoding='utf-8') as f:
            info_record = re.findall("'loginId': '(.*?)'", f.read())
            for loginId in info_record:
                userinfo_list.append(loginId)
        # 多线程
        for thr in userinfo_list[:regiterSum]:
            grabber = BuyUrbtix()
            ip = random.choice(ipList)
            Thread_name = Thread(target=grabber.openSite, args=(thr,ip))
            self.threads.append(Thread_name)
            Thread_name.setDaemon(True)
            Thread_name.start()

    # 点击搜索按钮执行
    def search_1(self):
        keyword = self.lineEdit.text()
        self.textBrowser_1.append("正在查询 %s 的所有场次和价格..." % keyword)
        if keyword == self.keywordJudge:
            self.textBrowser_1.append("请等待...")
            self.keywordJudge = ''
            return
        self.keywordJudge = keyword
        Thread_name = Thread(target=self.refresh)
        self.threads.append(Thread_name)
        Thread_name.start()

        Thread_01 = Thread(target=self.show_session_data)
        self.threads.append(Thread_01)
        Thread_01.start()


    # 把选择的场次和价格显示到主界面
    def show_session_data(self):
        global SHOW_S_P
        self.comboBox_2.clear()
        self.comboBox.clear()
        while True:
            # if self.ex.sessionName and self.ex.sessionPrice:
            if ex.sessionName and ex.sessionPrice and SHOW_S_P:
                for i,eventDateName in enumerate(ex.sessionName):
                    self.comboBox_2.addItem(eventDateName, i)
                for i,price in enumerate(ex.sessionPrice):
                    self.comboBox.addItem(str(price), i)# 价格
                self.comboBox.setCurrentIndex(0)
                self.comboBox_2.setCurrentIndex(0)
                ex.sessionName.clear()
                ex.sessionPrice.clear()
                SHOW_S_P = False
            time.sleep(0.2)

    # 把信息刷新到界面
    def refresh(self):
        try:
            if self.lineEdit.text():
                global eventDateList
                keyword = self.lineEdit.text()
                my_attr['selNum'] = self.lineEdit_8.text()
                ex.eventDateList = request_spider.get_date_url(keyword)
                if ex.eventDateList:
                    self.textBrowser_1.append("查询成功，请在选择界面选择场次和价格...")
                    global SESSION_DATA
                    SESSION_DATA = True
                    # ex.create_c()
                else:
                    self.textBrowser_1.append("查询失败，请确定您查询的节目存在...")
            else:
                sys.exit()
        except Exception as err:
            self.textBrowser_1.append("查询失败，请确定您查询的节目存在...")
            print(err)
            sys.exit()

    # 日志更新
    def output_login_status(self):
        # 登录成功输出
        while True:
            # 登陆日志
            login_record_list = login_record()
            if login_record_list:
                for i in login_record_list:
                    self.textBrowser_2.append(i)
                    self.textBrowser_2.moveCursor(self.textBrowser_2.textCursor().End)
                    login_record_list.remove(i)
            time.sleep(0.1)

    # 购买日志
    def output_buy_record(self):
        while True:
            buy_record_list = buy_record()
            if buy_record_list:
                for record in buy_record_list:
                    if "购买成功" in record:
                        self.buy_succeed_count += 1
                        self.label_7.setText(str(self.buy_succeed_count))
                    self.textBrowser_1.append(record)
                    self.textBrowser_1.moveCursor(self.textBrowser_1.textCursor().End)
                    buy_record_list.remove(record)
            time.sleep(0.1)

    # 注册日志
    def output_register_record(self):
        while True:
            register_record_list = register_record()
            if register_record_list:
                for i in register_record_list:
                    self.textBrowser_3.append(i)
                    self.textBrowser_3.moveCursor(self.textBrowser_3.textCursor().End)
                    register_record_list.remove(i)
            time.sleep(0.1)


    # 购买条件选择后点击执行
    def search_2(self):
        if not self.lineEdit_1.text():
            self.textBrowser_1.append("请输入购买总数量...")
            return

        if my_attr['selNum'] and my_attr['selPrice'] and my_attr['selSeatUrl']:
            self.textBrowser_1.append("正在购买，请等待...")
            return

        if ex.saleTime:
            Thread_name = Thread(target=self.wait_sale)
            Thread_name.setDaemon(True)
            Thread_name.start()
            return

        my_attr['gross'] = self.lineEdit_1.text()
        my_attr['selNum'] = self.lineEdit_8.text()
        my_attr['selPrice'] = ex.eventPrice
        my_attr['selSeatUrl'] = ex.eventUrl
        self.textBrowser_1.append("开始购买，请您耐心等待...")

    def wait_sale(self):
        dateList = ex.saleTime
        print("%s年%s月%s日%s时开始售票，等待购买！" % tuple(dateList))
        self.textBrowser_1.append("%s年%s月%s日%s时开始售票，等待购买！" % tuple(dateList))
        while True:
            saleTimestamp = int(time.mktime(time.strptime(''.join(dateList) + '0000', "%Y%m%d%H%M%S")))
            if saleTimestamp <= int(time.time()):
                print("%s年%s月%s日%s时开始售票，开始购买！" % tuple(dateList))
                self.textBrowser_1.append("%s年%s月%s日%s时开始售票，开始购买！" % tuple(dateList))
                break
            time.sleep(1)

        my_attr['gross'] = self.lineEdit_1.text()
        my_attr['selNum'] = self.lineEdit_8.text()
        my_attr['selPrice'] = ex.eventPrice
        my_attr['selSeatUrl'] = ex.eventUrl
        self.textBrowser_1.append("开始购买，请您耐心等待...")


    #点击注册执行并打印注册 
    def register(self):
        self.textBrowser_3.append("开始注册，请等待...")
        try:
            regiterSum = int(self.lineEdit_tab3.text())
        except Exception as err:
            res = QMessageBox.question(self, '提示', '请输入正整数！', QMessageBox.Ok)  # 提示框
            return
        threads = []
        for _ in range(regiterSum):
            uper = Register()
            Thread_name = Thread(target=uper.registerInfo)
            Thread_name.setDaemon(True)
            Thread_name.start()
            threads.append(Thread_name)

    # 退出程序
    def exit_quit(self):
        global EXIT_COND
        res = QMessageBox.question(self, '提示', '您确定要退出程序吗！', QMessageBox.Yes | QMessageBox.No)  # 提示框
        if res == QMessageBox.Yes:
            self._thread.exit_thread()
            time.sleep(1)
            sys.exit()
        else:
            pass


class Example(QMainWindow):
    sessionList = []
    priceList = []
    sessionListEvn = []
    priceListEvn = []
    eventDateList = []
    eventUrl = []
    eventPrice = []
    sessionName = []
    sessionPrice = []
    saleTime = []
    buyNum = 1

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle('城市售票网')   # 主窗口
        self.resize(680, 800)
        # 取消最大化
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        # 固定窗口大小
        self.setFixedSize(self.width(), self.height())

        self.w = QWidget()
        self.w.setFixedWidth(680)
        self.w.setFixedHeight(540)

        self.setCentralWidget(self.w)
        self.topFiller = QWidget()
        # 把布局放入到 w 窗口
        # 创建一个滚动条
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.topFiller)  # 滚动条放self.topFiller

        self.vbox = QVBoxLayout()               # 方框布局
        self.vbox.addWidget(self.scroll)        # 滚动条放入布局
        self.w.setLayout(self.vbox)

        self.initUI()

    def closeEvent(self, QCloseEvent):
        res = QMessageBox.question(self,'提示','您确定选择无误吗？',QMessageBox.Yes|QMessageBox.No,QMessageBox.No) #两个按钮是否， 默认No则关闭这个提示框
        if res == QMessageBox.Yes:
            global SHOW_S_P
            SHOW_S_P = True
            QCloseEvent.accept()
            self.cb1.setChecked(False)
            self.cb2.setChecked(False)
        else:
            QCloseEvent.ignore()

    def initUI(self):
        #新建全选复选框对象
        self.cb1 = QCheckBox('全选',self.topFiller)
        self.cb1.move(20,30)
        self.cb2 = QCheckBox('全选',self)
        self.cb2.move(20, 570)
        # 创建按钮
        bt1 = QPushButton('确定',self)
        bt2 = QPushButton('刷新',self)

        bt1.move(20,760)
        bt2.move(120,760)

        # 每当复选框的状态改变时，即每当用户选中或取消选中该信号时，就会发出此信号。
        # 所以当产生此信号的时候，我们将其连接相应的槽函数。
        self.cb1.stateChanged.connect(self.changecb1)   #  全选复选框连接到全选槽函数
        self.cb2.stateChanged.connect(self.changecb2)   #  全选复选框连接到全选槽函数
        bt1.clicked.connect(self.pitch_on)              #  连接到显示选中单元
        bt2.clicked.connect(self.create_c)              #  连接到创建函数

    def create_c(self):
        if self.eventDateList:
            self.sessionList = [eventDateName['eventDateName'] for eventDateName in self.eventDateList]
            self.priceList = [price for price in self.eventDateList[0]['priceList']]
            # print(self.priceList)
            # print(self.sessionList)
            ex.show()
        else:
            ex.show()
            QMessageBox.question(self, '提示', '搜索内容不存在！', QMessageBox.Ok)
            return

        # 清空上次搜索内容
        if self.sessionListEvn and self.priceListEvn:
            for s_evn in self.sessionListEvn:
                s_evn.deleteLater()
            for p_evn in self.priceListEvn:
                p_evn.deleteLater()

            self.sessionListEvn.clear()
            self.priceListEvn.clear()
            self.eventPrice.clear()
            self.eventUrl.clear()

        # 场次信息显示
        for i,item in enumerate(self.sessionList):
            cb = QCheckBox(item, self.topFiller)
            cb.move(30, 60+30*i)
            self.sessionListEvn.append(cb)
            cb.show()
        self.topFiller.setMinimumSize(580,(len(self.sessionList)+5)*30)  #设置滚动条的尺寸

        # 价格显示
        for i,item in enumerate(self.priceList):
            cb_1 = QCheckBox(str(item), self)
            if i % 2 == 0:
                i = i // 2 + 1
                cb_1.move(30, 570+30*i)
            else:
                i = i // 2 + 1
                cb_1.move(330, 570+30*i)
            self.priceListEvn.append(cb_1)
            cb_1.show()

    def pitch_on(self):
        if self.sessionList:
            for i in self.sessionListEvn:   # 遍历所有复选框
                if i.isChecked():           # 判断是否被选中
                    for eventDate in self.eventDateList:    # 遍历所有的数据
                        if eventDate['eventDateName'] == i.text():  # 判断数据是否被选中
                            if 'saleDate' in eventDate:
                                self.saleTime = eventDate['saleDate']
                                # print(eventDate['saleDate'])
                            self.eventUrl.append(eventDate["eventUrl"])     # 被选中则保存
                            self.sessionName.append(eventDate['eventDateName'])

            for i in self.priceListEvn:
                if i.isChecked():
                    if i.text() in self.eventDateList[0]['priceList']:
                        self.eventPrice.append(str(self.eventDateList[0]['priceList'].index(i.text())))
                        self.sessionPrice.append(i.text())

            # 如果选择的有数据，则关闭窗口，没有数据，提示选择数据
            if self.eventPrice and self.eventUrl:
                self.close()
            else:
                res = QMessageBox.question(self, '提示', '您没有选择或价格场次，确定退出吗？', QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.No)  # 两个按钮是否， 默认No则关闭这个提示框
                if res == QMessageBox.Yes:
                    self.close()
        else:
            print("输入内容不存在！")

    # 全选复选框槽函数
    def changecb1(self):
        if self.cb1.checkState() == Qt.Checked:
            for qcb in self.sessionListEvn:
                qcb.setChecked(True)
        elif self.cb1.checkState() == Qt.Unchecked:
            for qcb in self.sessionListEvn:
                qcb.setChecked(False)

    # 全选复选框槽函数
    def changecb2(self):
        if self.cb2.checkState() == Qt.Checked:
            for qcb in self.priceListEvn:
                qcb.setChecked(True)
        elif self.cb2.checkState() == Qt.Unchecked:
            for qcb in self.priceListEvn:
                qcb.setChecked(False)

    # 刷新按钮
    def refresh_cb(self):
        while True:
            if self.sessionList and self.priceList:
                self.create_c()
                break
            time.sleep(0.2)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # 创建一个QApplication，也就是你要开发的软件app
    ex = Example()
    MainWindow = QtWidgets.QMainWindow()    # 创建一个QMainWindow，用来装载你需要的各种组件、控件
    ui = Ui_MainWindow()                     # ui是你创建的ui类的实例化对象
    ui.setupUi(MainWindow)                  # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow
    MainWindow.show()                       # 执行QMainWindow的show()方法，显示这个QMainWindow
    # ex.show()
    sys.exit(app.exec_())

