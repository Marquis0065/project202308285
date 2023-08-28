import pandas as pd
import numpy as np
import datetime
pd.set_option('display.max_colwidth', None) #显示单元格完整信息
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

user = pd.read_csv(r'C:\Users\User\Desktop\SEO\_0815\会员列表导出.csv',encoding='gbk')
firChargeUser = pd.read_csv(r'C:\Users\User\Desktop\SEO\_0815\会员首存报表.csv',encoding='gbk')
data = pd.read_excel(r'C:\Users\User\Desktop\SEO\_0815\今日数据.xlsx')
data_2 = pd.read_excel(r'C:\Users\User\Desktop\SEO\_0815\今日数据.xlsx','趋势分析')
daili = pd.read_excel(r'C:\Users\User\Desktop\SEO\_0807\SEO每日模板-每日更新.xlsx','代理总表')

user['注册时间']=pd.to_datetime(user['注册时间'])
hour_user= pd.merge(user,daili,how = 'left',left_on='代理',right_on='代理线')
hour_user['小时数']= hour_user['注册时间'].dt.hour
firChargeUser['注册时间']=pd.to_datetime(firChargeUser['注册时间'])
hour_charge = pd.merge(firChargeUser,daili,how='left',left_on='所属代理',right_on='代理线')
hour_charge['小时数']= hour_charge['注册时间'].dt.hour
dic ={'日期':(datetime.datetime.now()+datetime.timedelta(days=0)).strftime('%Y/%m/%d'),
      '人员':[i for i in ['Paddy', 'Tony', 'Max', 'Martin', 'Zed', 'Hugo', 'Aber', 'DK', 'Ben'] for j in range(7)],'指标':['接收率','发送IP数','接收IP数','注册','注册率','开户','开户转化率']*9, '总计':0, '0-2':0, '2-4':0, '4-6':0, '6-8':0, '8-10':0, '10-12':0, '12-14':0, '14-16':0, '16-18':0, '18-20':0, '20-22':0, '22-24':0}
df = pd.DataFrame(dic)

data_2['PV'] = pd.to_numeric(data_2['PV'],errors='coerce',downcast='integer')
data_2['UV'] = pd.to_numeric(data_2['UV'],errors='coerce',downcast='integer')
data_2['IP'] = pd.to_numeric(data_2['IP'],errors='coerce',downcast='integer')

# 循环方式
name_list = ['Martin','Paddy', 'Tony', 'Max',  'Zed', 'Hugo', 'Aber', 'DK', 'Ben']
hour_list = ['0-2', '2-4', '4-6', '6-8', '8-10', '10-12', '12-14', '14-16', '16-18', '18-20', '20-22', '22-24']


# Martin
for h in hour_list:
    df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),h] =data_2[data_2['网站名(domain)'].str.contains('redquan.com')&(data_2['时间']>=int(h.split('-')[0])) & (data_2['时间']<int(h.split('-')[1]))]['IP'].sum()
    df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),h] =data_2[data_2['网站名(domain)'].str.contains('martin.bty')&(data_2['时间']>=int(h.split('-')[0])) & (data_2['时间']<int(h.split('-')[1]))]['IP'].sum()
    df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),h] =len(hour_user[(hour_user['seo变化数据团队']=='martin') & (hour_user['小时数']>=int(h.split('-')[0]))& (hour_user['小时数']<int(h.split('-')[1]))])
    df.loc[(df['人员']=='Martin') & (df['指标']=='注册率'),h]=round(len(hour_user[(hour_user['seo变化数据团队']=='martin') & (hour_user['小时数']>=int(h.split('-')[0]))& (hour_user['小时数']<int(h.split('-')[1]))])/df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),h].iloc[0]*100,2)
    df.loc[(df['人员']=='Martin') & (df['指标']=='开户'),h] =len(hour_charge[(hour_charge['seo变化数据团队']=='martin') & (hour_charge['小时数']>=int(h.split('-')[0]))& (hour_charge['小时数']<int(h.split('-')[1]))])
    df.loc[(df['人员']=='Martin') & (df['指标']=='开户转化率'),h]=round(len(hour_charge[(hour_charge['seo变化数据团队']=='martin') & (hour_charge['小时数']>=int(h.split('-')[0]))& (hour_charge['小时数']<int(h.split('-')[1]))])/df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),h].iloc[0]*100,2)
    df.loc[(df['人员']=='Martin') & (df['指标']=='接收率'),h] =round(df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),h].iloc[0] / df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),h].iloc[0]*100,2)

# 7总计
df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'总计'] =df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'0-2':].T.sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'总计'] =df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'0-2':].T.sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'总计'] =df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'0-2':].T.sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='开户'),'总计'] =df.loc[(df['人员']=='Martin') & (df['指标']=='开户'),'0-2':].T.sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='开户转化率'),'总计'] =round(df.loc[(df['人员']=='Martin') & (df['指标']=='开户'),'总计'].iloc[0] / df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'总计'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='注册率'),'总计'] =round(df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'总计'].iloc[0] / df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'总计'].iloc[0]*100,2)

