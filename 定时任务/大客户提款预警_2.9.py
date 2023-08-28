import time
import datetime
import requests
import json
import telebot
import hmac, base64, struct, hashlib
import platform
from selenium import webdriver

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
# 生成验证码
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
# selenium 保持登录
# browser = webdriver.Chrome()
# browser.get('http://fundmng.bsportsadmin.com/')
# browser.add_cookie({'name':'admin-uid','value':'690'})
# browser.add_cookie({'name': 'admin-token', 'value': token})
# print(browser.get_cookies())
# # browser.get('http://fundmng.bsportsadmin.com/api/manage/system/auth/init/system/list')
# browser.get('http://fundmng.bsportsadmin.com/api/manage/digital/coin/list')
pages = 20
now_time = int(time.time())
day_time = (now_time - (now_time-time.timezone)%86400)*1000

url = 'http://fundmng.bsportsadmin.com/api/manage/fund/withdraw/record/list/history'

session = requests.session()

dict_orderID = {}
header = {
    'Accept': 'application/json, text/plain, */*',
    # 'Accept-Encoding':'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Length': '292',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'admin-token=67c8b1bd1b434f898ed8570a860355b8; admin-uid=690',
    'Device_id': '1.0',
    'Gl_version': '2.0',
    'Host': 'fundmng.bsportsadmin.com',
    'Language': 'zh_CN',
    'Menuid': '100504',
    'Opeartionmenu': '%u8D22%u52A1%u7BA1%u7406-%u63D0%u73B0%u8BA2%u5355%u8BB0%u5F55',
    'Origin': 'http://fundmng.bsportsadmin.com',
    'Os_type': '0',
    'Referer': 'http://fundmng.bsportsadmin.com/system/financial-management/withdraw-record',
    'Sign': '525f286b21988b7c6a79f623f62f9695',
    'Some': 'header',
    'Systemid': '50',
    'Timestamp': '1691886184000',
    'Token': token,
    'Uid': '690',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Version': '1.0'
}
for i in range(1, pages):

    data = {
        'page': i,
        'size': 20,
        'aisleType': '1,2,3,4',
        'vipLevel': '0,1,2,3,4,5,6,7,8,9,10,11',
        'dateType': '1',
        'withdrawStatus[0]': '0',
        'withdrawStatus[1]': '10',
        'withdrawStatus[2]': '11',
        'withdrawStatus[3]': '16',
        'userType': '-1',
        'minAmount': 10000,
        'coinCode': 'CNY',
        'startTime': day_time,
        'endTime': 1725206399999
    }

    response = session.post(url=url, data=data, headers=header,timeout=100)
    # print(response.status_code,page)
    response.encoding = 'utf-8'

    obj = json.loads(response.text)

    for i in obj['data']['list']:
        if (i["durationEnd"] == 0) and (i["vipLevel"] > 5) and (
                now_time - (i["createDate"] // 1000) >= 7200):
            dict_orderID[i["orderId"]] = now_time - i["createDate"] // 1000


def job():
    # 生成验证码
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
        'Accept': 'application/json, text/plain, */*',
        # 'Accept-Encoding':'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Length': '292',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'admin-token=67c8b1bd1b434f898ed8570a860355b8; admin-uid=690',
        'Device_id': '1.0',
        'Gl_version': '2.0',
        'Host': 'fundmng.bsportsadmin.com',
        'Language': 'zh_CN',
        'Menuid': '100504',
        'Opeartionmenu': '%u8D22%u52A1%u7BA1%u7406-%u63D0%u73B0%u8BA2%u5355%u8BB0%u5F55',
        'Origin': 'http://fundmng.bsportsadmin.com',
        'Os_type': '0',
        'Referer': 'http://fundmng.bsportsadmin.com/system/financial-management/withdraw-record',
        'Sign': '525f286b21988b7c6a79f623f62f9695',
        'Some': 'header',
        'Systemid': '50',
        'Timestamp': '1691886184000',
        'Token': token,
        'Uid': '690',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Version': '1.0'
    }
    fp = open('大客户提款预警_0803.txt', 'w')
    now_current = int(time.time())
    # day_current = (now_current - (now_time-time.timezone)%86400)*1000
    yesterday = datetime.date.today() + datetime.timedelta(days=-1)
    yesterday_start_time=int(time.mktime(time.strptime(str(yesterday), '%Y-%m-%d')))

    sum_ = 0
    for page in range(1, pages):
        data = {
            'page': page,
            'size': 20,
            'aisleType': '1,2,3,4',
            'vipLevel': '0,1,2,3,4,5,6,7,8,9,10,11',
            'dateType': '1',
            'withdrawStatus[0]': '0',
            'withdrawStatus[1]': '10',
            'withdrawStatus[2]': '11',
            'withdrawStatus[3]': '16',
            'userType': '-1',
            'minAmount': 10000,
            'coinCode': 'CNY',
            'startTime': yesterday_start_time*1000,
            'endTime': 1725206399999
        }

        response = session.post(url=url, data=data, headers=header,timeout=100)
        # print(response.status_code,page)
        response.encoding = 'utf-8'

        obj = json.loads(response.text)

        for i in obj['data']['list']:
            if (i["durationEnd"] == 0) and (i["vipLevel"] > 5) and (now_current - i["createDate"] // 1000 >= 7200):
                try:
                    print([i["vipLevel"], i["reallyName"], i['username'], '金额:{}'.format(int(i["amount"])),
                           '风控审核时间：'+str((divmod((now_current * 1000) - i["riskApvTime"], 60000))[0]) + '分钟',
                           '总耗时：' + str((divmod((now_current * 1000) - i["createDate"], 60000))[0]) + '分钟',
                           '提现单号'+i["orderId"]])
                except:
                    print([i["vipLevel"], i["reallyName"], i['username'], '金额:{}'.format(int(i["amount"])),
                           '风控审核时间：无',
                           '总耗时：' + str((divmod((now_current * 1000) - i["createDate"], 60000))[0]) + '分钟',
                           '提现单号' + i["orderId"]])
                if i["orderId"] in dict_orderID:
                    if ((now_current - i["createDate"] // 1000) - dict_orderID[i["orderId"]]) >= 3600:
                        fp.write('会员等级：{}\n'.format(i["vipLevel"]))
                        fp.write('账号：{}\n'.format(i["username"]))
                        fp.write('金额：{}\n'.format(i["amount"]))
                        fp.write('提现单号：{}\n'.format(i["orderId"]))
                        fp.write('状态：风险审核通过\n')
                        try:
                            fp.write('出款耗时：{}'.format(
                                (divmod((now_current * 1000) - i["riskApvTime"], 60000))[0]) + '分钟\n')
                        except:
                            fp.write('出款耗时：无\n')
                        fp.write(
                            '总耗时：{}'.format((divmod((now_current * 1000) - i["createDate"], 60000))[0]) + '分钟\n')
                        fp.write('-------------------------------------\n')
                        sum_ += 1
                        dict_orderID[i["orderId"]] = now_current - i["createDate"] // 1000
                else:
                    dict_orderID[i["orderId"]] = now_current - i["createDate"] // 1000
                    fp.write('会员等级：{}\n'.format(i["vipLevel"]))
                    fp.write('账号：{}\n'.format(i["username"]))
                    fp.write('金额：{}\n'.format(i["amount"]))
                    fp.write('提现单号：{}\n'.format(i["orderId"]))
                    fp.write('状态：风险审核通过\n')
                    try:
                        fp.write('出款耗时：{}'.format((divmod((now_current * 1000) - i["riskApvTime"], 60000))[0]) + '分钟\n')
                    except:
                        fp.write('出款耗时：无\n')
                    fp.write('总耗时：{}'.format((divmod((now_current * 1000) - i["createDate"], 60000))[0]) + '分钟\n')
                    fp.write('-------------------------------------\n')
                    sum_ += 1

    print('字典人数: '+str(len(dict_orderID)))
    print(dict_orderID)
    print(f'sum_: {sum_}')
    bot_da = telebot.TeleBot('6106076754:AAHjxPSBpyjwpY-lq1iEslUufW46XQvAfr0')
    #bot_m = telebot.TeleBot("6377312623:AAGz3ZSMVswWq0QVlihRPklw8b7skSBP16Y")
    bot_a = telebot.TeleBot('6321364690:AAFvTiujKew0Fqi6OfL6awyM5Nx2LscJbVs')
    if sum_ > 0:
        fp.write(f'总计：{sum_}')
        fp.close()
        r_fp = open('大客户提款预警_0803.txt', 'r')
        text = r_fp.read()
        r_fp.close()

        #bot_m.send_message(-677235937, '姓名、账号、提款金额、提款时间已超出60分钟请协助推进！')
        # bot_m.send_message(-677235937, r_fp.read())  -812533282
        # bot_a.send_message(-677235937,text,timeout=1000)
        bot_a.send_message(-812533282,text,timeout=1000)
        #bot_da.send_message(-953042672, '姓名、账号、提款金额、提款时间已超出60分钟请协助推进！')
        # bot_da.send_message(-953042672, text,timeout=1000)
        # bot_da.send_message(6255966584, text,timeout=1000)

    else:
        #bot_da.send_message(-677235937, '大客户提款预警当前无数据：'+time.strftime('%H:%M:%S',time.localtime()))
        bot_da.send_message(6255966584, '当前无数据',timeout=1000)
        bot_da.send_message(6279115720, '当前无数据',timeout=1000)
        print('当前无数据：'+time.strftime('%H:%M:%S',time.localtime()))
        # bot_da.send_message(6255966584, '当前无数据',timeout=1000)
        # bot_da.send_message(6279115720, '当前无数据',timeout=1000)
    bot_da.stop_polling()
    bot_a.stop_polling()


def loop():
    while 1:
        job()
        time.sleep(600)
if __name__ == '__main__':
    loop()




