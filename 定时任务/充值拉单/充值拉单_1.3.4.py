import datetime
import time
import pandas as pd
import requests
import json
import pandas as pd
import numpy as np
from jsonpath import jsonpath
import telebot
import hmac, base64, struct, hashlib
import platform

dic_chartype= {'CNY_支付宝':['支付宝支付', '支付宝转账', '支付宝H5', '支付宝红包', '极速支付宝', '支付宝扫码', '支付宝转卡'],
               'CNY_微信':['微信支付', '微信转账', '微信扫码', '微信红包', '微信H5', '微信小店', '极速微信', '微信转卡'],
               'CNY_其他第三方':['QQ支付','京东支付','云闪付转账',
                                 '云闪付','充值卡支付','数字人民币','极速QQ','云闪付转卡','极速零钱','钉钉红包','QQ红包','综合支付','京东E卡'],
               'CNY_网银':['网银支付', '银联扫码支付', '网银转账', '银联快捷', '手机银行', '银行卡直充', '人民币直充'],
               'CNY_银行卡':['银行卡转账', '银行卡转卡', '银行卡支付'],
               'CNY_虚拟币':['EB_Pay', 'TO_Pay', '虚拟币支付'],
               'VND_银行卡':['越南Bank_online', '越南Local_bank', '越南银行转账'],
               'VND_第三方':['越南Momo_pay', '越南Zalo_pay', '越南Qr_pay', '越南Viettel_Pay'],
               'MYR_银行卡':['马来西亚_银行转账', '马来西亚Bank_online'],
               'THB_银行卡':['泰国_银行转账', '泰国Bank_online'],
               'THB_第三方':['泰国PROMPT_PAY', '泰国TRUE_MONEY', '泰国RABBIT_LINE_PAY'],
               'BRL_银行卡':['巴西_银行卡转账', '巴西_网银支付'],
               'BRL_第三方':['巴西PIX_Pay'],
               'EGP_银行卡':['埃及_银行卡转账', '埃及Bank_online']}

paymentID = '1,2,3,4,5,6,7,8,9,10,11,24,25,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,1000,1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012,2000,2001,2002,2003,2004,2005,2006,3000,3001,4000,4001,4002,4003,4004,8000,8001,8002,10000,10001'.split(',')
chongchi = pd.read_excel(r'C:\Users\User\Desktop\文件\定时任务\充值拉单\充值拉单监控群分类大项2.xlsx','Sheet2')
dic_chongchi = {}
for i ,j in zip(paymentID,chongchi['充值方式'].tolist()):
    dic_chongchi[i]=j


