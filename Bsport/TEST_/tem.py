import os
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
import warnings
warnings.filterwarnings('ignore')

# pd.set_option('display.max_colwidth', None) #显示单元格完整信息
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

day = 0
pages_user = 150
pages_fircharge = 60
access_token ='24.675734f72d0e4eca2188e368bb9871be.2592000.1696930532.282335-38761358'
start_date = (datetime.datetime.now()+datetime.timedelta(days=day)).strftime('%Y%m%d')
end_date = (datetime.datetime.now()+datetime.timedelta(days=day)).strftime('%Y%m%d')


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

# 获取今日数据
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

dic_website = {}
for k,v in zip(jsonpath.jsonpath(json.loads(response.text),'$..domain'),jsonpath.jsonpath(json.loads(response.text),'$..site_id')):
    dic_website[k]=v
# with open(r'C:\Users\User\Desktop\SEO\12-18\dic_website.txt','r') as f:
#     dic_website=f.read()
# print(dic_website)
print(dic_website)