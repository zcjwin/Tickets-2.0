
from selenium import webdriver
import time

url = 'http://www.urbtix.hk'
driver = webdriver.Chrome()
driver.get(url)
driver.get('https://ticket.urbtix.hk/internet/memberSignUp')
driver.set_window_size(919, 1160)

# 滑动滚动条到指定元素
ac = driver.find_element_by_id('captchaImage')
driver.execute_script("arguments[0].scrollIntoView();", ac)
time.sleep(0.5)
driver.save_screenshot("imgs/register.png")
# 滑动滚动条到底部
# js = "var q=document.body.scrollTop=100000"
# driver.execute_script(js)

time.sleep(2)
driver.quit()
