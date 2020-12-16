import datetime
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from random_userinfo import *
from captcha_register import *
from captcha import *
from tkinter import *
from tkinter import ttk
import os, sys, time, json
import random

dataCard = tuple()
my_attr = {
    'registerStatus' : [],
    'loginStatus' : [],
    'buyRecord' : [],
    'buyStatus' : [],
    "selSeatUrl" : [],
    'selPrice' : [],
    'cardInfos' : [],
    'cardInfo' : tuple(),
    'selNum' : 1,
    'gross' : -1,
    }

class BuyUrbtix:
    def __init__(self):
        self.url = 'http://www.urbtix.hk'

    def openSite(self,username,ip):
        # test()
        d = DesiredCapabilities.CHROME
        d['loggingPrefs'] = {'performance': 'ALL'}
        self.username = username
        self.opt = webdriver.ChromeOptions()
        # 隐藏界面
        # self.opt.headless = True
        # 设置代理
        # porxy = "--proxy-server=socks5://{}".format(ip)
        # self.opt.add_argument(porxy)
        # 创建浏览器对象
        self.driver = webdriver.Chrome(desired_capabilities=d,chrome_options=self.opt)
        # 无头浏览器
        # self.driver = webdriver.PhantomJS(executable_path='phantomjs-2.1.1-windows/bin/phantomjs.exe')

        self.driver.set_window_size(919,1160)
        self.wait = WebDriverWait(self.driver, 10, 0.5)
        self.driver.get(self.url)
        self.login()

    def login(self):
        # 访问登录界面url
        self.driver.get("https://ticket.urbtix.hk/internet/login/memberLogin")
        if datetime.datetime.now().hour == 9 and datetime.datetime.now().minute > 35:
            my_attr['loginStatus'].append(self.username + "：等待登录！")
        while True:
            if datetime.datetime.now().hour == 9 and datetime.datetime.now().minute > 35:
                pass
            else:
                my_attr['loginStatus'].append(self.username + "：开始登录！")
                break
            time.sleep(1)

        for _ in range(10):  # 循环等待10秒加载页面
            try:
                self.driver.find_element_by_id('j_username').clear()
                self.driver.find_element_by_id('j_username').send_keys(self.username)
                self.driver.find_element_by_id('j_password').clear()
                self.driver.find_element_by_id('j_password').send_keys('abcDEF123456')
                break
            except:
                time.sleep(2)
                self.driver.get(self.url)
                self.driver.get("https://ticket.urbtix.hk/internet/login/memberLogin")
        else:
            my_attr['loginStatus'].append(self.username + "：登陆失败！")
            self.driver.quit()
            sys.exit()
        # time.sleep(30)
        dotLocations = self.captcha()
        for _ in range(5):
            if dotLocations:
                for i in dotLocations:
                    if int(i) > 5:
                        h, w = 2, int(i) - 5
                    else:
                        h, w = 1, int(i)
                    try:
                        self.driver.find_element_by_xpath("//td[@id='captcha-image-input-key-container']/table/tbody/tr[%s]/td[%s]/img" % (h, w)).click()
                    except:
                        self.driver.get("https://ticket.urbtix.hk/internet/login/memberLogin")
                        break
                self.driver.find_element_by_class_name('btn-inner-blk').click()
                # 账号已经在线登录的话点击确定继续登录
                try:
                    self.driver.find_element_by_id('concurrent-login-yes').click()
                except Exception:
                    pass
                self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'mem-login-state-link')))
                dr = self.driver.find_element_by_class_name('mem-login-state-link').text
                if dr == "登出":  # 登录成功
                    my_attr['loginStatus'].append(self.username + "：登陆成功！")
                    time.sleep(0.1)
                    self.wait_search()  # 循环等待用户输入
                    self.performanceDetail()  # 购买正价票
                    break
                if dr == "登入":
                    time.sleep(0.2)
            self.driver.find_element_by_id('j_username').clear()
            self.driver.find_element_by_id('j_username').send_keys(self.username)
            self.driver.find_element_by_id('j_password').clear()
            self.driver.find_element_by_id('j_password').send_keys('abcDEF123456')
            dotLocations = self.captcha()
        else:
            my_attr['loginStatus'].append(self.username + "：登陆失败！")
            self.driver.quit()
            sys.exit()
        self.driver.save_screenshot(r"captcha_img\login_later_%s.png" % self.username)   # 保存登陆后截图

    def captcha(self):
        time.sleep(0.5)
        if not os.path.isdir("captcha_img"):
            os.mkdir("captcha_img")
        filename = r"captcha_img\tickets_login_%s.png" % self.username
        chaojiying = Chaojiying_Client('zhoujielun', 'zhou123456', "44cc7ed6df07f1233882eaa5996b1b05")  # 用户中心>>软件ID 生成一个替换 96001
        self.driver.save_screenshot(filename)   # 截图并保存到指定路径
        cut_cap(filename, self.username)        # 切割出验证码
        im = open(r"captcha_img\captcha_%s.png" % self.username, 'rb').read()
        imgDict = chaojiying.PostPic(im, 9104)  # 获取验证码信息字典
        # print(imgDict)
        return get_dot_location(imgDict)  # 得到点坐标

    # 循环等待用户输入
    def wait_search(self):
        while True:
            if my_attr['selSeatUrl'] and my_attr['selNum']:
                break
            time.sleep(0.5)

    def performanceDetail(self):
        # 选择购买正价票数量
        session = random.choice(my_attr['selSeatUrl'])          # 购买场次
        num = int(random.choice(str(my_attr['selNum'])))        # 购买数量
        priceIndex = int(random.choice(my_attr['selPrice']))    # 购买价格区间id
        # print(session, num, priceIndex)
        # my_attr['buyStatus'].append("%s: 开始购买 价格索引 %s 的场次数量为 %s" % (self.username, priceIndex, num))
        while True:
            try:
                self.driver.get(session)  # 打开选择场次页
                self.driver.find_elements_by_class_name('pricezone-radio-input')[priceIndex].click()  # 选择票区
                time.sleep(0.2)
                Select(self.driver.find_element_by_class_name('chzn-select')).select_by_index(num)  # 选择购买数量
                self.driver.find_element_by_id('adjacent-seats-chk').click()  # 取消相连座位
                self.driver.find_element_by_class_name('btn-inner-blk').click()  # 点击快速购票
                self.driver.find_element_by_xpath("//form[@id='reviewTicketForm']/div[@class='ticket-review-confirm-btn']/div[@class='btn-outer-blk cursor-pointer']/div[@class='btn-inner-blk']").click()  # 点击加入购物篮
                break
            except Exception as err:
                # print(num,priceIndex)
                # my_attr['buyStatus'].append(str(err))
                num -= 1
                if num <= 0:
                    num = int(random.choice(str(my_attr['selNum'])))
                    priceIndex += 1
                    if priceIndex >= len(my_attr['selPrice']):
                        self.driver.find_element_by_class_name('mem-login-state-link').click()
                        my_attr['buyStatus'].append(self.username + "：购买失败！")
                        self.driver.quit()
                        sys.exit()
            time.sleep(0.2)

        try:
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ticket-review-tbl')))
            self.driver.find_element_by_id('checkbox-not-adjacent').click()
        except Exception as err:
            pass

        while True:
            try:
                self.driver.find_element_by_xpath('//form/table/tbody/tr/td/div[@id="checkout-btn"]/div/div[@class="btn-inner-blk"]/span').click()
                break
            except:
                self.driver.find_element_by_xpath("//form/div/div/div[@class='btn-inner-blk']").click()  # 点击加入购物篮
                time.sleep(0.1)

        while True:
            try:
                # 选择取票方式设置为自动取票机取票
                Select(self.driver.find_element_by_id('delivery-method-select')).select_by_index(1)
                # 选择付款方法
                self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ddTitleText')))
                self.driver.find_element_by_class_name('ddTitleText').click()
                choose_pay = self.driver.find_element_by_id('payment-type-select_child')
                enable_pay = choose_pay.find_element_by_tag_name('ul')
                # self.driver.find_elements_by_xpath("//img[@alt='萬事達卡']").click()
                pay = enable_pay.find_elements_by_tag_name('li')
                time.sleep(0.1)
                pay[4].click()  # 万事达卡
                break
            except Exception as err:
                self.driver.get('https://ticket.urbtix.hk/internet/secure/form/shoppingCart')
                time.sleep(0.1)

        # cardInfo = CardInfo()                  # 每个线程让用户输入信用卡信息
        cardInfo = get_credit_card_info()      # 读取用户提前输入的信用卡信息
        creditCard = cardInfo[0]
        userinfo = cardInfo[1:]

        for _ in range(20):
            try:
                self.driver.find_element_by_id('input-claim-password').clear()                      # 清空输入框
                self.driver.find_element_by_id('input-claim-password').send_keys(123456)            # 取票密码
                self.driver.find_element_by_id('input-claim-password-retype').clear()               # 清空输入框
                self.driver.find_element_by_id('input-claim-password-retype').send_keys(123456)     # 重复取票密码
                self.driver.find_element_by_id('input-card-number').clear()                         # 清空输入框
                self.driver.find_element_by_id('input-card-number').send_keys(creditCard)           # 输入银行卡号
                self.driver.find_element_by_id('button-confirm').click()                            # 点击购买
                break
            except Exception as err:
                print("Error:",err)
                time.sleep(0.2)
        else:
            my_attr['buyStatus'].append(self.username + "：购买失败！")
            self.driver.get('https://ticket.urbtix.hk/internet/logout')
            self.driver.quit()
            sys.exit()

        for _ in range(20):
            try:
                self.driver.find_element_by_id('checkbox-tnc').click()              # 同意协议
                self.driver.find_element_by_id('button-confirm').click()           # 点击购买
                break
            except Exception as err:
                print("Error:",err)

        for entry in self.driver.get_log('performance'):
            datainfo = json.loads(entry['message'])
            if 'documentURL' in datainfo['message']['params']:
                if 'https://cps.cityline.com.hk/CPSPayment/APIPaymentRequest?' in datainfo['message']['params']['documentURL']:
                    self.driver.get(datainfo['message']['params']['documentURL'])
                    self.driver.get('https://ticket.urbtix.hk/internet/secure/transaction/process')

        validMonth = userinfo[3]
        validYear = userinfo[2][-2:]
        safetyCode = userinfo[1]
        phoneNum = userinfo[0]
        self.driver.find_element_by_id('expireMonth').send_keys(validMonth)    # 有效期 月
        self.driver.find_element_by_id('expireYear').send_keys(validYear)     # 有效期 年
        self.driver.find_element_by_id('cvn2').send_keys(safetyCode)          # 安全码后三位
        try:
            self.driver.find_element_by_id('cellPhoneNumber').send_keys(phoneNum)   # 手机号
        except:
            pass
        # self.driver.find_element_by_id('btnGetCode').click()             # 点击发送验证码
        smsCode = self.get_smsCode(phoneNum)
        self.driver.find_element_by_id('smsCode').send_keys(smsCode)     # 输入验证码
        self.driver.find_element_by_id('btnCardPay').click()             # 点击付款


        time.sleep(900)
        self.driver.quit()

        # for entry in self.driver.get_log('performance'):
        #     datainfo = json.loads(entry['message'])
        #     # print(datainfo['message']['params'])
        #     if 'documentURL' in datainfo['message']['params']:
        #         if 'https://cashier.95516.com/b2c/api/unifiedOrder.action?tn=' in datainfo['message']['params']['documentURL']:
        #             paymentPageUrl = datainfo['message']['params']['documentURL']
        #             self.driver.quit()
                    # print(datainfo)
                    # self.Payment(paymentPageUrl, userinfo)

    def get_smsCode(self, phoneNum):
        smsCode = SMSCode(phoneNum)
        return smsCode.num

    def Payment(self, url, userinfo):
        validMonth = userinfo[3]
        validYear = userinfo[2][-2:]
        safetyCode = userinfo[1]
        phoneNum = userinfo[0]
        driverPay = webdriver.Chrome()
        driverPay.get(url)
        driverPay.find_element_by_id('expireMonth').send_keys(validMonth)    # 有效期 月
        driverPay.find_element_by_id('expireYear').send_keys(validYear)     # 有效期 年
        driverPay.find_element_by_id('cvn2').send_keys(safetyCode)          # 安全码后三位
        try:
            driverPay.find_element_by_id('cellPhoneNumber').send_keys(phoneNum)   # 手机号
        except:
            pass
        driverPay.find_element_by_id('btnGetCode').click()             # 点击发送验证码
        time.sleep(900)
        driverPay.quit()

        # # 判断是否付款成功
        # try:
        #     self.driver.find_element_by_class_name('')
        #     my_attr['buyStatus'].append(self.username + "：购买成功！")
        #     print(self.username + ":购买成功!")
        #     self.driver.save_screenshot(r"captcha_img\over_%s.png" % self.username)  # 程序执行结束截图
        #
        # except :
        #     my_attr['buyStatus'].append(self.username + "：购买失败！")
        #     print(self.username + ":购买失败!")
        #     self.driver.save_screenshot(r"captcha_img\over_%s.png" % self.username)  # 程序执行结束截图
        #
        #
        #
        # # 付款失败执行
        # try:
        #     dialog_box = self.driver.find_element_by_class_name('ui-dialog-buttonset')
        #     dialog_box.find_element_by_class_name('ui-button-text').click()
        #     self.driver.save_screenshot(r"captcha_img\over_%s.png" % self.username)  # 程序执行结束截图
        #     time.sleep(0.5)
        #
        # except Exception:
        #     self.driver.save_screenshot(r"captcha_img\over_%s.png" % self.username)  # 程序执行结束截图
        #     time.sleep(20)
        #     self.driver.quit()
        #     sys.exit()

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

    def getinfo(self):
        self.num = self.text_num.get() #获取文本框内容
        if len(self.num) == 6 and self.num.isdigit():
            self.frame.destroy()
        self.label_hint["text"] = "请输入正确验证码！"


