import os
import warnings
warnings.filterwarnings('ignore')
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
from openpyxl import Workbook, load_workbook
from openpyxl import formatting, styles
from openpyxl.styles import Color, PatternFill, Font, Border
from PIL import ImageGrab
import pyperclip

pd.set_option('display.max_colwidth', None) #显示单元格完整信息
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

day = -32
start_date = (datetime.datetime.now()+datetime.timedelta(days=day)).strftime('%Y%m%d')
end_date = (datetime.datetime.now()+datetime.timedelta(days=day)).strftime('%Y%m%d')
pages_user = 150
pages_fircharge = 60
# with open(r'C:\Users\User\Desktop\SEO\SEO代码新 0903到期.txt','r') as f:
#     access_token = f.read()
# 启动控制台

url = 'http://fundmng.bsportsadmin.com/api/manage/fund/withdraw/record/list/history'
session = requests.session()

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

# selenium模拟浏览器,并运行jar包，生成今日数据
# 指定文件夹路径
# folder_path = r'C:\Users\User\Desktop\SEO\_0816'
# # 指定文件名
# file_name = '今日数据.xlsx'
# # 判断文件是否存在
# file_path = os.path.join(folder_path, file_name)
# if os.path.exists(file_path):
#     os.remove(file_path)

## python接口提取今日数据
print('启动百度统计API----')
shuju_website = {'domain':[],
                 '日期':[],
                 'pv':[],
                 'uv':[],
                 'ip':[]}
qishi = {'domain':[],
         '日期':[],
         '时间':[],
         'pv':[],
         'uv':[],
         'ip':[]}

url_siteid = 'https://openapi.baidu.com/rest/2.0/tongji/config/getSiteList?access_token=121.1e832791a57b87542b2bb51e2f3f5bfa.Y_Uhf0W55kh6mBiTGZX0qWg0O5ZqJYZmPyHTqi8.HEyD3w'
response = requests.get(url_siteid)
# jsonpath.jsonpath(json.loads(response.text),'$..site_id')
# jsonpath.jsonpath(json.loads(response.text),'$..domain')
dic_website = {}
for k,v in zip(jsonpath.jsonpath(json.loads(response.text),'$..domain'),jsonpath.jsonpath(json.loads(response.text),'$..site_id')):
    dic_website[k]=v

# 分别获取各网站数据
app = xw.App(visible=False,add_book=False)
book = app.books.open(r'C:\Users\User\Desktop\SEO\截图文件\今日数据(python接口).xlsx')
sheet1 = book.sheets['网站概况']
sheet1.range('A2').clear_contents()
sheet_qishu = book.sheets['趋势分析']
sheet_qishu.range('A2').clear_contents()
for k in dic_website:
    url_web = f'https://openapi.baidu.com/rest/2.0/tongji/report/getData?access_token=121.1e832791a57b87542b2bb51e2f3f5bfa.Y_Uhf0W55kh6mBiTGZX0qWg0O5ZqJYZmPyHTqi8.HEyD3w&site_id={dic_website[k]}&method=overview/getTimeTrendRpt&start_date={start_date}&end_date={end_date}&metrics=pv_count,visitor_count,ip_count'
    response = requests.get(url_web)
    response.encoding='utf8'
    # 趋势数据
    for i in range(24):
        qishi['domain'].append(k)
        qishi['日期'].append((datetime.datetime.now()+datetime.timedelta(days=day)).strftime('%Y/%m/%d'))
        qishi['时间'].append(i)
        qishi['pv'].append(json.loads(response.text)['result']['items'][1][i][0])
        qishi['uv'].append(json.loads(response.text)['result']['items'][1][i][1])
        qishi['ip'].append(json.loads(response.text)['result']['items'][1][i][2])
    result_pv_uv_ip = []
    # 遍历列表并相加元素
    for i in range(3):
        sum = 0
        for j in range(len(json.loads(response.text)['result']['items'][1])):
            try:
                sum += json.loads(response.text)['result']['items'][1][j][i]
            except:
                sum +=0
        result_pv_uv_ip.append(sum)

    shuju_website['domain'].append(k)
    shuju_website['日期'].append((datetime.datetime.now()+datetime.timedelta(days=day)).strftime('%Y/%m/%d'))
    shuju_website['pv'].append(result_pv_uv_ip[0])
    shuju_website['uv'].append(result_pv_uv_ip[1])
    shuju_website['ip'].append(result_pv_uv_ip[2])
    time.sleep(1)
sheet1.range('A2').options(index=False,header = False).value = pd.DataFrame(shuju_website)
sheet_qishu.range('A2').options(index=False,header = False).value = pd.DataFrame(qishi)
book.save()
app.quit()
print('今日数据获取完毕！')