# 8接收率
df.loc[(df['人员']=='Martin') & (df['指标']=='接收率'),'总计'] =round(df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'总计'].iloc[0] / df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'总计'].iloc[0]*100,2)

#--------------------------------------------------------------------
# Paddy
for h in hour_list:
    df.loc[(df['人员']=='Paddy') & (df['指标']=='发送IP数'),h] =data_2[data_2['网站名(domain)'].str.contains('paddy.com')&(data_2['时间']>=int(h.split('-')[0])) & (data_2['时间']<int(h.split('-')[1]))]['IP'].sum()
    df.loc[(df['人员']=='Paddy') & (df['指标']=='接收IP数'),h] =data_2[data_2['网站名(domain)'].str.contains('paddy.bty')&(data_2['时间']>=int(h.split('-')[0])) & (data_2['时间']<int(h.split('-')[1]))]['IP'].sum()
    df.loc[(df['人员']=='Paddy') & (df['指标']=='注册'),h] =len(hour_user[(hour_user['seo变化数据团队']=='paddy') & (hour_user['小时数']>=int(h.split('-')[0]))& (hour_user['小时数']<int(h.split('-')[1]))])
    df.loc[(df['人员']=='Paddy') & (df['指标']=='注册率'),h]=round(len(hour_user[(hour_user['seo变化数据团队']=='paddy') & (hour_user['小时数']>=int(h.split('-')[0]))& (hour_user['小时数']<int(h.split('-')[1]))])/df.loc[(df['人员']=='Paddy') & (df['指标']=='接收IP数'),h].iloc[0]*100,2)
    df.loc[(df['人员']=='Paddy') & (df['指标']=='开户'),h] =len(hour_charge[(hour_charge['seo变化数据团队']=='paddy') & (hour_charge['小时数']>=int(h.split('-')[0]))& (hour_charge['小时数']<int(h.split('-')[1]))])
    df.loc[(df['人员']=='Paddy') & (df['指标']=='开户转化率'),h]=round(len(hour_charge[(hour_charge['seo变化数据团队']=='paddy') & (hour_charge['小时数']>=int(h.split('-')[0]))& (hour_charge['小时数']<int(h.split('-')[1]))])/df.loc[(df['人员']=='Paddy') & (df['指标']=='注册'),h].iloc[0]*100,2)
    df.loc[(df['人员']=='Paddy') & (df['指标']=='接收率'),h] =round(df.loc[(df['人员']=='Paddy') & (df['指标']=='接收IP数'),h].iloc[0] / df.loc[(df['人员']=='Paddy') & (df['指标']=='发送IP数'),h].iloc[0]*100,2)

# 7总计
df.loc[(df['人员']=='Paddy') & (df['指标']=='发送IP数'),'总计'] =df.loc[(df['人员']=='Paddy') & (df['指标']=='发送IP数'),'0-2':].T.sum()
df.loc[(df['人员']=='Paddy') & (df['指标']=='接收IP数'),'总计'] =df.loc[(df['人员']=='Paddy') & (df['指标']=='接收IP数'),'0-2':].T.sum()
df.loc[(df['人员']=='Paddy') & (df['指标']=='注册'),'总计'] =df.loc[(df['人员']=='Paddy') & (df['指标']=='注册'),'0-2':].T.sum()
df.loc[(df['人员']=='Paddy') & (df['指标']=='开户'),'总计'] =df.loc[(df['人员']=='Paddy') & (df['指标']=='开户'),'0-2':].T.sum()
df.loc[(df['人员']=='Paddy') & (df['指标']=='开户转化率'),'总计'] =round(df.loc[(df['人员']=='Paddy') & (df['指标']=='开户'),'总计'].iloc[0] / df.loc[(df['人员']=='Paddy') & (df['指标']=='注册'),'总计'].iloc[0]*100,2)
df.loc[(df['人员']=='Paddy') & (df['指标']=='注册率'),'总计'] =round(df.loc[(df['人员']=='Paddy') & (df['指标']=='注册'),'总计'].iloc[0] / df.loc[(df['人员']=='Paddy') & (df['指标']=='接收IP数'),'总计'].iloc[0]*100,2)

# 8接收率
df.loc[(df['人员']=='Paddy') & (df['指标']=='接收率'),'总计'] =round(df.loc[(df['人员']=='Paddy') & (df['指标']=='接收IP数'),'总计'].iloc[0] / df.loc[(df['人员']=='Paddy') & (df['指标']=='发送IP数'),'总计'].iloc[0]*100,2)