class CardInfo:
    def __init__(self):
        self.frame = Tk()
        self.frame.resizable(0,0)
        self.frame.geometry('280x130')
        self.frame.title("输入银行卡信息")

        self.label_num = Label(self.frame, text="信用卡号:")
        self.label_pwd = Label(self.frame, text="安全码号:")
        self.label_year = Label(self.frame, text="有效年份:")
        self.label_month = Label(self.frame, text="有效月份:")

        self.text_num = Entry(self.frame, width=30)
        self.text_pwd = Entry(self.frame, width=30)
        # self.text_year = Entry(self.frame, width=30)
        # self.text_month = Entry(self.frame, width=30)

        self.label_num.grid(row=0, column=0)
        self.label_pwd.grid(row=1, column=0)
        self.label_year.grid(row=2, column=0)
        self.label_month.grid(row=3, column=0)

        self.button_ok = Button(self.frame, text="确定", width=10,command=self.getinfo)

        self.text_num.grid(row=0, column=1)
        self.text_pwd.grid(row=1, column=1)
        # self.text_year.grid(row=2, column=1)
        # self.text_month.grid(row=3, column=1)

        self.button_ok.grid(row=4, column=1)
        # 创建一个下拉列表
        yearList = StringVar()
        self.text_year = ttk.Combobox(self.frame, width=27, textvariable=yearList)
        self.text_year['values'] = ['{}'.format(i) for i in range(datetime.datetime.now().year,datetime.datetime.now().year+11)] # 设置下拉列表的值
        self.text_year.grid(row=2, column=1)  # 设置其在界面中出现的位置  column代表列   row 代表行
        self.text_year.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值

        # 创建一个下拉列表
        monthList = StringVar()
        self.text_month = ttk.Combobox(self.frame, width=27, textvariable=monthList)
        self.text_month['values'] = ['{0:0>2}'.format(i) for i in range(1,13)]  # 设置下拉列表的值
        self.text_month.grid(row=3, column=1)  # 设置其在界面中出现的位置  column代表列   row 代表行
        self.text_month.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值

        self.frame.mainloop()


    def getinfo(self):
        num = self.text_num.get() #获取文本框内容
        pwd = self.text_pwd.get() #获取文本框内容
        year = self.text_year.get() #获取文本框内容
        month = self.text_month.get() #获取文本框内容
        my_attr['cardInfo'] = (num,pwd,year,month)
        self.frame.quit()


