from threading import Thread
import request_spider
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import sys, time


class Ui_MainWindow(QMainWindow):

    threads = []
    keywordJudge = ''
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.ex = Example()


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

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "城市售票网-抢票"))
        self.pushButton.setText(_translate("MainWindow", "点击登录"))
        self.pushButton.clicked.connect(self.login)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "账号登录"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "抢购中心"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "账号注册"))
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

        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    # 点击登录执行
    def login(self):
        ex = Example()

    # 点击搜索按钮执行
    def search_1(self):
        keyword = self.lineEdit.text()
        if keyword == self.keywordJudge:
            return
        self.keywordJudge = keyword
        Thread_name = Thread(target=self.refresh)
        self.threads.append(Thread_name)
        Thread_name.start()
        Thread_name.join()
        self.ex.refresh_cb()
        self.ex.show()


    # 把信息刷新到界面
    def refresh(self):
        try:
            if self.lineEdit.text():
                global eventDateList
                keyword = self.lineEdit.text()
                eventDateList = request_spider.get_date_url(keyword)
                self.ex.sessionList = [eventDateName['eventDateName'] for eventDateName in eventDateList]
                self.ex.priceList = [price for price in eventDateList[0]['priceList']]
            else:
                sys.exit()
        except Exception as err:
            print(err)
            sys.exit("")


    # 购买条件选择后点击执行
    def search_2(self):
        pass

    #点击注册执行并打印注册 
    def register(self):
        pass


class Example(QMainWindow):
    sessionList = []
    priceList = []
    sessionListEvn = []
    priceListEvn = []

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle('城市售票网')   # 主窗口
        self.resize(680, 800)              # 主窗口大小

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
        res=QMessageBox.question(self,'提示','您确定选择无误吗？',QMessageBox.Yes|QMessageBox.No,QMessageBox.No) #两个按钮是否， 默认No则关闭这个提示框
        if res==QMessageBox.Yes:
            QCloseEvent.accept()
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
        if self.sessionListEvn and self.priceListEvn:
            return
        for i,item in enumerate(self.sessionList):
            cb = QCheckBox(item, self.topFiller)
            cb.move(30, 60+30*i)
            cb.stateChanged.connect(self.changecb2)   # 连接到单个复选框槽函数
            self.sessionListEvn.append(cb)
            cb.show()
        self.topFiller.setMinimumSize(580,20*30)  #######设置滚动条的尺寸

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
        self.close()
        if self.sessionList:
            for i in self.sessionListEvn+self.priceListEvn:
                if i.isChecked():
                    print(i.text())
            for i in self.sessionListEvn+self.priceListEvn:
                if i.isChecked():
                    break
                else:
                    print("你什么都没有选中(内)！")
                    break
        else:
            print("你什么都没有选中(外)！")

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

    # 单个复选框槽函数
    def changecb_odd(self):
        # 全选打勾
        for qcb in self.priceListEvn:
            if not qcb.isChecked():
                break
        else:
            self.cb1.setCheckState(Qt.Checked)
        # 取消全选打勾
        for qcb in self.priceListEvn:
            if qcb.isChecked():
                break
        else:
            self.cb1.setTristate(False)
            self.cb1.setCheckState(Qt.Unchecked)

    def refresh_cb(self):
        while True:
            if self.sessionList and self.priceList:
                self.create_c()
                break
            time.sleep(0.2)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # 创建一个QApplication，也就是你要开发的软件app
    MainWindow = QtWidgets.QMainWindow()    # 创建一个QMainWindow，用来装载你需要的各种组件、控件
    ui = Ui_MainWindow()                     # ui是你创建的ui类的实例化对象
    ui.setupUi(MainWindow)                  # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow
    MainWindow.show()                       # 执行QMainWindow的show()方法，显示这个QMainWindow
    # ex = Example()
    # ex.show()
    sys.exit(app.exec_())