#-----------------------------------Tony----------
for h in hour_list:
    df.loc[(df['人员']=='Tony') & (df['指标']=='发送IP数'),h] =data_2[data_2['网站名(domain)'].str.contains('tonyb.com')&(data_2['时间']>=int(h.split('-')[0])) & (data_2['时间']<int(h.split('-')[1]))]['IP'].sum() // 2
    df.loc[(df['人员']=='Tony') & (df['指标']=='接收IP数'),h] =data_2[data_2['网站名(domain)'].str.contains('tony.bty')&(data_2['时间']>=int(h.split('-')[0])) & (data_2['时间']<int(h.split('-')[1]))]['IP'].sum()
    df.loc[(df['人员']=='Tony') & (df['指标']=='注册'),h] =len(hour_user[(hour_user['seo变化数据团队']=='tony') & (hour_user['小时数']>=int(h.split('-')[0]))& (hour_user['小时数']<int(h.split('-')[1]))])
    df.loc[(df['人员']=='Tony') & (df['指标']=='注册率'),h]=round(len(hour_user[(hour_user['seo变化数据团队']=='tony') & (hour_user['小时数']>=int(h.split('-')[0]))& (hour_user['小时数']<int(h.split('-')[1]))])/df.loc[(df['人员']=='Tony') & (df['指标']=='接收IP数'),h].iloc[0]*100,2)
    df.loc[(df['人员']=='Tony') & (df['指标']=='开户'),h] =len(hour_charge[(hour_charge['seo变化数据团队']=='tony') & (hour_charge['小时数']>=int(h.split('-')[0]))& (hour_charge['小时数']<int(h.split('-')[1]))])
    df.loc[(df['人员']=='Tony') & (df['指标']=='开户转化率'),h]=round(len(hour_charge[(hour_charge['seo变化数据团队']=='tony') & (hour_charge['小时数']>=int(h.split('-')[0]))& (hour_charge['小时数']<int(h.split('-')[1]))])/df.loc[(df['人员']=='Tony') & (df['指标']=='注册'),h].iloc[0]*100,2)
    df.loc[(df['人员']=='Tony') & (df['指标']=='接收率'),h] =round(df.loc[(df['人员']=='Tony') & (df['指标']=='接收IP数'),h].iloc[0] / df.loc[(df['人员']=='Tony') & (df['指标']=='发送IP数'),h].iloc[0]*100,2)

# 7总计
df.loc[(df['人员']=='Tony') & (df['指标']=='发送IP数'),'总计'] =df.loc[(df['人员']=='Tony') & (df['指标']=='发送IP数'),'0-2':].T.sum()
df.loc[(df['人员']=='Tony') & (df['指标']=='接收IP数'),'总计'] =df.loc[(df['人员']=='Tony') & (df['指标']=='接收IP数'),'0-2':].T.sum()
df.loc[(df['人员']=='Tony') & (df['指标']=='注册'),'总计'] =df.loc[(df['人员']=='Tony') & (df['指标']=='注册'),'0-2':].T.sum()
df.loc[(df['人员']=='Tony') & (df['指标']=='开户'),'总计'] =df.loc[(df['人员']=='Tony') & (df['指标']=='开户'),'0-2':].T.sum()
df.loc[(df['人员']=='Tony') & (df['指标']=='开户转化率'),'总计'] =round(df.loc[(df['人员']=='Tony') & (df['指标']=='开户'),'总计'].iloc[0] / df.loc[(df['人员']=='Tony') & (df['指标']=='注册'),'总计'].iloc[0]*100,2)
df.loc[(df['人员']=='Tony') & (df['指标']=='注册率'),'总计'] =round(df.loc[(df['人员']=='Tony') & (df['指标']=='注册'),'总计'].iloc[0] / df.loc[(df['人员']=='Tony') & (df['指标']=='接收IP数'),'总计'].iloc[0]*100,2)

# 8接收率
df.loc[(df['人员']=='Tony') & (df['指标']=='接收率'),'总计'] =round(df.loc[(df['人员']=='Tony') & (df['指标']=='接收IP数'),'总计'].iloc[0] / df.loc[(df['人员']=='Tony') & (df['指标']=='发送IP数'),'总计'].iloc[0]*100,2)