class Register():
    def __init__(self):
        self.url = 'http://www.urbtix.hk'

    def registerInfo(self):
        # self.driver = webdriver.Chrome()
        self.driver = webdriver.PhantomJS(executable_path='phantomjs-2.1.1-windows/bin/phantomjs.exe')
        self.wait = WebDriverWait(self.driver, 10, 0.5)
        self.driver.get(self.url)
        with open('infomation.txt', 'a', encoding='utf-8') as f:
            for _ in range(5):
                try:
                    info_dict = {}
                    self.driver.get('https://ticket.urbtix.hk/internet/memberSignUp')
                    surname = getSurname()
                    self.driver.find_element_by_id('surname').clear()
                    self.driver.find_element_by_id('surname').send_keys(surname)
                    info_dict['surname'] = surname
                    firstName = getfirstName()
                    self.driver.find_element_by_id('firstName').clear()
                    self.driver.find_element_by_id('firstName').send_keys(firstName)
                    info_dict['firstName'] = firstName
                    contactPhoneNo = getTelNo()
                    self.driver.find_element_by_id('contactPhoneNo').clear()
                    self.driver.find_element_by_id('contactPhoneNo').send_keys(contactPhoneNo)
                    info_dict['contactPhoneNo'] = contactPhoneNo
                    emailAddress = getEmail()
                    self.driver.find_element_by_id('emailAddress').clear()
                    self.driver.find_element_by_id('emailAddress').send_keys(emailAddress)
                    info_dict['emailAddress'] = emailAddress
                    self.driver.find_element_by_id('emailAddressRetype').clear()
                    self.driver.find_element_by_id('emailAddressRetype').send_keys(emailAddress)
                    self.loginId = getLoginId()
                    self.driver.find_element_by_id('loginId').clear()
                    self.driver.find_element_by_id('loginId').send_keys(self.loginId)
                    info_dict['loginId'] = self.loginId
                    self.driver.find_element_by_id('password').clear()
                    self.driver.find_element_by_id('password').send_keys('abcDEF123456')
                    info_dict['password'] = 'abcDEF123456'
                    self.driver.find_element_by_id('passwordRetype').clear()
                    self.driver.find_element_by_id('passwordRetype').send_keys('abcDEF123456')
                    dotLocations = self.captcha()
                    # dotLocations = ['1','2','3','4']
                    if dotLocations:
                        for i in dotLocations:
                            if int(i) > 5:
                                h, w = 2, int(i) - 5
                            else:
                                h, w = 1, int(i)
                            self.driver.find_element_by_xpath("//td[@id='captcha-image-input-key-container']/table/tbody/tr[%s]/td[%s]/img" % (h, w)).click()
                    time.sleep(0.2)
                    # 接受服务条款按钮
                    self.driver.find_element_by_id('checkbox-tnc').click()
                    # 点击确定按钮
                    self.driver.find_element_by_xpath('//form/div/div/div[@id="button-confirm"]/div/div/span').click()
                    # 判断是否注册成功
                    self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'confirmation-message')))
                    self.driver.find_element_by_class_name('confirmation-message')
                    if self.driver.find_element_by_class_name('confirmation-message'):
                        f.write(str(info_dict) + '\n')
                        my_attr['registerStatus'].append(self.loginId + ':会员注册成功')
                        print(info_dict['loginId'], ':会员注册成功')
                        self.driver.save_screenshot(r"captcha_img\register_later_%s.png" % self.loginId)  # 保存登陆后截图
                        self.driver.quit()
                        sys.exit()
                    break
                except Exception:
                    self.driver.get(self.url)
                    time.sleep(0.2)
            else:
                my_attr['registerStatus'].append("会员注册失败！")
                self.driver.quit()
                print("会员注册失败！")
                sys.exit()

    def captcha_old(self):
        time.sleep(0.5)
        chaojiying = Chaojiying_Client('zhoujielun', 'zhou123456', "44cc7ed6df07f1233882eaa5996b1b05")  # 用户中心>>软件ID 生成一个替换 96001
        if not os.path.isdir("captcha_img"):
            os.mkdir("captcha_img")
        filename = r"captcha_img/tickets_register_%s.png" % self.loginId   #  设置文件名
        self.driver.save_screenshot(filename)   # 截图并保存到指定路径
        cut_cap_register(filename, self.loginId)        # 切割出验证码
        im = open(r"captcha_img\captcha_%s.png" % self.loginId, 'rb').read()
        imgDict = chaojiying.PostPic(im, 9104)  # 获取验证码信息字典
        # print(imgDict)
        return get_dot_location_register(imgDict)  # 得到点坐标

    def captcha(self):
        time.sleep(0.5)
        chaojiying = Chaojiying_Client('zhoujielun', 'zhou123456', "44cc7ed6df07f1233882eaa5996b1b05")  # 用户中心>>软件ID 生成一个替换 96001
        if not os.path.isdir("captcha_img"):
            os.mkdir("captcha_img")
        filename = r"captcha_img/tickets_register_%s.png" % self.loginId   #  设置文件名
        self.driver.save_screenshot(filename.replace('register','home'))
        # 找到元素的节点
        iva_attr_obj = self.driver.find_element_by_class_name('member-account-detail-tbl').find_element_by_tag_name('tbody')
        left = iva_attr_obj.location['x']
        top = iva_attr_obj.location['y']
        right = iva_attr_obj.location['x'] + iva_attr_obj.size['width']
        bottom = iva_attr_obj.location['y'] + iva_attr_obj.size['height']
        img = cv.imread(filename.replace('register','home'))
        r_image = img[top:bottom, left:right]
        cv.imwrite(filename, r_image)
        cut_cap_register(filename, self.loginId)        # 切割出验证码
        im = open(r"captcha_img\captcha_%s.png" % self.loginId, 'rb').read()
        imgDict = chaojiying.PostPic(im, 9104)  # 获取验证码信息字典
        # print(imgDict)
        return get_dot_location_register(imgDict)  # 得到点坐标

def get_credit_card_info():
    try :
        with open("credit_card_info.txt", 'r') as f:
            info = f.read().rstrip()
            infoList = info.split('\n')
            cardInfos = [x.split(' ') for x in infoList]
            cardInfo = random.choice(cardInfos)
            time.sleep(0.2)
            return cardInfo
    except Exception:
        my_attr['buyStatus'] = "请先输入信用卡信息,再打开该程序。"



# 返回登录日志
def login_record():
    while 1:
        if my_attr['loginStatus']:
            return my_attr['loginStatus']
        time.sleep(0.1)


# 返回购买日志
def buy_record():
    while 1:
        if my_attr['buyStatus']:
            return my_attr['buyStatus']
        time.sleep(0.1)

# 返回注册日志
def register_record():
    while 1:
        if my_attr['registerStatus']:
            return my_attr['registerStatus']
        time.sleep(0.1)

if __name__ == '__main__':
    pass
    # get_credit_card_info()
    # random_card_info()


