import pandas as pd
import numpy as np
import datetime
import xlwings as xw
pd.set_option('display.max_colwidth', None) #显示单元格完整信息
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

day = 0
user = pd.read_csv(r'C:\Users\User\Desktop\SEO\_0815\会员列表导出.csv',encoding='gbk')
firChargeUser = pd.read_csv(r'C:\Users\User\Desktop\SEO\_0815\会员首存报表.csv',encoding='gbk')
data = pd.read_excel(r'C:\Users\User\Desktop\SEO\_0815\今日数据.xlsx')
data_2 = pd.read_excel(r'C:\Users\User\Desktop\SEO\_0815\今日数据.xlsx','趋势分析')
daili = pd.read_excel(r'C:\Users\User\Desktop\SEO\_0807\SEO每日模板-每日更新.xlsx','代理总表')

his_data  = pd.read_csv(r'C:\Users\User\Desktop\SEO\SEO每日更新_814.csv',encoding='gbk')
dic ={'日期':(datetime.datetime.now()+datetime.timedelta(days=day)).strftime('%Y/%m/%d'),
      '人员':[i for i in ['Paddy', 'Tony', 'Max', 'Martin', 'Zed', 'Hugo', 'Aber', 'DK', 'Ben'] for j in range(7)],'指标':['接收率','发送IP数','接收IP数','注册','注册率','开户','开户转化率']*9, '总计':0, '0-2':0, '2-4':0, '4-6':0, '6-8':0, '8-10':0, '10-12':0, '12-14':0, '14-16':0, '16-18':0, '18-20':0, '20-22':0, '22-24':0}
df = pd.DataFrame(dic)
shuju = pd.DataFrame({'人员':['Paddy', 'Tony', 'Max', 'Martin', 'Zed', 'Hugo', 'Aber', 'DK', 'Ben','当日汇总'],
                      '日期':(datetime.datetime.now()+datetime.timedelta(days=day)).strftime('%Y/%m/%d'),
                      '发送IP':0,
                      '接受IP':0,
                      '对比昨天(总IP)':0,
                      '对比前3天均值(总IP)':0,
                      '对比前5天均值(总IP)':0,
                      '对比前7天均值(总IP)':0,
                      '对比昨天(总注册)':0,
                      '对比前3天均值(总注册)':0,
                      '对比前5天均值(总注册)':0,
                      '对比前7天均值(总注册)':0,
                      '对比昨天(总开户)':0,
                      '对比前3天均值(总开户)':0,
                      '对比前5天均值(总开户)':0,
                      '对比前7天均值(总开户)':0})


shuju.set_index('人员',inplace = True)

data['IP']=pd.to_numeric(data['IP'],errors='coerce').replace(np.nan,0).astype('int64')
grp=data.groupby('网站名(domain)').agg({'IP':sum})

shuju.loc['Paddy','发送IP']=grp.loc['paddy.com','IP']
shuju.loc['Paddy','接受IP']=grp.loc['paddy.bty','IP']
shuju.loc['Tony','发送IP']=grp.loc['tonyb.com','IP']/2
shuju.loc['Tony','接受IP']=grp.loc['tony.bty','IP']
shuju.loc['Max','发送IP']=grp.loc['mulu.com','IP']
shuju.loc['Max','接受IP']=grp.loc['max.bty','IP']
shuju.loc['Martin','发送IP']=grp.loc['redquan.com','IP']
try:
    shuju.loc['Martin','接受IP']=grp.loc['martin.bty','IP']
except:
    shuju.loc['Martin','接受IP']=0
shuju.loc['Zed','发送IP']=grp.loc['zed.com','IP']
shuju.loc['Zed','接受IP']=grp.loc['zed.bty','IP']
shuju.loc['Hugo','发送IP']=grp.loc['hugo.com','IP']
try:
    shuju.loc['Hugo','接受IP']=grp.loc['hugo.bty','IP']
except:
    shuju.loc['Hugo','接受IP']=0