#-----------------------------------Max----------
for h in hour_list:
    df.loc[(df['人员']=='Max') & (df['指标']=='发送IP数'),h] =data_2[data_2['网站名(domain)'].str.contains('mulu.com')&(data_2['时间']>=int(h.split('-')[0])) & (data_2['时间']<int(h.split('-')[1]))]['IP'].sum()
    df.loc[(df['人员']=='Max') & (df['指标']=='接收IP数'),h] =data_2[data_2['网站名(domain)'].str.contains('max.bty')&(data_2['时间']>=int(h.split('-')[0])) & (data_2['时间']<int(h.split('-')[1]))]['IP'].sum()
    df.loc[(df['人员']=='Max') & (df['指标']=='注册'),h] =len(hour_user[(hour_user['seo变化数据团队']=='max') & (hour_user['小时数']>=int(h.split('-')[0]))& (hour_user['小时数']<int(h.split('-')[1]))])
    df.loc[(df['人员']=='Max') & (df['指标']=='注册率'),h]=round(len(hour_user[(hour_user['seo变化数据团队']=='max') & (hour_user['小时数']>=int(h.split('-')[0]))& (hour_user['小时数']<int(h.split('-')[1]))])/df.loc[(df['人员']=='Max') & (df['指标']=='接收IP数'),h].iloc[0]*100,2)
    df.loc[(df['人员']=='Max') & (df['指标']=='开户'),h] =len(hour_charge[(hour_charge['seo变化数据团队']=='max') & (hour_charge['小时数']>=int(h.split('-')[0]))& (hour_charge['小时数']<int(h.split('-')[1]))])
    df.loc[(df['人员']=='Max') & (df['指标']=='开户转化率'),h]=round(len(hour_charge[(hour_charge['seo变化数据团队']=='max') & (hour_charge['小时数']>=int(h.split('-')[0]))& (hour_charge['小时数']<int(h.split('-')[1]))])/df.loc[(df['人员']=='Max') & (df['指标']=='注册'),h].iloc[0]*100,2)
    df.loc[(df['人员']=='Max') & (df['指标']=='接收率'),h] =round(df.loc[(df['人员']=='Max') & (df['指标']=='接收IP数'),h].iloc[0] / df.loc[(df['人员']=='Max') & (df['指标']=='发送IP数'),h].iloc[0]*100,2)

# 7总计
df.loc[(df['人员']=='Max') & (df['指标']=='发送IP数'),'总计'] =df.loc[(df['人员']=='Max') & (df['指标']=='发送IP数'),'0-2':].T.sum()
df.loc[(df['人员']=='Max') & (df['指标']=='接收IP数'),'总计'] =df.loc[(df['人员']=='Max') & (df['指标']=='接收IP数'),'0-2':].T.sum()
df.loc[(df['人员']=='Max') & (df['指标']=='注册'),'总计'] =df.loc[(df['人员']=='Max') & (df['指标']=='注册'),'0-2':].T.sum()
df.loc[(df['人员']=='Max') & (df['指标']=='开户'),'总计'] =df.loc[(df['人员']=='Max') & (df['指标']=='开户'),'0-2':].T.sum()
df.loc[(df['人员']=='Max') & (df['指标']=='开户转化率'),'总计'] =round(df.loc[(df['人员']=='Max') & (df['指标']=='开户'),'总计'].iloc[0] / df.loc[(df['人员']=='Max') & (df['指标']=='注册'),'总计'].iloc[0]*100,2)
df.loc[(df['人员']=='Max') & (df['指标']=='注册率'),'总计'] =round(df.loc[(df['人员']=='Max') & (df['指标']=='注册'),'总计'].iloc[0] / df.loc[(df['人员']=='Max') & (df['指标']=='接收IP数'),'总计'].iloc[0]*100,2)

# 8接收率
df.loc[(df['人员']=='Max') & (df['指标']=='接收率'),'总计'] =round(df.loc[(df['人员']=='Max') & (df['指标']=='接收IP数'),'总计'].iloc[0] / df.loc[(df['人员']=='Max') & (df['指标']=='发送IP数'),'总计'].iloc[0]*100,2)

#-----------------------------------Zed----------
for h in hour_list:
    df.loc[(df['人员']=='Zed') & (df['指标']=='发送IP数'),h] =data_2[data_2['网站名(domain)'].str.contains('zed.com')&(data_2['时间']>=int(h.split('-')[0])) & (data_2['时间']<int(h.split('-')[1]))]['IP'].sum()
    df.loc[(df['人员']=='Zed') & (df['指标']=='接收IP数'),h] =data_2[data_2['网站名(domain)'].str.contains('zed.bty')&(data_2['时间']>=int(h.split('-')[0])) & (data_2['时间']<int(h.split('-')[1]))]['IP'].sum()
    df.loc[(df['人员']=='Zed') & (df['指标']=='注册'),h] =len(hour_user[(hour_user['seo变化数据团队']=='zed') & (hour_user['小时数']>=int(h.split('-')[0]))& (hour_user['小时数']<int(h.split('-')[1]))])
    df.loc[(df['人员']=='Zed') & (df['指标']=='注册率'),h]=round(len(hour_user[(hour_user['seo变化数据团队']=='zed') & (hour_user['小时数']>=int(h.split('-')[0]))& (hour_user['小时数']<int(h.split('-')[1]))])/df.loc[(df['人员']=='Zed') & (df['指标']=='接收IP数'),h].iloc[0]*100,2)
    df.loc[(df['人员']=='Zed') & (df['指标']=='开户'),h] =len(hour_charge[(hour_charge['seo变化数据团队']=='zed') & (hour_charge['小时数']>=int(h.split('-')[0]))& (hour_charge['小时数']<int(h.split('-')[1]))])
    df.loc[(df['人员']=='Zed') & (df['指标']=='开户转化率'),h]=round(len(hour_charge[(hour_charge['seo变化数据团队']=='zed') & (hour_charge['小时数']>=int(h.split('-')[0]))& (hour_charge['小时数']<int(h.split('-')[1]))])/df.loc[(df['人员']=='Zed') & (df['指标']=='注册'),h].iloc[0]*100,2)
    df.loc[(df['人员']=='Zed') & (df['指标']=='接收率'),h] =round(df.loc[(df['人员']=='Zed') & (df['指标']=='接收IP数'),h].iloc[0] / df.loc[(df['人员']=='Zed') & (df['指标']=='发送IP数'),h].iloc[0]*100,2)

