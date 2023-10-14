# SEO环境： schedule
import warnings
warnings.filterwarnings('ignore')
import requests
import pandas as pd
import numpy as np
import json
import time
import datetime
import xlwings as xw
import telebot
import hmac, base64, struct, hashlib
import math
import threading
import multiprocessing


start = int(time.time())

pd.set_option('display.max_colwidth', None) #显示单元格完整信息
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

day = -1
pages_user = 150
pages_fircharge = 60
pages_fircharge_two = 100
pages_trade = 150

url_trade ='http://fundmng.bsportsadmin.com/api/manage/data/balance/record/list'
url_fircharge = 'http://fundmng.bsportsadmin.com/api/manage/data/detail/firstRecharge'
url_user = 'http://fundmng.bsportsadmin.com/api/manage/user/maintain/user/list'
url_huiyuan = 'http://fundmng.bsportsadmin.com/api/manage/data/loss/user/manage/list'  #会员流失

daili = pd.read_excel(r'C:\Users\User\Desktop\SEO\SEO提单数据\1011\代理线.xlsx')
# 第一次获取token
submit_url = 'http://fundmng.bsportsadmin.com/api/manage/user/admin/login/submit'
header0 = {
    'Accept':'application/json, text/plain, */*',
    # 'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'Content-Length':'48',
    'Content-Type':'application/x-www-form-urlencoded',
    'Cookie':'admin-uid=690; admin-token=db76bebda5274c80adaadd40bd794f24',
    'Device_id':'1.0',
    'Gl_version':'2.0',
    'Host':'fundmng.bsportsadmin.com',
    'Language':'zh_CN',
    'Origin':'http://fundmng.bsportsadmin.com',
    'Os_type':'0',
    'Referer':'http://fundmng.bsportsadmin.com/login',
    'Sign':'2bc4c378817f47731f0adf450a627d19',
    'Some':'header',
    'Systemid':"",
    'Timestamp':'1692415901000',
    'Token':'-1',
    'Uid':'-1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'Version':'1.0'
}
def get_google_code(secret):
    key = base64.b32decode(secret, True)
    msg = struct.pack(">Q", int(time.time()) // 30)
    google_code = hmac.new(key, msg, hashlib.sha1).digest()
    # 很多网上的代码不可用，就在于这儿，没有chr字符串
    o = ord(chr(google_code[19])) & 15
    # google_code = (struct.unpack(">I", google_code[o:o + 4])[0] & 0x7fffffff) % 1000000
    google_code = (struct.unpack(">I", google_code[o:o + 4])[0] & 0x7fffffff) % 1000000
    return '%06d' % google_code


# 采集会员流失统计表
# token
data0 = {
    'username': 'Marquis',
    'password': 'qwer123456',
    'code': get_google_code('64ehnxj6yily5bhv23kgb62ozuh6yuu2')
}
session0 = requests.Session()
response0  =session0.post(url=submit_url,data=data0,headers=header0)
response0.encoding = 'utf-8'
obj0 = json.loads(response0.text)
token = obj0['data']['token']

header = {
    'Device_id':'1.0',
    'Os_type':'0',
    'Referer':'http://fundmng.bsportsadmin.com/system/statistics/member-loss',
    'Sign':'6f518a02e3479ecaaf4ec58b3e5b3878',
    'Timestamp':'1697073050000',
    'Token':token,
    'Uid':'690',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Version':'1.0'
}
# 总条数
data_init = {
    'page': 1,
    'size': 20,
    'vipLevel': 0,
    'regStartTime': 1601481600000,
    'regEndTime': int(time.time())*1000,
}
#获取会员流失页码
session = requests.session()
response = session.post(url=url_huiyuan,data=data_init,headers=header)
obj_init = json.loads(response.text)
n_data = obj_init['data']['total']
print('总条数：',n_data)
pages = math.ceil(n_data/500)
print('总页码：',pages)

page_list = []
for i in range(0,pages,pages//10):
    page_list.append(i)
page_list[10]=pages

def huiyuan_q_fun(start_page,end_page):
    dic_huiyuan = {'会员账号':[],'代理':[],'vip等级':[],'首存时间':[]}
    for page in range(start_page,end_page+1):
        # 获取页码数量
        print(f'第{page}页。。。')
        data = {
            'page': page,
            'size': 500,
            'vipLevel': 0,
            'regStartTime': 1601481600000,
            'regEndTime': int(time.time())*1000,
        }
        response = session.post(url=url_huiyuan,data=data,headers=header)
        response.encoding='utf8'
        obj = json.loads(response.text)

        for i in obj['data']['dataList']:
            dic_huiyuan['会员账号'].append(i['userName'])
            dic_huiyuan['代理'].append(i['parentName'])
            dic_huiyuan['vip等级'].append(i['vipLevel'])
            dic_huiyuan['首存时间'].append(i['firstTime'])
    print(pd.DataFrame(dic_huiyuan).shape)
    return  dic_huiyuan


#多线程使用
if __name__ =='__main__':
    for i in range(10):
        t1 = threading.Thread()









