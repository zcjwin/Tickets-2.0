from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import time,json


def get_Online_Payment_url(url):
    opt = webdriver.ChromeOptions()
    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'performance': 'ALL'}
    driver = webdriver.Chrome(desired_capabilities=d)
    driver.get(url)
    opt.arguments
    for entry in driver.get_log('performance'):
        datainfo = json.loads(entry['message'])
        print(datainfo)
        if 'documentURL' in datainfo['message']['params']:
            if 'https://cashier.95516.com/b2c/api/unifiedOrder.action?tn=' in datainfo['message']['params']['documentURL']:
                print(datainfo['message']['params']['documentURL'])
    # driver.find_element_by_id('expireMonth').send_keys('09')  # 取票密码
    # driver.find_element_by_id('expireYear').send_keys('22')  # 重复取票密码
    # driver.find_element_by_id('cvn2').send_keys('126')  # 输入银行卡号
    # driver.find_element_by_id('cellPhoneNumber').send_keys('15836958746')  # 输入银行卡号
    # driver.find_element_by_id('btnGetCode').click()  # 输入银行卡号
    time.sleep(100)
    driver.quit()


url = 'http://www.urbtix.hk/'
get_Online_Payment_url(url)