# 7总计
df.loc[(df['人员']=='Zed') & (df['指标']=='发送IP数'),'总计'] =df.loc[(df['人员']=='Zed') & (df['指标']=='发送IP数'),'0-2':].T.sum()
df.loc[(df['人员']=='Zed') & (df['指标']=='接收IP数'),'总计'] =df.loc[(df['人员']=='Zed') & (df['指标']=='接收IP数'),'0-2':].T.sum()
df.loc[(df['人员']=='Zed') & (df['指标']=='注册'),'总计'] =df.loc[(df['人员']=='Zed') & (df['指标']=='注册'),'0-2':].T.sum()
df.loc[(df['人员']=='Zed') & (df['指标']=='开户'),'总计'] =df.loc[(df['人员']=='Zed') & (df['指标']=='开户'),'0-2':].T.sum()
df.loc[(df['人员']=='Zed') & (df['指标']=='开户转化率'),'总计'] =round(df.loc[(df['人员']=='Zed') & (df['指标']=='开户'),'总计'].iloc[0] / df.loc[(df['人员']=='Zed') & (df['指标']=='注册'),'总计'].iloc[0]*100,2)
df.loc[(df['人员']=='Zed') & (df['指标']=='注册率'),'总计'] =round(df.loc[(df['人员']=='Zed') & (df['指标']=='注册'),'总计'].iloc[0] / df.loc[(df['人员']=='Zed') & (df['指标']=='接收IP数'),'总计'].iloc[0]*100,2)

# 8接收率
df.loc[(df['人员']=='Zed') & (df['指标']=='接收率'),'总计'] =round(df.loc[(df['人员']=='Zed') & (df['指标']=='接收IP数'),'总计'].iloc[0] / df.loc[(df['人员']=='Zed') & (df['指标']=='发送IP数'),'总计'].iloc[0]*100,2)

#-----------------------------------Hugo----------
for h in hour_list:
    df.loc[(df['人员']=='Hugo') & (df['指标']=='发送IP数'),h] =data_2[data_2['网站名(domain)'].str.contains('hugo.com')&(data_2['时间']>=int(h.split('-')[0])) & (data_2['时间']<int(h.split('-')[1]))]['IP'].sum()
    df.loc[(df['人员']=='Hugo') & (df['指标']=='接收IP数'),h] =data_2[data_2['网站名(domain)'].str.contains('hugo.bty')&(data_2['时间']>=int(h.split('-')[0])) & (data_2['时间']<int(h.split('-')[1]))]['IP'].sum()
    df.loc[(df['人员']=='Hugo') & (df['指标']=='注册'),h] =len(hour_user[(hour_user['seo变化数据团队']=='hugo') & (hour_user['小时数']>=int(h.split('-')[0]))& (hour_user['小时数']<int(h.split('-')[1]))])
    df.loc[(df['人员']=='Hugo') & (df['指标']=='注册率'),h]=round(len(hour_user[(hour_user['seo变化数据团队']=='hugo') & (hour_user['小时数']>=int(h.split('-')[0]))& (hour_user['小时数']<int(h.split('-')[1]))])/df.loc[(df['人员']=='Hugo') & (df['指标']=='接收IP数'),h].iloc[0]*100,2)
    df.loc[(df['人员']=='Hugo') & (df['指标']=='开户'),h] =len(hour_charge[(hour_charge['seo变化数据团队']=='hugo') & (hour_charge['小时数']>=int(h.split('-')[0]))& (hour_charge['小时数']<int(h.split('-')[1]))])
    df.loc[(df['人员']=='Hugo') & (df['指标']=='开户转化率'),h]=round(len(hour_charge[(hour_charge['seo变化数据团队']=='hugo') & (hour_charge['小时数']>=int(h.split('-')[0]))& (hour_charge['小时数']<int(h.split('-')[1]))])/df.loc[(df['人员']=='Hugo') & (df['指标']=='注册'),h].iloc[0]*100,2)
    df.loc[(df['人员']=='Hugo') & (df['指标']=='接收率'),h] =round(df.loc[(df['人员']=='Hugo') & (df['指标']=='接收IP数'),h].iloc[0] / df.loc[(df['人员']=='Hugo') & (df['指标']=='发送IP数'),h].iloc[0]*100,2)

