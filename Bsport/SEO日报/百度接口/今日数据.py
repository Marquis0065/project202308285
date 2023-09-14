# 获取 siteid字典
import time
import xlwings as xw
import jsonpath
import requests
import json
import pandas as pd
import datetime

day = -1
access_token = '121.1e832791a57b87542b2bb51e2f3f5bfa.Y_Uhf0W55kh6mBiTGZX0qWg0O5ZqJYZmPyHTqi8.HEyD3w'
start_date = (datetime.datetime.now()+datetime.timedelta(days=day)).strftime('%Y%m%d')
end_date = (datetime.datetime.now()+datetime.timedelta(days=day)).strftime('%Y%m%d')
# (datetime.datetime.now()+datetime.timedelta(days=day)).strftime('%Y/%m/%d')
shuju = {'domain':[],
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

# url_siteid = 'https://openapi.baidu.com/rest/2.0/tongji/config/getSiteList?access_token=24.f6c93d2eb8f209b114cd9acfeb6d1765.2592000.1697001874.282335-38761358'
# response = requests.get(url_siteid)
# response.encoding='utf-8'
# print(response.text)
# jsonpath.jsonpath(json.loads(response.text),'$..site_id')
# jsonpath.jsonpath(json.loads(response.text),'$..domain')
# dic_website = {}
# for k,v in zip(jsonpath.jsonpath(json.loads(response.text),'$..domain'),jsonpath.jsonpath(json.loads(response.text),'$..site_id')):
#     dic_website[k]=v
with open(r'C:\Users\User\Desktop\SEO\12-18\dic_website.txt','r') as f:
    dic_website=eval(f.read())
# 分别获取各网站数据
app = xw.App(visible=False,add_book=False)
book = app.books.open(r'C:\Users\User\Desktop\SEO\seo数据(当天)\今日数据(当天).xlsx')
sheet_web = book.sheets['网站概况']
sheet_qishu = book.sheets['趋势分析']
for k in dic_website:
    url_web = f'https://openapi.baidu.com/rest/2.0/tongji/report/getData?access_token={access_token}&site_id={dic_website[k]}&method=overview/getTimeTrendRpt&start_date={start_date}&end_date={end_date}&metrics=pv_count,visitor_count,ip_count'
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
    print(k,result_pv_uv_ip)
    shuju['domain'].append(k)
    shuju['日期'].append((datetime.datetime.now()+datetime.timedelta(days=day)).strftime('%Y/%m/%d'))
    shuju['pv'].append(result_pv_uv_ip[0])
    shuju['uv'].append(result_pv_uv_ip[1])
    shuju['ip'].append(result_pv_uv_ip[2])
    time.sleep(1)
sheet_web.range('A2').options(index=False,header = False).value = pd.DataFrame(shuju)
sheet_qishu.range('A2').options(index=False,header = False).value = pd.DataFrame(qishi)
book.save(rf'C:\Users\User\Desktop\SEO\seo数据(当天)\今日数据-{start_date}.xlsx')
app.quit()
print(pd.DataFrame(qishi))


