
from lxml import etree
import requests
import re, json
import datetime

t = datetime.datetime.now()
nowDate = [t.year, t.month, t.day, t.hour]


# 获取当前时间的所有场次
def get_session_url(url):
    sessionList = []
    keepSession = requests.session()
    keepSession.get(url='http://www.urbtix.hk/')
    keepSession.get('http://www.urbtix.hk/other')
    searchRes = keepSession.get(url=url)
    try:
        # 创建解析对象
        parseHtml = etree.HTML(searchRes.text)
        # 调用xpath返回结束,text()为文本内容
        mainXpath = parseHtml.xpath('''//div[@id="evt-info-blk"]/div[2]//tr''')
        for index in mainXpath:
            dId = index.xpath('''td/div/img/@data-evt_id''')[0]
            sId = index.xpath('''td/div/img/@data-perf_id''')[0]
            sDate = index.xpath('td/div/div/text()')
            sTime = index.xpath('td[2]/span/text()')
            sName = index.xpath('td[3]/text()')
            sDate = [x.replace('\t','').replace('\r\n','') for x in sDate]
            sTime = [x.replace('\t','').replace('\r\n','') for x in sTime]
            sName = [x.replace('\t','').replace('\r\n','') for x in sName]
            sDateTime = "%s年%s%s日%s%s" % (sDate[-1],sDate[0],sDate[1],sDate[2],sTime[0])
            sessionList.append({'eventUrl':'https://ticket.urbtix.hk/internet/zh_TW/secure/event/%s/performanceDetail/%s' % (dId, sId),'eventDateName':sDateTime+"-"+sName[0]})
    except:
        html = searchRes.text
        try:
            DateSale = re.findall('售日期: (.*?)年(.*?)月(.*?)日 上午(.*?)時<',html)[0]   # 开售时间
            saleDate = [date for date in DateSale]
            isSale = '未开售--> '
        except:
            isSale = ''
        datainfo_list = re.findall('month">(.*?)<.*?"date">(.*?)<.*?class="day">(.*?)<.*?class="year">(.*?)<.*?<span>(.*?)<.*?"perf-name-col">(.*?)<.*?class=.*?id=.*?data-evt_id="(.*?)".*?data-perf_id="(.*?)"',html,re.S)
        datainfo_set = eval(str(datainfo_list).replace(r'\r','').replace(r'\t','').replace(r'\n',''))
        for datainfo in datainfo_set:
            sDateTime = "%s年%s%s日%s%s" % (datainfo[3], datainfo[0], datainfo[1], datainfo[2], datainfo[4])
            if isSale:
                sessionList.append({'eventUrl': 'https://ticket.urbtix.hk/internet/zh_TW/secure/event/%s/performanceDetail/%s' % (datainfo[-2], datainfo[-1]),'eventDateName': isSale + sDateTime + "-" + datainfo[-3], 'saleDate' : saleDate})
            else:
                sessionList.append({'eventUrl': 'https://ticket.urbtix.hk/internet/zh_TW/secure/event/%s/performanceDetail/%s' % (datainfo[-2], datainfo[-1]),'eventDateName': isSale + sDateTime + "-" + datainfo[-3]})

    # print(sessionList)
    return sessionList
    # [{'url': 'https://ticket.urbtix.hk/internet/zh_TW/secure/event/38245/performanceDetail/371710',
    # 'date': '2019年八月16日 星期五下午8時',
    # 'name': '風車草劇團《尋常心》- 葵青劇院場地伙伴計劃節目'}]

# 获取搜索到内容所有场次url
def get_date_url(keyword):
    sessionList = []
    keepSession = requests.session()
    keepSession.get(url='http://www.urbtix.hk/')
    keepSession.get('http://www.urbtix.hk/other')
    searchRes = keepSession.get(url='https://ticket.urbtix.hk/internet/eventSearch/keyword?', params={'keyword':keyword})
    # print(searchRes.text)
    eventListJSON = re.findall(r'eventListJSON = (.*?);', searchRes.text)
    # open('html.html','wb').write(searchRes.content)
    eventListDict = json.loads(eventListJSON[0])
    for event in eventListDict:
        eventUrl = "https://ticket.urbtix.hk/internet/zh_TW/eventDetail/" + str(event['eventId'])
        sessionList += get_session_url(eventUrl)
        for sDict in sessionList:
            priceList = [str(i) for i in eventListDict[0]['priceList']]
            sDict['priceList'] = priceList
    # print(sessionList)
    return sessionList
    # [{'eventUrl': 'https://ticket.urbtix.hk/internet/zh_TW/eventDetail/38245', 'eventDate': '2019/08/16-18, 20-22, 24-25', 'eventName': '風車草劇團《尋常心》- 葵青劇院場地伙伴計劃節目'}, {'eventUrl': 'https://ticket.urbtix.hk/internet/zh_TW/eventDetail/38350', 'eventDate': '2019/08/23-25', 'eventName': '風車草劇團《尋常心》- 葵青劇院場地伙伴計劃節目 (加場)'}]

def get_ip_list(num):
    url = r"http://api.wandoudl.com/api/ip?app_key=983f239649581e0c6b4c1da74eee5fff&pack=205087&num={}&xy=3&type=1&lb=\r\n&mr=1&".format(num)
    ip_text = requests.get(url)
    return ip_text.text.split('\r\n')

if __name__ == '__main__':
    keyword = input("请输入搜索内容：")
    data_list = get_date_url(keyword)
    for data in data_list:
        print(data)
    # get_session_url('https://ticket.urbtix.hk/internet/zh_TW/eventDetail/38245')