# google验证码函数
submit_url = 'http://fundmng.bsportsadmin.com/api/manage/user/admin/login/submit'
header0 = {
    'Device_id':'1.0',
    'Os_type':'0',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
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

# 生成验证码
print('生成google验证码。。。')
google_code = get_google_code('64ehnxj6yily5bhv23kgb62ozuh6yuu2')
data0 = {
    'username': 'Marquis',
    'password': 'qwer123456',
    'code': google_code
}
# 获取token
print('获取token中。。。')
session0 = requests.Session()
response0  =session0.post(url=submit_url,data=data0,headers=header0)
response0.encoding = 'utf-8'
obj0 = json.loads(response0.text)
token0 = obj0['data']['token']

# 发送请求
print('开始发送请求....')
url = 'http://fundmng.bsportsadmin.com/api/manage/fund/recharge/record/list'
header = {
    'Device_id': '1.0',
    'Os_type': '0',
    'Sign': '525f286b21988b7c6a79f623f62f9695',
    'Timestamp': '1691886184000',
    'Token': token0,
    'Uid': '690',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Version': '1.0'
}
session  = requests.Session()
data_ori = {
    'dateType':'1',
    'startTime':int(time.time()-(120*60))*1000,
    'endTime':int(time.time())*1000,
    'userType':'-1',
    'orderStatus':'0,1,2,3,4,5,6,7,8,9',
    'agentType':'-1',
    'page':1,
    'size':500,
    'paymentIdList':'1,2,3,4,5,6,7,8,9,10,11,24,25,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,1000,1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012,2000,2001,2002,2003,2004,2005,2006,3000,3001,4000,4001,4002,4003,4004,8000,8001,8002,10000,10001',
    'coinCode':'CNY'
}
response_ori = session.post(url=url,headers=header,data=data_ori)
pages = json.loads(response_ori.text)['data']['pages']
print(f'共{pages}页。。')

dic0 = {'充值日期':"createDate",'充值单号':"orderId",'用户层级':"userLevel",'账户名':"username",'姓名':"reallyName",'VIP等级':"vipLevel",'充值金额':"amount",'到账金额':"payAmount"}
dic = {'充值日期':[],'充值单号':[],'用户层级':[],'账户名':[],'姓名':[],'VIP等级':[],'充值金额':[],'到账金额':[]}
ori_dic={}
for page in range(1,pages+1):
    data = {
        'dateType':'1',
        'startTime':int(time.time()-(120*60))*1000,
        'endTime':int(time.time())*1000,
        'userType':'-1',
        'orderStatus':'0,1,2,3,4,5,6,7,8,9',
        'agentType':'-1',
        'page':page,
        'size':500,
        'paymentIdList':'1,2,3,4,5,6,7,8,9,10,11,24,25,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,1000,1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012,2000,2001,2002,2003,2004,2005,2006,3000,3001,4000,4001,4002,4003,4004,8000,8001,8002,10000,10001',
        'coinCode':'CNY'
    }

    response = session.post(url=url,headers=header,data=data)
    response.encoding = 'utf8'

    # 提取数据

    obj0 = json.loads(response.text)
    for i in obj0['data']['list']:
        # if (i["userLevel"] == '多次拉单不付款层级' and i["payAmount"] ==0 ):
        if (i["userLevel"] == '多次拉单不付款层级' and i["payAmount"] ==0 and i["vipLevel"] > -1):
            for k in dic:
                dic[k].append(i[dic0[k]])
# 生成结果数据
df = pd.DataFrame(dic)
df.insert(1,'时间',df['充值日期'].map(lambda x:time.strftime("%H:%M")))
df['充值日期']= df['充值日期'].map(lambda x:time.strftime("%Y-%m-%d"))

result = df.groupby('账户名').agg({'账户名':len,'充值金额':[np.max,np.mean],'VIP等级':np.mean})
result.reset_index(inplace=True)
result = pd.DataFrame({'账户名':result.iloc[:,0],'数量':result.iloc[:,1],'最大金额':result.iloc[:,2],'平均金额':result.iloc[:,3],'VIP等级':result.iloc[:,4]})

result.set_index('账户名',inplace=True)
result = result.loc[result['数量']>7,:]
df.set_index('账户名',inplace=True)
print(result)
ori_dic={}
for name in result.index:
    ori_dic[name]=int(time.time())

#加载会员代理线列表
user1 = pd.read_excel(r'C:\Users\User\Desktop\文件\定时任务\会员列表更新\会员总表2022.xlsx')
user2 = pd.read_excel(r'C:\Users\User\Desktop\文件\定时任务\会员列表更新\会员总表2023.xlsx')
# 2023年会员列表去重
user2.drop_duplicates(inplace=True)
huiyuan_all = user1.append(user2)
huiyuan_all = huiyuan_all.iloc[:,:2]
#修改列名
huiyuan_all=huiyuan_all.rename(columns={'代理':'上级代理'})
daili = pd.read_csv(r'\\DESKTOP-OABVORH\Data\Code2023-10数据库版\输出数据\每日更新\代理列表\代理列表.csv')
print('零点会员列表：',huiyuan_all.shape)

num_ = 0
def job():
    # 生成验证码
    sum_ = 0
    print('job开始，生成google验证码。。。')
    google_code = get_google_code('64ehnxj6yily5bhv23kgb62ozuh6yuu2')
    data = {
        'username': 'Marquis',
        'password': 'qwer123456',
        'code': google_code
    }
    # 获取token
    print('获取token中。。。')

    response  =session0.post(url=submit_url,data=data,headers=header0)
    response.encoding = 'utf-8'
    obj = json.loads(response.text)
    token = obj['data']['token']

    # 发送请求
    print('开始发送请求....')
    url = 'http://fundmng.bsportsadmin.com/api/manage/fund/recharge/record/list'
    header = {
        'Device_id': '1.0',
        'Os_type': '0',
        'Sign': '525f286b21988b7c6a79f623f62f9695',
        'Timestamp': '1691886184000',
        'Token': token,
        'Uid': '690',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Version': '1.0'
    }
    session  = requests.Session()
    dic0 = {'充值日期':"createDate",'充值单号':"orderId",'用户层级':"userLevel",'账户名':"username",'姓名':"reallyName",'VIP等级':"vipLevel",'充值金额':"amount",'到账金额':"payAmount",'充值方式':"paymentId"}
    dic = {'充值日期':[],'充值单号':[],'用户层级':[],'账户名':[],'姓名':[],'VIP等级':[],'充值金额':[],'到账金额':[],'充值方式':[]}
    fw = open('result-912.txt','w')
    # 重新获取页码
    data_sec = {
        'dateType':'1',
        'startTime':int(time.time()-(180*60))*1000,
        'endTime':int(time.time())*1000,
        'userType':'-1',
        'orderStatus':'0,1,2,3,4,5,6,7,8,9',
        'agentType':'-1',
        'page':1,
        'size':500,
        'paymentIdList':'1,2,3,4,5,6,7,8,9,10,11,24,25,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,1000,1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012,2000,2001,2002,2003,2004,2005,2006,3000,3001,4000,4001,4002,4003,4004,8000,8001,8002,10000,10001',
        'coinCode':'CNY'
    }
    response_sec = session.post(url=url,headers=header,data=data_sec)
    pages = json.loads(response_sec.text)['data']['pages']
    print(f'共{pages}页。。')

    for page in range(1,pages+1):
        data = {
            'dateType':'1',
            'startTime':int(time.time()-(120*60))*1000,
            'endTime':int(time.time())*1000,
            'userType':'-1',
            'orderStatus':'0,1,2,3,4,5,6,7,8,9',
            'agentType':'-1',
            'page':page,
            'size':500,
            'paymentIdList':'1,2,3,4,5,6,7,8,9,10,11,24,25,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,1000,1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012,2000,2001,2002,2003,2004,2005,2006,3000,3001,4000,4001,4002,4003,4004,8000,8001,8002,10000,10001',
            'coinCode':'CNY'
        }

        response = session.post(url=url,headers=header,data=data)
        response.encoding = 'utf8'

        # 提取数据

        obj = json.loads(response.text)
        for i in obj['data']['list']:
            # if (i["userLevel"] == '多次拉单不付款层级' and i["payAmount"] ==0 ):
            if (i["userLevel"] == '多次拉单不付款层级' and i["payAmount"] ==0 and i["vipLevel"] > -1):
                for k in dic:
                    dic[k].append(i[dic0[k]])
    # 生成结果数据
    df2 = pd.DataFrame(dic)
    df2.insert(1,'时间',df2['充值日期'].map(lambda x:time.strftime("%H:%M")))
    df2['充值日期']= df2['充值日期'].map(lambda x:time.strftime("%Y-%m-%d"))
    #处理充值方式
    df2['充值方式2']= df2['充值方式'].astype(str).map(dic_chongchi)
    for i in df2['充值方式2']:
        for k in dic_chartype:
            if i in dic_chartype[k]:
                df2.loc[df2['充值方式2']==i,'充值方式3']=k


    result2 = df2.groupby('账户名').agg({'账户名':len,'充值金额':[np.max,np.mean],'VIP等级':np.mean,'充值方式3':set})
    result2.reset_index(inplace=True)
    result2 = pd.DataFrame({'账户名':result2.iloc[:,0],'数量':result2.iloc[:,1],'最大金额':result2.iloc[:,2],'平均金额':result2.iloc[:,3],'VIP等级':result2.iloc[:,4],'分类':result2.iloc[:,5]})

    result2.set_index('账户名',inplace=True)
    result2 = result2.loc[result2['数量']>3,:]
    df2.set_index('账户名',inplace=True)
    print(result2.sort_values('数量',ascending=False))
    print('result2:',result2.shape)


    # 获取当前时间
    now = datetime.datetime.now()
    # 获取昨日8点的时间
    yesterday_8am = datetime.datetime(now.year, now.month, now.day-1, 8)
    # 将时间转换为时间戳
    yes_8am = int(yesterday_8am.timestamp())*1000+1000
    url_huiyuan = 'http://fundmng.bsportsadmin.com/api/manage/user/maintain/user/list'
    data_huiyuan = {
        'username': 'Marquis',
        'password': 'qwer123456',
        'code': get_google_code('64ehnxj6yily5bhv23kgb62ozuh6yuu2')
    }
    header_hui = {
        'Device_id':'1.0',
        'Os_type':'0',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }
    response  =session0.post(url=submit_url,data=data_huiyuan,headers=header_hui)
    response.encoding = 'utf-8'
    obj = json.loads(response.text)
    token = obj['data']['token']

    header_huiyuan = {
        'Device_id': '1.0',
        'Os_type': '0',
        'Sign': 'd86257d4abd6fa45c67bd4ee02f71ba2',
        'Timestamp': '1697599199000',
        'Token': token,
        'Uid': '690',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Version': '1.0'
    }


    dic_huiyuan={'会员账号':[],'上级代理':[]}
    for page in range(1,25):
        data_huiyuan ={
            'page':page,
            'size':200,
            'userVip':'0,1,2,3,4,5,6,7,8,9,10,11',
            'status':'0,1,2,4',
            'sortType':'3',
            'sortStr':'descend',
            'searchType':'1',
            'channelId':'34',
            'registeredStartDate':yes_8am,
            'registeredEndDate':int(time.time())*1000
        }
        response = requests.post(url=url_huiyuan,data=data_huiyuan,headers=header_huiyuan)
        response.encoding = 'utf8'
        obj = json.loads(response.text)
        for i in obj['data']['list']:
            dic_huiyuan['会员账号'].append(i['username'])
            dic_huiyuan['上级代理'].append(i['parentName'])

    today_huiyuan =pd.DataFrame(dic_huiyuan)

    global huiyuan_all
    huiyuan_all = pd.concat([huiyuan_all,today_huiyuan])
    print('增加今日后会员数量：',huiyuan_all.shape)
    huiyuan_all.drop_duplicates('会员账号',inplace=True)
    print('去重后：',huiyuan_all.shape)

    huiyuan_daili = huiyuan_all.merge(daili,on='上级代理',how='left')
    huiyuan_daili.drop_duplicates('会员账号',inplace=True)
    huiyuan_daili.set_index('会员账号',inplace=True)

    #匹配代理线
    result2 = result2.join(huiyuan_daili)
    result2 = result2.fillna('-')
    result2['最大金额']=result2['最大金额'].astype(int)
    result2['平均金额']=result2['平均金额'].astype(int)
    result2['VIP等级']=result2['VIP等级'].astype(int)
    print('result22:',result2.shape)
    print(result2)

    #去除重复index
    result2 = result2[~result2.index.duplicated()]

    # 写入数据
    for user in result2.index:
        if user in ori_dic:
            if int(time.time())-ori_dic[user] >600:

                fw.write(f'会员等级：{result2.loc[user,"VIP等级"]}\n')
                fw.write(f'账号：{" "}{user}\n')
                fw.write(f'上级代理：{" "}{result2.loc[user,"上级代理"]}\n')
                fw.write(f'小组：{" "}{result2.loc[user,"小组"]}\n')
                fw.write(f'充值方式：')
                for i in list(result2.loc[user,"分类"]):
                    fw.write(i)
                    if len(result2.loc[user,"分类"])>1:
                        if i != list(result2.loc[user,"分类"])[-1]:
                            fw.write(' ,\n')
                            fw.write(f'{"           "}')
                fw.write('\n')
                fw.write(f'最大充值金额：{result2.loc[user,"最大金额"]}\n')
                fw.write(f'平均充值金额：{result2.loc[user,"平均金额"]}\n')
                fw.write(f'2小时内申请次数：{result2.loc[user,"数量"]}\n')
                fw.write('-----------------------\n')
                ori_dic[user]=int(time.time())
                sum_ +=1
        else:
            ori_dic[user]=int(time.time())
            fw.write(f'会员等级：{result2.loc[user,"VIP等级"]}\n')
            fw.write(f'账号：{" "}{user}\n')
            fw.write(f'上级代理：{" "}{result2.loc[user,"上级代理"]}\n')
            fw.write(f'小组：{" "}{result2.loc[user,"小组"]}\n')
            fw.write(f'充值方式：')
            for i in list(result2.loc[user,"分类"]):
                fw.write(i)
                if len(result2.loc[user,"分类"])>1:
                    if i != list(result2.loc[user,"分类"])[-1]:
                        fw.write(' ,\n')
                        fw.write(f'{"           "}')


            fw.write('\n')
            fw.write(f'最大充值金额：{result2.loc[user,"最大金额"]}\n')
            fw.write(f'平均充值金额：{result2.loc[user,"平均金额"]}\n')
            fw.write(f'2小时内申请次数：{result2.loc[user,"数量"]}\n')
            fw.write('-----------------------\n')
            ori_dic[user]=int(time.time())
            sum_ +=1

    print('字典人数: '+str(len(ori_dic)))
    print(ori_dic)
    print(f'sum_: {sum_}')

    # 发送
    global num_
    if sum_>0:
        num_ += 1
        fw.write(f'总计：{sum_}\n')
        fw.write(f'发送次数：{num_}\n')
        fw.close()
        with open('result-912.txt','r') as fr:
            text = fr.read()
        bot_da = telebot.TeleBot('6106076754:AAHjxPSBpyjwpY-lq1iEslUufW46XQvAfr0') # -953042672
        #bot_m = telebot.TeleBot("6377312623:AAGz3ZSMVswWq0QVlihRPklw8b7skSBP16Y")
        # bot_a = telebot.TeleBot('6321364690:AAFvTiujKew0Fqi6OfL6awyM5Nx2LscJbVs')
        # bot_da.send_message(-677235937,text)   -996504819
        bot_da.send_message(-677235937,text)
        bot_da.stop_polling()
    else:
        bot_da = telebot.TeleBot('6106076754:AAHjxPSBpyjwpY-lq1iEslUufW46XQvAfr0')
        bot_da.send_message(6279115720,'----1.3.4-idea----充值拉单')
        bot_da.stop_polling()

while 1:
    job()
    time.sleep(300)