# 7总计
df.loc[(df['人员']=='Hugo') & (df['指标']=='发送IP数'),'总计'] =df.loc[(df['人员']=='Hugo') & (df['指标']=='发送IP数'),'0-2':].T.sum()
df.loc[(df['人员']=='Hugo') & (df['指标']=='接收IP数'),'总计'] =df.loc[(df['人员']=='Hugo') & (df['指标']=='接收IP数'),'0-2':].T.sum()
df.loc[(df['人员']=='Hugo') & (df['指标']=='注册'),'总计'] =df.loc[(df['人员']=='Hugo') & (df['指标']=='注册'),'0-2':].T.sum()
df.loc[(df['人员']=='Hugo') & (df['指标']=='开户'),'总计'] =df.loc[(df['人员']=='Hugo') & (df['指标']=='开户'),'0-2':].T.sum()
df.loc[(df['人员']=='Hugo') & (df['指标']=='开户转化率'),'总计'] =round(df.loc[(df['人员']=='Hugo') & (df['指标']=='开户'),'总计'].iloc[0] / df.loc[(df['人员']=='Hugo') & (df['指标']=='注册'),'总计'].iloc[0]*100,2)
df.loc[(df['人员']=='Hugo') & (df['指标']=='注册率'),'总计'] =round(df.loc[(df['人员']=='Hugo') & (df['指标']=='注册'),'总计'].iloc[0] / df.loc[(df['人员']=='Hugo') & (df['指标']=='接收IP数'),'总计'].iloc[0]*100,2)

# 8接收率
df.loc[(df['人员']=='Hugo') & (df['指标']=='接收率'),'总计'] =round(df.loc[(df['人员']=='Hugo') & (df['指标']=='接收IP数'),'总计'].iloc[0] / df.loc[(df['人员']=='Hugo') & (df['指标']=='发送IP数'),'总计'].iloc[0]*100,2)


#-----------------------------------Aber----------
for h in hour_list:
    df.loc[(df['人员']=='Aber') & (df['指标']=='发送IP数'),h] =data_2[data_2['网站名(domain)'].str.contains('aber.com')&(data_2['时间']>=int(h.split('-')[0])) & (data_2['时间']<int(h.split('-')[1]))]['IP'].sum()
    df.loc[(df['人员']=='Aber') & (df['指标']=='接收IP数'),h] =data_2[data_2['网站名(domain)'].str.contains('aber.bty')&(data_2['时间']>=int(h.split('-')[0])) & (data_2['时间']<int(h.split('-')[1]))]['IP'].sum()
    df.loc[(df['人员']=='Aber') & (df['指标']=='注册'),h] =len(hour_user[(hour_user['seo变化数据团队']=='aber') & (hour_user['小时数']>=int(h.split('-')[0]))& (hour_user['小时数']<int(h.split('-')[1]))])
    df.loc[(df['人员']=='Aber') & (df['指标']=='注册率'),h]=round(len(hour_user[(hour_user['seo变化数据团队']=='aber') & (hour_user['小时数']>=int(h.split('-')[0]))& (hour_user['小时数']<int(h.split('-')[1]))])/df.loc[(df['人员']=='Aber') & (df['指标']=='接收IP数'),h].iloc[0]*100,2)
    df.loc[(df['人员']=='Aber') & (df['指标']=='开户'),h] =len(hour_charge[(hour_charge['seo变化数据团队']=='aber') & (hour_charge['小时数']>=int(h.split('-')[0]))& (hour_charge['小时数']<int(h.split('-')[1]))])
    df.loc[(df['人员']=='Aber') & (df['指标']=='开户转化率'),h]=round(len(hour_charge[(hour_charge['seo变化数据团队']=='aber') & (hour_charge['小时数']>=int(h.split('-')[0]))& (hour_charge['小时数']<int(h.split('-')[1]))])/df.loc[(df['人员']=='Aber') & (df['指标']=='注册'),h].iloc[0]*100,2)
    df.loc[(df['人员']=='Aber') & (df['指标']=='接收率'),h] =round(df.loc[(df['人员']=='Aber') & (df['指标']=='接收IP数'),h].iloc[0] / df.loc[(df['人员']=='Aber') & (df['指标']=='发送IP数'),h].iloc[0]*100,2)

