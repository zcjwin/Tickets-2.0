import sys

from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem, QMessageBox
from PyQt5 import QtCore, QtWidgets

class GAKEY(QWidget):
    def __init__(self):
        super(GAKEY,self).__init__()
        # self.setGeometry(230, 260, 300, 460)
        self.setFixedSize(800,460)
        self.setWindowTitle("输入信用卡信息")
        # 固定窗口大小
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.setFixedSize(self.width(), self.height())

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(170, 400, 70, 30)
        self.pushButton.setText("添加")
        self.pushButton.clicked.connect(self.set_credit_card)

        self.pushButton_finish = QtWidgets.QPushButton(self)
        self.pushButton_finish.setGeometry(75, 400, 70, 30)
        self.pushButton_finish.setText("完成")
        self.pushButton_finish.clicked.connect(self.close)

        self.lineEdit_1 = QtWidgets.QLineEdit(self)
        self.lineEdit_1.setGeometry(QtCore.QRect(100, 60, 171, 30))

        self.lineEdit_3 = QtWidgets.QLineEdit(self)
        self.lineEdit_3.setGeometry(QtCore.QRect(100, 120, 171, 30))

        self.lineEdit_2 = QtWidgets.QLineEdit(self)
        self.lineEdit_2.setGeometry(QtCore.QRect(100, 180, 171, 30))

        self.combox_1 = QtWidgets.QComboBox(self)
        self.combox_1.setGeometry(QtCore.QRect(100, 240, 171, 30))
        self.combox_1.addItems(["2019","2020","2021","2022","2023","2024","2025","2026","2027","2028","2099"])

        self.combox_2 = QtWidgets.QComboBox(self)
        self.combox_2.setGeometry(QtCore.QRect(100, 300, 171, 30))
        self.combox_2.addItems(["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])

        self.label_1 = QtWidgets.QLabel(self)
        self.label_1.setGeometry(QtCore.QRect(30, 60, 60, 30))
        self.label_1.setText("信用卡号:")

        self.label_6 = QtWidgets.QLabel(self)
        self.label_6.setGeometry(QtCore.QRect(30, 120, 60, 30))
        self.label_6.setText("手机号码:")

        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(30, 180, 60, 30))
        self.label_2.setText("安全码号:")

        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(30, 240, 60, 30))
        self.label_3.setText("到期年份:")

        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(30, 300, 60, 30))
        self.label_4.setText("到期月份:")

        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(60, 340, 200, 30))
        self.label_5.setStyleSheet("color:red;font-size:18px")

        self.listwidget_1 = QListWidget(self)  # 2
        self.listwidget_1.setGeometry(310, 10, 480, 440)
        self.listwidget_1.setStyleSheet("font-size:20px;color:blue")
        self.listwidget_1.doubleClicked.connect(self.clickedlist)
        # self.listwidget_1.doubleClicked.connect(lambda: self.change_func(self.listwidget_1))

        self.show_card()

    def clickedlist(self, qModelIndex):
        index = qModelIndex.row()
        self.listwidget_1.takeItem(index)
        print(index)
        # QMessageBox.information(self, "QListView", "你选择了: " + self.qList[qModelIndex.row()])
        # print("点击的是：" + str(qModelIndex.row()))

    def set_credit_card(self):
        global dataCard
        cardNum = self.lineEdit_1.text().replace(" ", "")
        cardPwd = self.lineEdit_2.text().replace(" ", "")
        phoneNum = self.lineEdit_3.text().replace(" ", "")
        validityYear = self.combox_1.currentText()
        validityMorth = self.combox_2.currentText()
        dataCard = (cardNum, phoneNum, cardPwd, validityYear, validityMorth)
        if cardNum.isnumeric() and cardPwd.isnumeric() and len(cardNum) > 13 and len(cardNum) < 18 and len(phoneNum) == 11:
            self.label_5.setText("")
            self.lineEdit_1.setText("")
            self.lineEdit_2.setText("")
            self.lineEdit_3.setText("")
            self.listwidget_1.addItem(QListWidgetItem("{} {} {} {} {}".format(*dataCard)))
        else:
            self.label_5.setText("请输入正确的信用卡信息！")
            return

    def show_card(self):
        with open("credit_card_info.txt", 'r') as f:
            info = f.read().strip()
            infoList = info.split('\n')
            cardInfos = [x.split(' ') for x in infoList]
            for cardInfo in cardInfos:
                if len(cardInfo) == 5:
                    # print(cardInfo)
                    self.listwidget_1.addItem(QListWidgetItem("{} {} {} {} {}".format(*cardInfo)))

    def closeEvent(self, QCloseEvent):
        res=QMessageBox.question(self,'提示','您确定保存并关闭窗口吗？',QMessageBox.Yes|QMessageBox.No,QMessageBox.No) #两个按钮是否， 默认No则关闭这个提示框
        if res==QMessageBox.Yes:
            QCloseEvent.accept()
            self.save_data()
        else:
            QCloseEvent.ignore()

    def save_data(self):
        with open("credit_card_info.txt", 'w') as f:
            for i in range(self.listwidget_1.count()):
                f.write(self.listwidget_1.item(i).text()+'\n')



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # 创建一个QApplication，也就是你要开发的软件app
    gk = GAKEY()
    gk.show()
    sys.exit(app.exec_())
