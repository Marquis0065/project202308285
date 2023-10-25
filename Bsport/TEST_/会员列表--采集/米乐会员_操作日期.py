# SEO环境： schedule
import warnings
warnings.filterwarnings('ignore')
import requests
import pandas as pd
import json
import time
import hmac, base64, struct, hashlib
import math
import multiprocessing
import datetime
import os


start = int(time.time())
today_5am = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, 5)


# pd.set_option('display.max_colwidth', None) #显示单元格完整信息
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)


url_mile = 'https://f.m6vip6.com/api/forehead/data/proxy/member/allReport'  #会员列表
session = requests.Session()
# 采集会员列表

header = {
    # ':authority':'f.m6vip6.com',
    # ':method':'POST',
    # ':path':'/api/forehead/data/proxy/member/allReport',
    # ':scheme':'https',
    'Accept':'application/json, text/plain, */*',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'App-Type':'2',
    'Content-Length':'728',
    'Content-Type':'application/x-www-form-urlencoded',
    'Cookie':'WM_NI=i%2BhICl8%2FAngN0WZWgYZbd%2B2hTeJJHT%2BIf6WYbjV%2B91SGye0F12E6WjA3AWVSCU2wILw%2BkOdvk2Oi1OnpiRbzTIlGAB3wooID6utjcY40btFFTR1uJEKfK%2FfRzNFLVZrBeEI%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee8ef74ea199a3baed6086b88ab2c14e928f8fadc53a83bce5d1c85c9395a88fc42af0fea7c3b92aabf5a8aac268fcf18f8fe646f48996b8e6539abeacccb16498bb86abcb60e997aad7d653a2b69accbc3b9199b786b34ef3ee8bd7d66283ed8fb8d559818bfe98cc48b5f5a5b0e77ea9ee818ab445aeb0a7b3e1729897a4a8c44af1a9a190cc50f6abbc8be253f8f0ae95c54e988eff96c94f89ba85d0e55aba928aadd552b29eaba6cc37e2a3; WM_TID=73TK9wXVuSFBQBQEBQaFjBcvgFKQKhiB; agency-uid=187789; agency-token=ki92F1AJl4TYx37Qmjjfc/j/ZF5B4rjDKxYjm15dg2wZDM3/gtQhmA==',
    'Device-Id':'PC-73TK9wXVuSFBQBQEBQaFjBcvgFKQKhiB',
    'Origin':'https://f.m6vip6.com',
    'Os-Type':'0',
    'Referer':'https://f.m6vip6.com/report/member-all-data',
    'Sec-Ch-Ua':'"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'Sec-Ch-Ua-Mobile':'?0',
    'Sec-Ch-Ua-Platform':'"Windows"',
    'Sec-Fetch-Dest':'empty',
    'Sec-Fetch-Mode':'cors',
    'Sec-Fetch-Site':'same-origin',
    'Sign':'b7189f57ba1ca135b07c9597f393cc9e',
    'Timestamp':'1697880548211',
    'Token':'rsFLizCKQXdc7FctOBid4t2Ti3If7Vm7zjvbA25Tf8oVigFdV+PKzQ==',
    'Uid':'187789',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Version':'1.0'
}
# 总条数

data_init = {
    'page':1,
    'size':15,
    'parentName':'seo1998,seo2008,seo8888,seo3000,seo5001,seo5002,seo9999,seo6666,seo5003,seo8001,seo8002,seo8003,seo6001,seo6002,seo6003,seo6004,seo6005,seo6007,seo6008,seo6009,seo7001,seo7002,seo7006,seo7007,seo7003,seo7008,seo7009,seo5555,seo9001,seo9002,seo9003,seo9005,seo9006,seo5678,seo9900,zh9001,zh9010,zh9011,ki8888,zh9002,zh9003,zh0001,zh9005,zh9006,ldj131419,huoge40952845,timi9001,sven9001,abby9001,penial88,luren88,zh9008,zh9009,zh10000,chakala123,sasuke123,miyasaki123,hotalu123,zh6666,zh6677,zh1122,zh3355,zh8899,zh7777,aq9999,coco555',
    'regStartTime': 1514736000000,
    'regEndTime': int(today_5am.timestamp())*1000

}
#获取会员流失页码
session_init = requests.session()
response = session_init.post(url=url_mile,data=data_init,headers=header)
obj_init = json.loads(response.text)
n_data = obj_init['data']['total']
print('会员总条数：',n_data)
pages = math.ceil(n_data/500)
print('会员列表总页码：',pages)

page_list = []
for i in range(0,pages,100):
    page_list.append(i)
page_list.append(pages)
print(page_list)

def huiyuan_q_fun(start_page,end_page):

    dic_huiyuan = {'会员账号':[],'上级代理':[],'电话':[],'vip等级':[],'注册时间':[],'注册网址':[]}
    for page in range(start_page,end_page+1):
        # 获取页码数量
        print(f'第{page}页。。。')
        data = {
            'page':page,
            'size':500,
            'parentName':'seo1998,seo2008,seo8888,seo3000,seo5001,seo5002,seo9999,seo6666,seo5003,seo8001,seo8002,seo8003,seo6001,seo6002,seo6003,seo6004,seo6005,seo6007,seo6008,seo6009,seo7001,seo7002,seo7006,seo7007,seo7003,seo7008,seo7009,seo5555,seo9001,seo9002,seo9003,seo9005,seo9006,seo5678,seo9900,zh9001,zh9010,zh9011,ki8888,zh9002,zh9003,zh0001,zh9005,zh9006,ldj131419,huoge40952845,timi9001,sven9001,abby9001,penial88,luren88,zh9008,zh9009,zh10000,chakala123,sasuke123,miyasaki123,hotalu123,zh6666,zh6677,zh1122,zh3355,zh8899,zh7777,aq9999,coco555',
            'regStartTime': 1514736000000,
            'regEndTime': int(today_5am.timestamp())*1000
        }
        response = session.post(url=url_mile,data=data,headers=header)
        response.encoding='utf8'
        obj = json.loads(response.text)

        for i in obj['data']['list']:
            dic_huiyuan['会员账号'].append(i['username'])
            dic_huiyuan['上级代理'].append(i['parentName'])
            dic_huiyuan['电话'].append(i['telephone'])
            dic_huiyuan['vip等级'].append(i['vipLevel'])
            dic_huiyuan['注册时间'].append(time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(i['registerDate']//1000)))
            dic_huiyuan['注册网址'].append(i['registerDomain'])

    print(pd.DataFrame(dic_huiyuan).shape)
    return  dic_huiyuan

huiyuan_mile = pd.DataFrame(columns=['会员账号','上级代理','电话','vip等级','注册时间','注册网址'])



if __name__=='__main__':

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
        huiyuan_mile=huiyuan_mile.append(pd.DataFrame(dic))
    print(huiyuan_mile.shape)

    writer = pd.ExcelWriter(r'C:\Users\User\Desktop\文件\定时任务\会员列表更新\mile_会员总表_操作时间-idea.xlsx')
    huiyuan_mile.to_excel(writer, sheet_name='米乐总表-操作时间',index=False)

    writer.save()
    print('耗时:',int(time.time())-start,'s')

