# 7总计
df.loc[(df['人员']=='Aber') & (df['指标']=='发送IP数'),'总计'] =df.loc[(df['人员']=='Aber') & (df['指标']=='发送IP数'),'0-2':].T.sum()
df.loc[(df['人员']=='Aber') & (df['指标']=='接收IP数'),'总计'] =df.loc[(df['人员']=='Aber') & (df['指标']=='接收IP数'),'0-2':].T.sum()
df.loc[(df['人员']=='Aber') & (df['指标']=='注册'),'总计'] =df.loc[(df['人员']=='Aber') & (df['指标']=='注册'),'0-2':].T.sum()
df.loc[(df['人员']=='Aber') & (df['指标']=='开户'),'总计'] =df.loc[(df['人员']=='Aber') & (df['指标']=='开户'),'0-2':].T.sum()
df.loc[(df['人员']=='Aber') & (df['指标']=='开户转化率'),'总计'] =round(df.loc[(df['人员']=='Aber') & (df['指标']=='开户'),'总计'].iloc[0] / df.loc[(df['人员']=='Aber') & (df['指标']=='注册'),'总计'].iloc[0]*100,2)
df.loc[(df['人员']=='Aber') & (df['指标']=='注册率'),'总计'] =round(df.loc[(df['人员']=='Aber') & (df['指标']=='注册'),'总计'].iloc[0] / df.loc[(df['人员']=='Aber') & (df['指标']=='接收IP数'),'总计'].iloc[0]*100,2)

# 8接收率
df.loc[(df['人员']=='Aber') & (df['指标']=='接收率'),'总计'] =round(df.loc[(df['人员']=='Aber') & (df['指标']=='接收IP数'),'总计'].iloc[0] / df.loc[(df['人员']=='Aber') & (df['指标']=='发送IP数'),'总计'].iloc[0]*100,2)


#-----------------------------------DK----------
for h in hour_list:
    df.loc[(df['人员']=='DK') & (df['指标']=='发送IP数'),h] =data_2[data_2['网站名(domain)'].str.contains('dk.com')&(data_2['时间']>=int(h.split('-')[0])) & (data_2['时间']<int(h.split('-')[1]))]['IP'].sum() // 2
    df.loc[(df['人员']=='DK') & (df['指标']=='接收IP数'),h] =data_2[data_2['网站名(domain)'].str.contains('dk.bty')&(data_2['时间']>=int(h.split('-')[0])) & (data_2['时间']<int(h.split('-')[1]))]['IP'].sum()
    df.loc[(df['人员']=='DK') & (df['指标']=='注册'),h] =len(hour_user[(hour_user['seo变化数据团队']=='dk') & (hour_user['小时数']>=int(h.split('-')[0]))& (hour_user['小时数']<int(h.split('-')[1]))])
    df.loc[(df['人员']=='DK') & (df['指标']=='注册率'),h]=round(len(hour_user[(hour_user['seo变化数据团队']=='dk') & (hour_user['小时数']>=int(h.split('-')[0]))& (hour_user['小时数']<int(h.split('-')[1]))])/df.loc[(df['人员']=='DK') & (df['指标']=='接收IP数'),h].iloc[0]*100,2)
    df.loc[(df['人员']=='DK') & (df['指标']=='开户'),h] =len(hour_charge[(hour_charge['seo变化数据团队']=='dk') & (hour_charge['小时数']>=int(h.split('-')[0]))& (hour_charge['小时数']<int(h.split('-')[1]))])
    df.loc[(df['人员']=='DK') & (df['指标']=='开户转化率'),h]=round(len(hour_charge[(hour_charge['seo变化数据团队']=='dk') & (hour_charge['小时数']>=int(h.split('-')[0]))& (hour_charge['小时数']<int(h.split('-')[1]))])/df.loc[(df['人员']=='DK') & (df['指标']=='注册'),h].iloc[0]*100,2)
    df.loc[(df['人员']=='DK') & (df['指标']=='接收率'),h] =round(df.loc[(df['人员']=='DK') & (df['指标']=='接收IP数'),h].iloc[0] / df.loc[(df['人员']=='DK') & (df['指标']=='发送IP数'),h].iloc[0]*100,2)

# 7总计
df.loc[(df['人员']=='DK') & (df['指标']=='发送IP数'),'总计'] =df.loc[(df['人员']=='DK') & (df['指标']=='发送IP数'),'0-2':].T.sum()
df.loc[(df['人员']=='DK') & (df['指标']=='接收IP数'),'总计'] =df.loc[(df['人员']=='DK') & (df['指标']=='接收IP数'),'0-2':].T.sum()
df.loc[(df['人员']=='DK') & (df['指标']=='注册'),'总计'] =df.loc[(df['人员']=='DK') & (df['指标']=='注册'),'0-2':].T.sum()
df.loc[(df['人员']=='DK') & (df['指标']=='开户'),'总计'] =df.loc[(df['人员']=='DK') & (df['指标']=='开户'),'0-2':].T.sum()
df.loc[(df['人员']=='DK') & (df['指标']=='开户转化率'),'总计'] =round(df.loc[(df['人员']=='DK') & (df['指标']=='开户'),'总计'].iloc[0] / df.loc[(df['人员']=='DK') & (df['指标']=='注册'),'总计'].iloc[0]*100,2)
df.loc[(df['人员']=='DK') & (df['指标']=='注册率'),'总计'] =round(df.loc[(df['人员']=='DK') & (df['指标']=='注册'),'总计'].iloc[0] / df.loc[(df['人员']=='DK') & (df['指标']=='接收IP数'),'总计'].iloc[0]*100,2)

