import pandas as pd
import datetime
import time
import xlwings as xw
import hmac, base64, struct, hashlib
import requests
import json
import os
import telebot

# pd.set_option('display.max_colwidth', None) #显示单元格完整信息
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

pages_member = 200
pages_trade = 200
pages_p = 50
ayuang = '47chomf5mzxmkrcw3pf2yftn6s5fg7pa'
start = int(time.time())
# today_0 = (int(time.time()) - (int(time.time())-time.timezone)%86400)*1000
# today_18 = int(datetime.datetime.combine(datetime.date.today(), datetime.time(18)).timestamp())*1000
yesterday = datetime.date.today() + datetime.timedelta(days=-1)
yesterday_start_time=int(time.mktime(time.strptime(str(yesterday), '%Y-%m-%d')))*1000
today_12 = int(datetime.datetime.combine(datetime.date.today(), datetime.time(12)).timestamp())*1000
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
# 读取会员列表
# member = pd.read_csv(r'C:\Users\User\Desktop\文件\追击\0928\会员列表导出.csv',encoding='gbk')
# 采集会员列表
url_member = 'http://fundmng.bsportsadmin.com/api/manage/user/maintain/user/list'
# 采取token  '47chomf5mzxmkrcw3pf2yftn6s5fg7pa'
# google_code = get_google_code('64ehnxj6yily5bhv23kgb62ozuh6yuu2')
google_code = get_google_code('47chomf5mzxmkrcw3pf2yftn6s5fg7pa')
data0 = {
    'username': 'plier',
    'password': 'aa123456',
    'code': google_code
}
print('谷歌验证码：',google_code)
session0 = requests.Session()
response0  =session0.post(url=submit_url,data=data0,headers=header0)
response0.encoding = 'utf-8'
obj0 = json.loads(response0.text)
token = obj0['data']['token']