shuju.loc['Aber','发送IP']=grp.loc['aber.com','IP']/2
shuju.loc['Aber','接受IP']=grp.loc['aber.bty','IP']
shuju.loc['DK','发送IP']=grp.loc['dk.com','IP']/2
shuju.loc['DK','接受IP']=grp.loc['dk.bty','IP']
shuju.loc['Ben','发送IP']=grp.loc['ben.com','IP']/2
shuju.loc['Ben','接受IP']=grp.loc['ben.bty','IP']
shuju.loc['当日汇总','发送IP']=shuju['发送IP'].sum()
shuju.loc['当日汇总','接受IP']=shuju['接受IP'].sum()

shuju['日期'] = pd.to_datetime(shuju['日期'])
shuju.insert(1,'人员2',shuju.index)
shuju['人员2']=shuju['人员2'].str.lower()

# 第1次merge前，重置索引
shuju.reset_index(inplace=True)

merge_user = pd.merge(user,daili,how = 'left',left_on='代理',right_on='代理线')
grpSEO = merge_user.groupby('seo变化数据团队').agg({'seo变化数据团队':len})
grpSEO.rename(columns={'seo变化数据团队':'注册'},inplace=True)
grpSEO.reset_index(inplace=True)
grpSEO['人员2'] = grpSEO['seo变化数据团队'].str.lower()
grpSEO.set_index('seo变化数据团队',inplace=True)

shuju=shuju.merge(grpSEO,on='人员2',how='left')

shuju['注册率(%)'] = round(shuju['注册']/shuju['发送IP']*100,2)

merge_charge = pd.merge(firChargeUser,daili,how='left',left_on='所属代理',right_on='代理线')
grpCHARGE = merge_charge.groupby('seo变化数据团队').agg({'seo变化数据团队':len})
grpCHARGE= grpCHARGE.rename(columns={'seo变化数据团队':'开户'})
grpCHARGE.reset_index(inplace=True)
grpCHARGE['seo变化数据团队']=grpCHARGE['seo变化数据团队'].str.lower()
grpCHARGE= grpCHARGE.rename(columns={'seo变化数据团队':'人员2'})
# 第2次merge
shuju = pd.merge(shuju,grpCHARGE,how='left',on='人员2')
shuju['转化率(%)'] = round(shuju['开户']/shuju['注册']*100,2)

grp3  = merge_charge[merge_charge['注册时间'].str[:9]==merge_charge['交易时间'].str[:9]].groupby('seo变化数据团队').agg({'seo变化数据团队':len})
grp3.rename(columns = {'seo变化数据团队':'当日注册并开户'},inplace=True)
grp3.reset_index(inplace=True)
grp3['seo变化数据团队'] =grp3['seo变化数据团队'].str.lower()
grp3.rename(columns = {'seo变化数据团队':'人员2'},inplace=True)
# 第3次merge
shuju  = pd.merge(shuju,grp3,how='left',on='人员2')
shuju['当日注册激活率(%)'] = round(shuju['当日注册并开户']/shuju['注册']*100,2)

#------------
# his_data  = pd.read_csv(r'C:\Users\User\Desktop\SEO\SEO每日更新_814.csv',encoding='gbk')
his_data['日期']= pd.to_datetime(his_data['日期'])
be_data = his_data[his_data['日期']==(shuju['日期'][0]+datetime.timedelta(days=-2))][:-1]

# shuju.sort_index(inplace=True)
shuju.set_index('人员',inplace = True)
shuju.sort_index(inplace=True)
be_data.set_index('人员',inplace=True)
be_data.sort_index(inplace=True)

be3_data = his_data[his_data['日期']>(shuju['日期'][0]+datetime.timedelta(days=-3))]
be3_data = be3_data.groupby('人员').mean()[:-1]
be5_data = his_data[his_data['日期']>(shuju['日期'][0]+datetime.timedelta(days=-5))]
be5_data = be5_data.groupby('人员').mean()[:-1]
be7_data = his_data[his_data['日期']>(shuju['日期'][0]+datetime.timedelta(days=-7))]
be7_data = be7_data.groupby('人员').mean()[:-1]

shuju['对比昨天(总IP)']=shuju['发送IP']-be_data['总IP']
shuju['对比前3天均值(总IP)']= shuju['发送IP']-be3_data['总IP']
shuju['对比前5天均值(总IP)']= shuju['发送IP']-be5_data['总IP']
shuju['对比前7天均值(总IP)']= shuju['发送IP']-be7_data['总IP']

