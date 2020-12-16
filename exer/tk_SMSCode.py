from tkinter import *
from tkinter import ttk
from threading import Thread
import time

class SMSCode:
    def __init__(self, pnum):
        self.num = 123456
        self.frame = Tk()
        self.frame.resizable(0, 0)
        self.frame.geometry('280x130')
        self.frame.title("输入验证码")
        self.frame.bind('<Return>', self.getinfo)

        self.label_phone = Label(self.frame, text="手机号:")
        self.label_phone.place(y=10,x=20,anchor=NW)

        self.label_phonenum = Label(self.frame, text=pnum)
        self.label_phonenum.place(y=10,x=80,anchor=NW)

        self.label_num = Label(self.frame, text="验证码:")
        self.label_num.place(y=40,x=20,anchor=NW)

        self.text_num = Entry(self.frame, width=20)
        self.text_num.place(y=40,x=80,anchor=NW)

        self.label_hint = Label(self.frame, text="")
        self.label_hint.place(y=65,x=90,anchor=NW)

        self.button_ok = Button(self.frame, text="确定", width=10, command=self.getinfo)
        self.button_ok.place(y=90,x=100,anchor=NW)
        self.frame.mainloop()

    def getinfo(self,evt=None):
        self.num = self.text_num.get() #获取文本框内容
        if len(self.num) == 6 and self.num.isdigit():
            self.frame.destroy()
            return
        self.label_hint["text"] = "请输入正确验证码！"



if __name__ == '__main__':
    code = SMSCode("15839281746")
    print("return:",code.num)
    # time.sleep(10)