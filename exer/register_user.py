import sys, time
from threading import Thread
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from random_userinfo import *
from captcha_register import *
import os

class Register():
    def __init__(self):
        self.url = 'http://www.urbtix.hk'
        if not os.path.isdir('imgs'):
            os.mkdir('imgs')

    def registerInfo(self):
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(919, 1160)
        self.wait = WebDriverWait(self.driver, 10, 0.5)
        self.driver.get(self.url)
        with open('infomation2.txt', 'a', encoding='utf-8') as f:
            info_dict = {}
            self.driver.get('https://ticket.urbtix.hk/internet/memberSignUp')
            surname = getSurname()
            self.driver.find_element_by_id('surname').send_keys(surname)
            info_dict['surname'] = surname
            firstName = getfirstName()
            self.driver.find_element_by_id('firstName').send_keys(firstName)
            info_dict['firstName'] = firstName
            contactPhoneNo = getTelNo()
            self.driver.find_element_by_id('contactPhoneNo').send_keys(contactPhoneNo)
            info_dict['contactPhoneNo'] = contactPhoneNo
            emailAddress = getEmail()
            self.driver.find_element_by_id('emailAddress').send_keys(emailAddress)
            info_dict['emailAddress'] = emailAddress
            self.driver.find_element_by_id('emailAddressRetype').send_keys(emailAddress)
            self.loginId = getLoginId()
            self.driver.find_element_by_id('loginId').send_keys(self.loginId)
            info_dict['loginId'] = self.loginId
            self.driver.find_element_by_id('password').send_keys('abcDEF123456')
            info_dict['password'] = 'abcDEF123456'
            self.driver.find_element_by_id('passwordRetype').send_keys('abcDEF123456')
            # 滑动滚动条到指定元素
            ac = self.driver.find_element_by_id('captchaImage')
            self.driver.execute_script("arguments[0].scrollIntoView();", ac)
            # 滑动滚动条到底部
            # js = "var q=document.body.scrollTop=100000"
            # self.driver.execute_script(js)
            time.sleep(0.2)
            print("imgs/register_%s.png" % self.loginId)
            self.driver.save_screenshot("imgs/register_%s.png" % self.loginId)
            time.sleep(0.2)
            cut_cap("imgs/register_%s.png" % self.loginId, self.loginId)
            time.sleep(0.2)


            # 接受服务条款按钮
            self.driver.find_element_by_id('checkbox-tnc').click()
            # 点击确定按钮
            self.driver.find_element_by_xpath('//form/div/div/div[@id="button-confirm"]/div/div/span').click()
            # 判断是否注册成功
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'confirmation-message')))
                self.driver.find_element_by_class_name('confirmation-message')
                if self.driver.find_element_by_class_name('confirmation-message'):
                    f.write(str(info_dict) + '\n')
                    print(info_dict['loginId'],':会员注册成功')
                    self.driver.quit()
                    sys.exit()
            except Exception:
                print("会员注册失败！")

    def captcha(self):
        if not os.path.isdir("captcha_img"):
            os.mkdir("captcha_img")
        filename = r"captcha_img\tickets_login_%s.png" % self.username
        chaojiying = Chaojiying_Client('zhoujielun', 'zhou123456', "44cc7ed6df07f1233882eaa5996b1b05")  # 用户中心>>软件ID 生成一个替换 96001
        self.driver.save_screenshot(filename)   # 截图并保存到指定路径
        cut_cap_register(filename, self.username)        # 切割出验证码
        im = open(r"captcha_img\captcha_%s.png" % self.username, 'rb').read()
        imgDict = chaojiying.PostPic(im, 9104)  # 获取验证码信息字典
        # print(imgDict)
        dotLocations = get_dot_location(imgDict)  # 得到点坐标
        if dotLocations:
            for i in dotLocations:
                if int(i) > 5:
                    h, w = 2, int(i) - 5
                else:
                    h, w = 1, int(i)
                self.driver.find_element_by_xpath("//td[@id='captcha-image-input-key-container']/table/tbody/tr[%s]/td[%s]/img" % (h, w)).click()
            print(dotLocations)
        else:
            my_attr['loginStatus'].append(self.username + "：登陆失败！")
            self.driver.save_screenshot(r"captcha_img\login_lose_%s.png" % self.username)
            self.driver.quit()
            sys.exit()
        self.driver.save_screenshot(r"captcha_img\login_later_%s.png" % self.username)   # 保存登陆后截图


if __name__ == "__main__":
    threads = []
    for thr in range(3):
        uper = Register()
        Thread_name = Thread(target=uper.registerInfo)
        threads.append(Thread_name)
    for i in range(3):
        threads[i].start()