shuju['对比昨天(总注册)']=shuju['发送IP']-be_data['总IP']
shuju['对比前3天均值(总注册)']= shuju['注册']-be3_data['注册']
shuju['对比前5天均值(总注册)']= shuju['注册']-be5_data['注册']
shuju['对比前7天均值(总注册)']= shuju['注册']-be7_data['注册']

shuju['对比昨天(总开户)']=shuju['发送IP']-be_data['总IP']
shuju['对比前3天均值(总开户)']= shuju['开户']-be3_data['开户']
shuju['对比前5天均值(总开户)']= shuju['开户']-be5_data['开户']
shuju['对比前7天均值(总开户)']= shuju['开户']-be7_data['开户']

shuju = shuju.iloc[:,:4].join(shuju.iloc[:,-6:]).join(shuju.iloc[:,4:-6])
shuju.fillna(0,inplace=True)

shuju['对比昨天(总IP)'] =shuju['对比昨天(总IP)'].astype('int64')
shuju['对比前3天均值(总IP)'] = shuju['对比前3天均值(总IP)'].astype('int64')
shuju['对比前5天均值(总IP)'] = shuju['对比前5天均值(总IP)'].astype('int64')
shuju['对比前7天均值(总IP)'] = shuju['对比前7天均值(总IP)'].astype('int64')

shuju['对比昨天(总注册)'] =shuju['对比昨天(总注册)'].astype('int64')
shuju['对比前3天均值(总注册)'] = shuju['对比前3天均值(总注册)'].astype('int64')
shuju['对比前5天均值(总注册)'] = shuju['对比前5天均值(总注册)'].astype('int64')
shuju['对比前7天均值(总注册)'] = shuju['对比前7天均值(总注册)'].astype('int64')

shuju['对比昨天(总开户)'] =shuju['对比昨天(总开户)'].astype('int64')
shuju['对比前3天均值(总开户)'] = shuju['对比前3天均值(总开户)'].astype('int64')
shuju['对比前5天均值(总开户)'] = shuju['对比前5天均值(总开户)'].astype('int64')
shuju['对比前7天均值(总开户)'] = shuju['对比前7天均值(总开户)'].astype('int64')
shuju['注册'] = shuju['注册'].astype('int64')
shuju['开户'] = shuju['开户'].astype('int64')
shuju['当日注册并开户'] = shuju['当日注册并开户'].astype('int64')

for i in shuju.iloc[:,4:].columns:
    shuju.loc['当日汇总',i]=sum(shuju[i])

shuju.insert(1,'人员',shuju.index)
shuju.drop('人员2',inplace=True,axis=1)

## ---------------历史数据---------------------------------------------------------------------------------------------------------

user['注册时间']=pd.to_datetime(user['注册时间'])
hour_user= pd.merge(user,daili,how = 'left',left_on='代理',right_on='代理线')
hour_user['小时数']= hour_user['注册时间'].dt.hour
firChargeUser['注册时间']=pd.to_datetime(firChargeUser['注册时间'])
hour_charge = pd.merge(firChargeUser,daili,how='left',left_on='所属代理',right_on='代理线')
hour_charge['小时数']= hour_charge['注册时间'].dt.hour
# dic ={'日期':(datetime.datetime.now()+datetime.timedelta(days=0)).strftime('%Y/%m/%d'),
#       '人员':[i for i in ['Paddy', 'Tony', 'Max', 'Martin', 'Zed', 'Hugo', 'Aber', 'DK', 'Ben'] for j in range(7)],'指标':['接收率','发送IP数','接收IP数','注册','注册率','开户','开户转化率']*9, '总计':0, '0-2':0, '2-4':0, '4-6':0, '6-8':0, '8-10':0, '10-12':0, '12-14':0, '14-16':0, '16-18':0, '18-20':0, '20-22':0, '22-24':0}
# df = pd.DataFrame(dic)

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


print(shuju)
# 更新每日数据
shuju.to_csv(r'C:\Users\User\Desktop\SEO\SEO每日更新_814.csv',mode='a',index=False,header=False,encoding='gbk')
# 更新ip历史数据
df.to_csv(r'C:\Users\User\Desktop\SEO\ip历史数据_2.csv',mode='a',index=False,header=False,encoding='gbk')
