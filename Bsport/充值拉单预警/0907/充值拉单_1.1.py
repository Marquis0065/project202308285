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


def job():
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
    token = obj0['data']['token']

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
    dic0 = {'充值日期':"createDate",'充值单号':"orderId",'用户层级':"userLevel",'账户名':"username",'姓名':"reallyName",'VIP等级':"vipLevel",'充值金额':"amount",'到账金额':"payAmount"}
    dic = {'充值日期':[],'充值单号':[],'用户层级':[],'账户名':[],'姓名':[],'VIP等级':[],'充值金额':[],'到账金额':[]}
    for page in range(1,60):
        data = {
            'dateType':'1',
            'startTime':int(time.time()-(24*60*60))*1000,
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
    df = pd.DataFrame(dic)
    df.insert(1,'时间',df['充值日期'].map(lambda x:time.strftime("%H:%M")))
    df['充值日期']= df['充值日期'].map(lambda x:time.strftime("%Y-%m-%d"))

    result = df.groupby('账户名').agg({'账户名':len,'充值金额':[np.max,np.mean],'VIP等级':np.mean})
    result.reset_index(inplace=True)
    result = pd.DataFrame({'账户名':result.iloc[:,0],'数量':result.iloc[:,1],'最大金额':result.iloc[:,2],'平均金额':result.iloc[:,3],'VIP等级':result.iloc[:,4]})

    result.set_index('账户名',inplace=True)
    result = result.loc[result['数量']>10,:]
    df.set_index('账户名',inplace=True)
    print(result.sort_values('数量',ascending=False))

    # 写入数据
    fw = open('result2.txt','w')

    for name in result.index:
        fw.write(f'会员等级：{int(result.loc[name,"VIP等级"])}\n')
        fw.write(f'账号：{name}\n')
        fw.write(f'最大充值金额：{int(result.loc[name,"最大金额"])}\n')
        fw.write(f'平均充值金额：{int(result.loc[name,"平均金额"])}\n')
        fw.write(f'24小时内申请次数：{result.loc[name,"数量"]}\n')
        fw.write('---------------\n')
    fw.write(f'总计：{len(result.index)}')
    fw.close()
    with open('result2.txt','r') as fr:
        text = fr.read()
    bot_da = telebot.TeleBot('6106076754:AAHjxPSBpyjwpY-lq1iEslUufW46XQvAfr0') # -953042672
    #bot_m = telebot.TeleBot("6377312623:AAGz3ZSMVswWq0QVlihRPklw8b7skSBP16Y")
    # bot_a = telebot.TeleBot('6321364690:AAFvTiujKew0Fqi6OfL6awyM5Nx2LscJbVs')
    # bot_da.send_message(-677235937,text)
    bot_da.send_message(-996504819,text)
    bot_da.stop_polling()

while 1:
    job()
    time.sleep(600)