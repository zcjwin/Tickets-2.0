import cv2 as cv
from chaojiying import *

# 距离 298x245  图片大小 205x275
# 截图  宽107:107+314  高414:414+280
def cut_cap_register(filename, uid):
    img = cv.imread(filename)
    r_image = img[245:245+205, 298:298+275]
    cv.imwrite(r"captcha_img\captcha_%s.png" % uid,r_image)

def get_dot_location_register(imgDict):
    try:
        locationList = imgDict['pic_str'].split("|")
        # 宽度-15，高度-121
        dotLocations = []
        for locations in locationList:
            # print("locations:", locations)
            if int(locations.split(",")[-1]) > 145:
                dotLocation = int((int(locations.split(",")[0]) - 9)/50) + 6
            else:
                dotLocation = int((int(locations.split(",")[0]) - 9)/50) + 1
            dotLocations.append(dotLocation)
        # print(dotLocations)
        return dotLocations
    except:
        return False


if __name__ == '__main__':

    uid = ''
    # chaojiying = Chaojiying_Client('zhoujielun', 'zhou123456', "44cc7ed6df07f1233882eaa5996b1b05")	#用户中心>>软件ID 生成一个替换 96001
    filename = "imgs/register.png"
    cut_cap(filename, uid)
    # imgDict = chaojiying.PostPic(r"D:\SK_WORK\WORK\Captcha\out_img\captcha_%s.png" % uid, 9104)
    # dotLocations = get_dot_location(imgDict)


