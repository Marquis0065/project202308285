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
import queue
import concurrent.futures
import multiprocessing


start = int(time.time())

pd.set_option('display.max_colwidth', None) #显示单元格完整信息
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


url_huiyuan = 'http://fundmng.bsportsadmin.com/api/manage/user/maintain/user/list'  #会员列表

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
    'Referer':'http://fundmng.bsportsadmin.com/system/user-management/member-list',
    'Sign':'59951b8ae1578a128acea9b581dbe79e',
    'Timestamp':'1697351079000',
    'Token':token,
    'Uid':'690',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Version':'1.0'
}
# 总条数
data_init = {
    'page':1,
    'size':20,
    'userVip':'0,1,2,3,4,5,6,7,8,9,10,11',
    'status':'0,1,2,4',
    'sortType':'3',
    'sortStr':'descend',
    'searchType':'1',
    'channelId':'34',
    'registeredStartDate':1601481600000,
    'registeredEndDate':int(time.time())*1000
}
#获取会员流失页码
session = requests.session()
response = session.post(url=url_huiyuan,data=data_init,headers=header)
obj_init = json.loads(response.text)
n_data = obj_init['data']['total']
print('会员总条数：',n_data)
pages = math.ceil(n_data/500)
print('会员列表总页码：',pages)

page_list = []
for i in range(0,pages,pages//10):
    page_list.append(i)
page_list[10]=pages

def huiyuan_q_fun(start_page,end_page):
    dic_huiyuan = {'会员账号':[],'代理':[],'电话':[],'vip等级':[],'注册时间':[],'注册地':[]}
    for page in range(start_page,end_page+1):
        # 获取页码数量
        print(f'第{page}页。。。')
        data = {
            'page':page,
            'size':500,
            'userVip':'0,1,2,3,4,5,6,7,8,9,10,11',
            'status':'0,1,2,4',
            'sortType':'3',
            'sortStr':'descend',
            'searchType':'1',
            'channelId':'34',
            'registeredStartDate':1601481600000,
            'registeredEndDate':int(time.time())*1000
        }
        response = session.post(url=url_huiyuan,data=data,headers=header)
        response.encoding='utf8'
        obj = json.loads(response.text)

        for i in obj['data']['dataList']:
            dic_huiyuan['会员账号'].append(i['userName'])
            dic_huiyuan['代理'].append(i['parentName'])
            dic_huiyuan['电话'].append(i['telephone'])
            dic_huiyuan['vip等级'].append(i['vipLevel'])
            dic_huiyuan['注册时间'].append(i['registerDate'])
            dic_huiyuan['注册地'].append(i['registerIpLocation'])

    print(pd.DataFrame(dic_huiyuan).shape)
    return  dic_huiyuan


#多线程使用
if __name__ =='__main__':

    huiyuan = pd.DataFrame(columns=['会员账号','代理','电话','vip等级','注册时间','注册地'])

    pool = multiprocessing.Pool(processes=10)
    #创建进程共享队列
    result_queue = multiprocessing.Manager().Queue()
    for i in range(10):
        pool.apply_async(func=huiyuan_q_fun,args=(page_list[i]+1,page_list[i+1]),
                         callback=result_queue.put)
    #关闭进程池
    pool.close()
    #进程等待
    pool.join()


    while not result_queue.empty():
        huiyuan=huiyuan.append(pd.DataFrame(result_queue.get()))

    print(huiyuan.shape)
    print('主线程运行完成。。')











