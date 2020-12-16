# coding:utf-8

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0


def z_get_href_by_partial_link_text(str):
    try:
        var = driver.find_element_by_partial_link_text(str)
        return var.get_attribute("href")
    except:
        return ''


d = DesiredCapabilities.CHROME
d['loggingPrefs'] = {'performance': 'ALL'}
driver = webdriver.Chrome(desired_capabilities=d)

driver.get("http://www.csdn.net")

print("Title: " + driver.title)

login_key = ['登录', '登陆', '登入', 'login', 'Login', 'LOGIN']
reg_key = ['注册', '加入', '新账户', 'register', 'Register', 'REG']
findpass_key = ['找回密码', '忘记密码']

register_u = ''
login_u = ''
findpass_u = ''

driver.find_element_by_partial_link_text("注册").click()
# driver.find_element_by_partial_link_text("账号登录").click()


for entry in driver.get_log('performance'):
    print(entry)