header_huiyuan = {
    'Device_id': '1.0',
    'Os_type': '0',
    'Sign': '5d9818dde56ca3445ce212ba45c2dcf1',
    'Timestamp': '1694410046000',
    'Token': token,
    'Uid': '709',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Version': '1.0'
}
session = requests.Session()
dic_user = dict({'会员账号':[], '姓名':[], '手机号码':[],'代理':[], 'VIP等级':[], '注册时间':[],  '状态':[],'备注':[]})
for page in range(1,pages_member+1):
    data2 = {
        'page':page,
        'size':20,
        'userVip':'0,1,2,3,4,5,6,7,8,9,10,11',
        'status':'0,1,2,4',
        'sortType':'3',
        'sortStr':'descend',
        'searchType':'1',
        'channelId':'34',
        'registeredStartDate':yesterday_start_time,
        'registeredEndDate':today_12,
    }
    response2 = session.post(url_member,headers=header_huiyuan,data=data2)
    response2.encoding = 'utf-8'
    obj2 = json.loads(response2.text)
    for i in obj2['data']['list']:
        dic_user['会员账号'].append(i['username'])
        if i['reallyName'] !='':
            dic_user['姓名'].append(i['reallyName'])
        else:
            dic_user['姓名'].append('--')
        dic_user['手机号码'].append(i['telephone'])
        dic_user['代理'].append(i['parentName'])
        dic_user['VIP等级'].append(i['vipLevel'])
        dic_user['注册时间'].append(time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(i['registerDate']//1000)))
        dic_user['状态'].append(i['status'])
        dic_user['备注'].append(i['remark'])
member = pd.DataFrame(dic_user)
member['状态']=member['状态'].map({0:'正常',1:'完全锁定'})
print('用户列表行列:',member.shape)


# 读取交易失败列表
# fail_trade = pd.read_csv(r'C:\Users\User\Desktop\文件\追击\0928\交易明细报表.csv',encoding='gbk')
#采集交易明细表
# 重新获取token
google_code = get_google_code('47chomf5mzxmkrcw3pf2yftn6s5fg7pa')
data0 = {
    'username': 'plier',
    'password': 'aa123456',
    'code': google_code
}
session0 = requests.Session()
response0  =session0.post(url=submit_url,data=data0,headers=header0)
response0.encoding = 'utf-8'
obj0 = json.loads(response0.text)
token = obj0['data']['token']

header_jiaoyi = {
    'Device_id': '1.0',
    'Os_type': '0',
    'Sign': '5d9818dde56ca3445ce212ba45c2dcf1',
    'Timestamp': '1694410046000',
    'Token': token,
    'Uid': '709',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Version': '1.0'
}
url_trade = 'http://fundmng.bsportsadmin.com/api/manage/data/balance/record/list'
dic_trade = dict({'账户名':[], '状态':[], '操作时间':[],'账变时间':[]})
for page in range(1,pages_trade+1):
    data1 = {
        'page':page,
        'size':500,
        'status':'2',
        'reportType':'0',
        'userType':'0',
        'dateType':'0',
        'startDate':yesterday_start_time,
        'endDate':today_12,
        'type':'1,9'
    }
    response1 = session.post(url_trade,headers=header_jiaoyi,data=data1)
    response1.encoding = 'utf-8'
    obj1 = json.loads(response1.text)
    for i in obj1['data']['list']:
        if i['statusStr']=='失败':
            dic_trade['账户名'].append(i['username'])
            dic_trade['状态'].append(i['statusStr'])
            dic_trade['操作时间'].append(time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(i['transactionDate']//1000)))
            dic_trade['账变时间'].append(time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(i['balanceChangedDate']//1000)))

fail_trade = pd.DataFrame(dic_trade)
print('交易记录:',fail_trade.shape)

#读取P图诈单
# pitu = pd.read_csv(r'C:\Users\User\Desktop\文件\追击\0928\P图骗分名单.csv',encoding='gbk')
#采集P图数据
# 重新获取token
google_code = get_google_code('47chomf5mzxmkrcw3pf2yftn6s5fg7pa')
data0 = {
    'username': 'plier',
    'password': 'aa123456',
    'code': google_code
}
session0 = requests.Session()
response0  =session0.post(url=submit_url,data=data0,headers=header0)
response0.encoding = 'utf-8'
obj0 = json.loads(response0.text)
token = obj0['data']['token']

header_p = {
    'Accept':'application/json, text/plain, */*',
    #'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'Content-Length':'21',
    'Content-Type':'application/x-www-form-urlencoded',
    'Cookie':'admin-token=fc155f87cb87437ab4bcb8708ce61f0d; admin-uid=709',
    'Device_id':'1.0',
    'Gl_version':'2.0',
    'Host':'fundmng.bsportsadmin.com',
    'Language':'zh_CN',
    'Menuid':'100408',
    'Opeartionmenu':'%u7528%u6237%u7BA1%u7406-%u6807%u7B7E%u7BA1%u7406',
    'Origin':'http://fundmng.bsportsadmin.com',
    'Os_type':'0',
    'Referer':'http://fundmng.bsportsadmin.com/system/user-management/label-management',
    'Sign':'371c8ebcd41db514b855cb211e241002',
    'Some':'header',
    'Systemid':'51',
    'Timestamp':'1696487628000',
    'Token':token,
    'Uid':'709',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Version':'1.0'
}
url_p = 'http://fundmng.bsportsadmin.com/api/manage/user/tag/list/user'
dic_p = dict({'用户名':[], '添加时间':[], '添加人':[],'备注':[]})
for page in range(1,pages_p+1):
    data1 = {
        'page': page,
        'size': 200,
        'id': '127'
    }
    response_p = session.post(url_p,headers=header_p,data=data1)
    response_p.encoding = 'utf-8'
    obj_p = json.loads(response_p.text)

    for i in obj_p['data']['list']:
        dic_p['用户名'].append(i['username'])
        dic_p['添加人'].append(i['creator'])
        dic_p['添加时间'].append(time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(i['createTime']//1000)))
        dic_p['备注'].append(i['remark'])

pitu = pd.DataFrame(dic_p)
print('pitu:',pitu.shape)
#读取既往名单
pre_member = pd.read_excel(r'C:\Users\User\Desktop\文件\追击\1005\电销追击1005.xlsx','本月名单汇总')
#读取代理线
daili = pd.read_excel(r'C:\Users\User\Desktop\文件\追击\1005\电销追击1005.xlsx','代理线')
#去除重复代理线
daili.drop_duplicates('代理线',inplace = True)

#-----------------------开始处理-----------------------
member2 = member.merge(pitu['用户名'],left_on='会员账号',right_on='用户名',how='left')
member2 = member2.rename(columns = {'用户名':'P图骗分'})

fail_trade2 = fail_trade.drop_duplicates('账户名')
member3 = member2.merge(fail_trade2[['账户名','状态']],left_on='会员账号',right_on='账户名',how='left')
member3=member3.rename(columns={'状态_x':'状态','状态_y':'提单失败'})
member3.drop('账户名',axis=1,inplace=True)


member4 = member3.merge(daili,left_on='代理',right_on='代理线',how='left')

member5 = member4.merge(pre_member[['会员账号','提供时间']],on='会员账号',how='left')
member5=member5.rename(columns={'提供时间':'已提供'})

#最终提供名单
result = member5.loc[(member5['手机号码'].apply(lambda x: len(str(x)))==11)&(member5['状态']=='正常')&(member5['VIP等级']==0) \
                     &(member5['提单失败']=='失败')&(member5['已提供'].isna())&(member5['P图骗分'].isna())&(~member5['代理线'].isna()),]
result = result[['会员账号','手机号码','代理','VIP等级','注册时间','状态']]
result.insert(0,'提供时间',datetime.datetime.now().strftime('%Y%m%d')+'-12')
#删除特定代理线
result.drop(result.loc[result['代理']=='btyscnb0093',].index,inplace=True)
# result['提供时间']= datetime.datetime.now().strftime('%Y%m%d')+'-12'

# 筛选新增代理线
result2 = member5.loc[(member5['手机号码'].apply(lambda x: len(str(x)))==11)&(member5['状态']=='正常')&(member5['VIP等级']=='VIP0')&(member5['提单失败']=='失败')&(member5['已提供'].isna())&(member5['P图骗分'].isna())&(member5['代理线'].isna()),]
add_daili = result2.loc[result2['代理'].str.startswith(('btyseo','btydl','wbdl')),]['代理']

print(result.shape)
print('新增代理',add_daili.shape)

#写入本月工作簿
app = xw.App(visible=False,add_book=False)
book = app.books.open(r'C:\Users\User\Desktop\文件\追击\1005\电销追击1005.xlsx')
sheet_daili= book.sheets['代理线']
row_daili = sheet_daili.used_range.last_cell.row

sheet= book.sheets['本月名单汇总']
row = sheet.used_range.last_cell.row
#增加名单
if len(result)>0:
    sheet['A'+str(row+1)].options(index=False,header=False).value = result
#增加代理线
if len(add_daili)>0:
    sheet_daili['A'+str(row_daili+1)].options(index=False,header=False).value = add_daili
#今日数据(12点)
curr_sheet = book.sheets['今日名单(12点)']
#清空表格
curr_sheet.clear_contents()
if len(result)>0:
    curr_sheet['A1'].options(index=False,header=True).value = result
book.save()
book.close()
app.quit()
#保存发送表格-每日12点
result.to_excel(rf'C:\Users\User\Desktop\文件\追击\每日12点\追击名单_{datetime.datetime.now().strftime("%Y%m%d")}-12点.xlsx',index=False)
time.sleep(3)
#加密
app = xw.App(visible=False,add_book=False)
book = app.books.open(rf'C:\Users\User\Desktop\文件\追击\每日12点\追击名单_{datetime.datetime.now().strftime("%Y%m%d")}-12点.xlsx')
book.save(rf'C:\Users\User\Desktop\文件\追击\每日12点\追击名单_{datetime.datetime.now().strftime("%Y%m%d")}-12点.xlsx',password='qwer12')
book.close()
app.quit()
#发送
if os.path.exists(rf'C:\Users\User\Desktop\文件\追击\每日12点\追击名单_{datetime.datetime.now().strftime("%Y%m%d")}-12点.xlsx'):
    bot_m = telebot.TeleBot("6377312623:AAGz3ZSMVswWq0QVlihRPklw8b7skSBP16Y")
    bot_m.send_document(-677235937,open(rf'C:\Users\User\Desktop\文件\追击\每日12点\追击名单_{datetime.datetime.now().strftime("%Y%m%d")}-12点.xlsx','rb'),timeout=500)
    bot_m.stop_polling()
else:
    bot_m = telebot.TeleBot("6377312623:AAGz3ZSMVswWq0QVlihRPklw8b7skSBP16Y")
    bot_m.send_message(-677235937,'12点-追击运行失败。。。')
    bot_m.stop_polling()


end = int(time.time())
print(f'今日新增数量：{len(result)} ')
print(f'运行时间： {end-start}s')