# 8接收率
df.loc[(df['人员']=='DK') & (df['指标']=='接收率'),'总计'] =round(df.loc[(df['人员']=='DK') & (df['指标']=='接收IP数'),'总计'].iloc[0] / df.loc[(df['人员']=='DK') & (df['指标']=='发送IP数'),'总计'].iloc[0]*100,2)

#-----------------------------------Ben----------
for h in hour_list:
    df.loc[(df['人员']=='Ben') & (df['指标']=='发送IP数'),h] =data_2[data_2['网站名(domain)'].str.contains('ben.com')&(data_2['时间']>=int(h.split('-')[0])) & (data_2['时间']<int(h.split('-')[1]))]['IP'].sum() // 2
    df.loc[(df['人员']=='Ben') & (df['指标']=='接收IP数'),h] =data_2[data_2['网站名(domain)'].str.contains('ben.bty')&(data_2['时间']>=int(h.split('-')[0])) & (data_2['时间']<int(h.split('-')[1]))]['IP'].sum()
    df.loc[(df['人员']=='Ben') & (df['指标']=='注册'),h] =len(hour_user[(hour_user['seo变化数据团队']=='ben') & (hour_user['小时数']>=int(h.split('-')[0]))& (hour_user['小时数']<int(h.split('-')[1]))])
    df.loc[(df['人员']=='Ben') & (df['指标']=='注册率'),h]=round(len(hour_user[(hour_user['seo变化数据团队']=='ben') & (hour_user['小时数']>=int(h.split('-')[0]))& (hour_user['小时数']<int(h.split('-')[1]))])/df.loc[(df['人员']=='Ben') & (df['指标']=='接收IP数'),h].iloc[0]*100,2)
    df.loc[(df['人员']=='Ben') & (df['指标']=='开户'),h] =len(hour_charge[(hour_charge['seo变化数据团队']=='ben') & (hour_charge['小时数']>=int(h.split('-')[0]))& (hour_charge['小时数']<int(h.split('-')[1]))])
    df.loc[(df['人员']=='Ben') & (df['指标']=='开户转化率'),h]=round(len(hour_charge[(hour_charge['seo变化数据团队']=='ben') & (hour_charge['小时数']>=int(h.split('-')[0]))& (hour_charge['小时数']<int(h.split('-')[1]))])/df.loc[(df['人员']=='Ben') & (df['指标']=='注册'),h].iloc[0]*100,2)
    df.loc[(df['人员']=='Ben') & (df['指标']=='接收率'),h] =round(df.loc[(df['人员']=='Ben') & (df['指标']=='接收IP数'),h].iloc[0] / df.loc[(df['人员']=='Ben') & (df['指标']=='发送IP数'),h].iloc[0]*100,2)

# 7总计
df.loc[(df['人员']=='Ben') & (df['指标']=='发送IP数'),'总计'] =df.loc[(df['人员']=='Ben') & (df['指标']=='发送IP数'),'0-2':].T.sum()
df.loc[(df['人员']=='Ben') & (df['指标']=='接收IP数'),'总计'] =df.loc[(df['人员']=='Ben') & (df['指标']=='接收IP数'),'0-2':].T.sum()
df.loc[(df['人员']=='Ben') & (df['指标']=='注册'),'总计'] =df.loc[(df['人员']=='Ben') & (df['指标']=='注册'),'0-2':].T.sum()
df.loc[(df['人员']=='Ben') & (df['指标']=='开户'),'总计'] =df.loc[(df['人员']=='Ben') & (df['指标']=='开户'),'0-2':].T.sum()
df.loc[(df['人员']=='Ben') & (df['指标']=='开户转化率'),'总计'] =round(df.loc[(df['人员']=='Ben') & (df['指标']=='开户'),'总计'].iloc[0] / df.loc[(df['人员']=='Ben') & (df['指标']=='注册'),'总计'].iloc[0]*100,2)
df.loc[(df['人员']=='Ben') & (df['指标']=='注册率'),'总计'] =round(df.loc[(df['人员']=='Ben') & (df['指标']=='注册'),'总计'].iloc[0] / df.loc[(df['人员']=='Ben') & (df['指标']=='接收IP数'),'总计'].iloc[0]*100,2)

# 8接收率
df.loc[(df['人员']=='Ben') & (df['指标']=='接收率'),'总计'] =round(df.loc[(df['人员']=='Ben') & (df['指标']=='接收IP数'),'总计'].iloc[0] / df.loc[(df['人员']=='Ben') & (df['指标']=='发送IP数'),'总计'].iloc[0]*100,2)

print(df)
df.to_csv(r'C:\Users\User\Desktop\SEO\ip历史数据_2.csv',mode='a',index=False,header=True,encoding='gbk')