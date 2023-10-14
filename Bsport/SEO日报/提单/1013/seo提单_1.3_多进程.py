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

    # 采集会员列表和会员首存记录

    # 采集昨日首存报表
    dic_fir = dict({'会员名':[], '所属代理':[],'注册时间':[], '交易时间':[], '交易类型':[], '币种':[], '金额':[]})
    # 昨天开始时间戳
    yesterday = datetime.date.today() + datetime.timedelta(days=day)
    yesterday_start_time = int(time.mktime(time.strptime(str(yesterday), '%Y-%m-%d')))
    # 昨天结束时间戳
    yesterday_end_time = int(time.mktime(time.strptime(str(datetime.date.today()), '%Y-%m-%d'))) - 1

    #---------------------token----------------------
    # 采取token
    google_code = get_google_code('64ehnxj6yily5bhv23kgb62ozuh6yuu2')
    data0 = {
        'username': 'Marquis',
        'password': 'qwer123456',
        'code': google_code
    }
    session0 = requests.Session()
    response0  =session0.post(url=submit_url,data=data0,headers=header0)
    response0.encoding = 'utf-8'
    obj0 = json.loads(response0.text)
    token = obj0['data']['token']

    header = {
        'Accept':'application/json, text/plain, */*',
        # 'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Content-Length':'75',
        'Content-Type':'application/x-www-form-urlencoded',
        'Cookie':'admin-token=67c8b1bd1b434f898ed8570a860355b8; admin-uid=690',
        'Device_id':'1.0',
        'Gl_version':'2.0',
        'Host':'fundmng.bsportsadmin.com',
        'Language':'zh_CN',
        'Menuid':'100112',
        'Opeartionmenu':'%u62A5%u8868%u67E5%u8BE2-%u4F1A%u5458%u9996%u5B58%u62A5%u8868',
        'Origin':'http://fundmng.bsportsadmin.com',
        'Os_type':'0',
        'Referer':'http://fundmng.bsportsadmin.com/system/report-query/report-first-recharge',
        'Sign':'ca83944852acc68fe114cbc65f1e1d22',
        'Some':'header',
        'Systemid':'54',
        'Timestamp':'1692092554000',
        'Token':token,
        'Uid':'690',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Version':'1.0'
    }
    for page in range(1,pages_fircharge+1):
        data = {
            'page': page,
            'size': 20,
            'tradeType': 0,
            'isFake': 0,
            'stime': yesterday_start_time*1000,
            'etime': yesterday_end_time*1000+999
        }
        response = session.post(url_fircharge,headers=header,data=data)
        response.encoding = 'utf-8'
        obj = json.loads(response.text)

        for i in obj['data']['list']:
            dic_fir['会员名'].append(i['userName'])
            dic_fir['所属代理'].append(i['parentName'])
            dic_fir['注册时间'].append(time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(i['createTime']//1000)))
            dic_fir['交易时间'].append(time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(i['regTime']//1000)))
            dic_fir['交易类型'].append(i['tradeType'])
            dic_fir['币种'].append(i['coinCode'])
            dic_fir['金额'].append(i['amount'])
    firChargeUser = pd.DataFrame(dic_fir)
    print('会员首存行列：',firChargeUser.shape)

    # 2.采集昨天和今天的首存报表
    dic_fir_two = dict({'会员名':[], '所属代理':[],'注册时间':[], '交易时间':[], '交易类型':[], '币种':[], '金额':[]})
    for page in range(1,pages_fircharge_two+1):
        data = {
            'page': page,
            'size': 20,
            'tradeType': 0,
            'isFake': 0,
            'stime': yesterday_start_time*1000,
            'etime': int(time.time())*1000
        }
        response = session.post(url_fircharge,headers=header,data=data)
        response.encoding = 'utf-8'
        obj = json.loads(response.text)

        for i in obj['data']['list']:
            dic_fir_two['会员名'].append(i['userName'])
            dic_fir_two['所属代理'].append(i['parentName'])
            dic_fir_two['注册时间'].append(time.strftime('%Y/%m/%d',time.localtime(i['createTime']//1000)))
            dic_fir_two['交易时间'].append(time.strftime('%Y/%m/%d',time.localtime(i['regTime']//1000)))
            dic_fir_two['交易类型'].append(i['tradeType'])
            dic_fir_two['币种'].append(i['coinCode'])
            dic_fir_two['金额'].append(i['amount'])
    charge_two  = pd.DataFrame(dic_fir_two)
    print('昨天+今天的会员首存行列：',charge_two.shape)

    # 采集会员列表
    dic_user = dict({'会员账号':[], '姓名':[],'代理':[],'玩家层级':[], '注册时间':[], '首存时间':[],'备注':[]})
    for page in range(1,pages_user+1):
        data2 = {
            'page':page,
            'size':20,
            'userVip':'0,1,2,3,4,5,6,7,8,9,10,11',
            'status':'0,1,2,4',
            'sortType':'3',
            'sortStr':'descend',
            'searchType':'1',
            'channelId':'34',
            'registeredStartDate':yesterday_start_time*1000,
            'registeredEndDate':yesterday_end_time*1000+999,
        }
        response2 = session.post(url_user,headers=header,data=data2)
        response2.encoding = 'utf-8'
        obj2 = json.loads(response2.text)
        for i in obj2['data']['list']:
            dic_user['会员账号'].append(i['username'])
            if i['reallyName'] !='':
                dic_user['姓名'].append(i['reallyName'])
            else:
                dic_user['姓名'].append('-')

            dic_user['代理'].append(i['parentName'])
            dic_user['玩家层级'].append(i['levelName'])
            dic_user['注册时间'].append(time.strftime('%Y/%m/%d',time.localtime(i['registerDate']//1000)))
            dic_user['首存时间'].append(time.strftime('%Y/%m/%d',time.localtime(i['firstRechargeDate']//1000)))
            dic_user['备注'].append(i['remark'])
    user = pd.DataFrame(dic_user)
    print('用户列表行列:',user.shape)
    # 删除测试账号
    user = user[~user['会员账号'].str.contains('test')&~user['会员账号'].str.contains('ceshi')&~user['姓名'].str.contains('测试') \
                &~user['姓名'].str.contains('ceshi')&~user['代理'].str.contains('测试')&~user['代理'].str.contains('ceshi') \
                &~user['备注'].str.contains('测试')&~user['备注'].str.contains('试玩')&~user['备注'].str.contains('晒单') \
                &~user['玩家层级'].str.contains('测试')]
    print('去重后：',user.shape)

    shuju = pd.DataFrame({'人员':['paddy', 'tony', 'max', 'martin', 'zed', 'hugo', 'aber', 'dk', 'ben']})
    shuju['人员2']=shuju['人员']
    shuju.set_index('人员2',inplace=True)
    shuju.sort_index(inplace=True)
    # 注册数

    merge_user = pd.merge(user,daili,how = 'left',left_on='代理',right_on='代理线')
    result = merge_user.groupby('seo变化数据团队').agg({'seo变化数据团队':len})
    result.rename(columns={'seo变化数据团队':'注册数'},inplace=True)

    # 绑卡
    merge_user_dropna = merge_user.loc[~merge_user['seo变化数据团队'].isna()&(merge_user['姓名']!='-'),]
    bangka = merge_user_dropna.groupby('seo变化数据团队').agg({'会员账号':len})
    bangka.rename(columns={'会员账号':'绑卡数'},inplace=True)

    # join
    result2 = result.join(bangka).fillna(0)
    result2['绑卡率'] = result2['绑卡数']/result2['注册数']

    # 采集交易明细 trade
    print('开始采集会员交易明细表。。。。')
    # 新token
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
        'Accept':'application/json, text/plain, */*',
        # 'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Content-Length':'103',
        'Content-Type':'application/x-www-form-urlencoded',
        'Cookie':'admin-token=fc66d42ccb0f4ca58b184fbe5498158c; admin-uid=690',
        'Device_id':'1.0',
        'Gl_version':'2.0',
        'Host':'fundmng.bsportsadmin.com',
        'Language':'zh_CN',
        'Menuid':'100104',
        'Opeartionmenu':'%u62A5%u8868%u67E5%u8BE2-%u4F1A%u5458%u9996%u5B58%u62A5%u8868',
        'Origin':'http://fundmng.bsportsadmin.com',
        'Os_type':'0',
        'Referer':'http://fundmng.bsportsadmin.com/system/report-query/transaction-for-user',
        'Sign':'1abc87008c66bc0b4d3d7a3870442b16',
        'Some':'header',
        'Systemid':'54',
        'Timestamp':'1697016616000',
        'Token':token,
        'Uid':'690',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Version':'1.0'
    }

    dic_trade = dict({'账户名':[], '所属代理':[]})
    for page in range(1,pages_trade+1):
        data2 = {
            'page':page,
            'size':500,
            'reportType':'0',
            'userType':'0',
            'dateType':'0',
            'startDate':yesterday_start_time*1000,
            'endDate':yesterday_end_time*1000+999,
            'type':'1'
        }
        response2 = session.post(url_trade,headers=header,data=data2)
        response2.encoding = 'utf-8'
        obj2 = json.loads(response2.text)
        for i in obj2['data']['list']:
            dic_trade['账户名'].append(i['username'])
            dic_trade['所属代理'].append(i['parentName'])

    trade = pd.DataFrame(dic_trade)
    print('trade:',trade.shape)
    # 未拉过单
    huiyuan2 = huiyuan.loc[(huiyuan['首存时间']=='--'),]
    print('去除会员流失有首存时间后：',huiyuan2.shape)
    merge_huiyuan = huiyuan2.merge(daili,left_on = '代理',right_on='代理线')
    # print(merge_huiyuan.shape)
    # merge_huiyuan2 = merge_huiyuan.loc[~merge_huiyuan['准点激活团队'].isna(),]
    # print('处理后：',merge_huiyuan2.shape)

    mingdan= set(list(merge_huiyuan['会员账号'].values)+list(charge_two['会员名'].values))
    # 删除交易测试账号
    trade2 = trade[~trade['账户名'].str.contains('test')&~trade['账户名'].str.contains('ceshi')&~trade['所属代理'].str.contains('测试')&~trade['所属代理'].str.contains('ceshi')]
    trade_daili= trade2.merge(daili,left_on='所属代理',right_on='代理线')
    print('去除测试后的trade:',trade2.shape)
    tidan = trade_daili.loc[trade_daili['账户名'].isin(mingdan),]
    # 去除重复用户
    tidan.drop_duplicates('账户名',inplace=True)
    tidan_grp = tidan.groupby('seo变化数据团队').agg({'账户名':len}).rename(columns={'账户名':'提单人数'})
    shuju = shuju.join(result2).join(tidan_grp)
    shuju.fillna(0,inplace=True)
    shuju['提单率']=shuju['提单人数']/shuju['绑卡数']

    # 计算首存人数
    charge_merge = firChargeUser.merge(daili,left_on = '所属代理',right_on='代理线')
    charge_grp = charge_merge.groupby('seo变化数据团队').agg({'seo变化数据团队':len})
    charge_grp.rename(columns={'seo变化数据团队':'首存数'},inplace=True)
    shuju = shuju.join(charge_grp)
    shuju.fillna(0,inplace=True)
    shuju['提单充值率']=shuju['首存数']/shuju['提单人数']
    # 当日注册当日首存
    merge_2_user = merge_user.loc[merge_user['注册时间']==merge_user['首存时间'],]
    merge_2_grp = merge_2_user.groupby('seo变化数据团队').agg({'seo变化数据团队':len})
    merge_2_grp.rename(columns={'seo变化数据团队':'当日注册当日首存'},inplace=True)
    shuju = shuju.join(merge_2_grp)
    shuju.fillna(0,inplace=True)
    shuju['当日注册当日首存率']  = shuju['当日注册当日首存']/shuju['注册数']

    # 当天注册当天绑卡当天提单
    merge_3_user = merge_user.loc[(merge_user['注册时间']==merge_user['首存时间'])&(~merge_user['seo变化数据团队'].isna())&(merge_user['姓名']!='-'),]
    merge_3_grp = merge_3_user.groupby('seo变化数据团队').agg({'会员账号':len})
    merge_3_grp.rename(columns={'会员账号':'当天注册当天绑卡当天提单'},inplace=True)
    shuju = shuju.join(merge_3_grp)

    # 后续处理
    last_date = str((datetime.datetime.now()+datetime.timedelta(days=day)).strftime('%Y/%m/%d'))
    shuju.fillna(0,inplace=True)
    tem = pd.DataFrame({'人员': last_date,
                        '注册数':shuju['注册数'].sum(),
                        '绑卡数':shuju['绑卡数'].sum(),
                        '绑卡率':shuju['绑卡数'].sum()/shuju['注册数'].sum(),
                        '提单人数':shuju['提单人数'].sum(),
                        '提单率':shuju['提单人数'].sum()/shuju['绑卡数'].sum(),
                        '首存数':shuju['首存数'].sum(),
                        '提单充值率':shuju['首存数'].sum()/shuju['提单人数'].sum(),
                        '当日注册当日首存':shuju['当日注册当日首存'].sum(),
                        '当日注册当日首存率':shuju['当日注册当日首存'].sum()/shuju['注册数'].sum(),
                        '当天注册当天绑卡当天提单':shuju['当天注册当天绑卡当天提单'].sum()},index=[0])
    shuju = tem.append(shuju)
    # 去除小数点
    shuju.fillna(0,inplace=True)
    shuju['注册数'] = shuju['注册数'].astype('int')
    shuju['绑卡数'] = shuju['绑卡数'].astype('int')
    shuju['提单人数'] = shuju['提单人数'].astype('int')
    shuju['首存数'] = shuju['首存数'].astype('int')
    shuju['当日注册当日首存'] = shuju['当日注册当日首存'].astype('int')
    shuju['当天注册当天绑卡当天提单'] = shuju['当天注册当天绑卡当天提单'].astype('int')

    # 增加%
    shuju['绑卡率']=shuju['绑卡率'].map(lambda x:str(0)+'%' if np.isinf(x) else str(round(x*100))+'%')
    shuju['提单率']=shuju['提单率'].map(lambda x:str(0)+'%' if np.isinf(x) else str(round(x*100))+'%')
    shuju['提单充值率']=shuju['提单充值率'].map(lambda x:str(0)+'%' if np.isinf(x) else str(round(x*100))+'%')
    shuju['当日注册当日首存率']=shuju['当日注册当日首存率'].map(lambda x:str(0)+'%' if np.isinf(x) else str(round(x*100))+'%')


    shuju['辅助日期']=['总计']+[last_date for i in range(9)]

    print(shuju)

    # 保存数据
    # app = xw.App(visible=False,add_book=False)
    # book =app.books.open(r'C:\Users\User\Desktop\SEO\SEO提单数据\1011\SEO数据-每日.xlsx')
    # sheet = book.sheets['总表']
    # row = sheet.used_range.last_cell.row
    # sheet['A'+str(row+1)].options(index=False,header=False).value = shuju
    # book.save()
    # time.sleep(2)
    # book.close()
    # app.quit()

    print('已保存,主进程结束')
    print('耗时：',int(time.time())-start,'s')