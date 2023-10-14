# 会员流失 ，第一次获取token
import multiprocessing

import requests
import pandas as pd
import numpy as np
import jsonpath
import json
import time
import datetime
import xlwings as xw
import telebot
import hmac, base64, struct, hashlib
import math
import warnings
warnings.filterwarnings('ignore')

start = int(time.time())


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
# 采集会员流失记录

url_huiyuan = 'http://fundmng.bsportsadmin.com/api/manage/data/loss/user/manage/list'
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
    'regEndTime': 1798854399999,
}
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
            'regEndTime': 1798854399999,
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




if __name__ == '__main__':
    huiyuan = pd.DataFrame(columns=['会员账号','代理','vip等级','首存时间'])
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
    #输出数据
    while not result_queue.empty():
        dic = result_queue.get()
        huiyuan=huiyuan.append(pd.DataFrame(dic))
    print(huiyuan.shape)

    print('耗时：',int(time.time())-start,'s')







# import multiprocessing
#
# q = multiprocessing.Queue()
#
#
# if __name__=='__main__':
#     jobs = []
#     for i in range(10):
#         p = multiprocessing.Process(target=huiyuan_q_fun, args=(page_list[i]+1,page_list[i+1],q))
#         jobs.append(p)
#         p.start()
#     for p in jobs:
#          p.join()
#     df= pd.DataFrame(columns=['会员账号','代理','vip等级','首存时间'])
#     for i in range(10):
#         print('队列：',i+1)
#         dic=q.get()
#         if i ==5:
#             print(dic)
#         df=df.append(pd.DataFrame(dic))
#
#     print(df.shape)
#     print('总耗时：',int(time.time())-start,'s')

#
#
# with multiprocessing.Pool(processes=10) as pool:
#     for i in range(10):
#         pool.starmap(huiyuan_q_fun, (page_list[i]+1,page_list[i+1], q))
# print(q.maxsize)
#
# df= pd.DataFrame()
# while not q.empty():
#     tem = pd.DataFrame(q.get())
#     df = df.append(tem)


