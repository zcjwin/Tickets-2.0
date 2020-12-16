from selenium import webdriver
from PIL import Image
import time
import cv2 as cv

def get_page():
    driver = webdriver.PhantomJS(executable_path='phantomjs-2.1.1-windows/bin/phantomjs.exe')
    url = 'http://www.urbtix.hk'
    url2 = 'https://ticket.urbtix.hk/internet/memberSignUp'
    driver.get(url)
    driver.get(url2)
    time.sleep(0.5)
    mem_detail = str(time.time()).replace('.', '')[10:] + 'p01.png'
    driver.save_screenshot(mem_detail)
    # 找到元素的节点
    iva_attr_obj = driver.find_element_by_class_name('member-account-detail-tbl').find_element_by_tag_name('tbody')
    print(iva_attr_obj.location)  # 打印元素的坐标位置
    print(iva_attr_obj.size)      # 打印元素的大小
    left = iva_attr_obj.location['x']
    top = iva_attr_obj.location['y']
    right = iva_attr_obj.location['x'] + iva_attr_obj.size['width']
    bottom = iva_attr_obj.location['y'] + iva_attr_obj.size['height']

    # 298x245
    img = cv.imread(mem_detail)
    r_image = img[top:bottom, left:right]
    cv.imwrite(r"captcha_img\captcha.png",r_image)


    # image = Image.open(mem_detail)
    # image = image.crop((left, top, right, bottom))
    # image.save(str(time.time()).replace('.', '') + 'p01.png')


get_page()