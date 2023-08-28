import pandas as pd
import numpy as np
import datetime
# pd.set_option('display.max_colwidth', None) #显示单元格完整信息
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

user = pd.read_csv(r'C:\Users\User\Desktop\SEO_0807\会员列表导出.csv',encoding='gbk')
firChargeUser = pd.read_csv(r'C:\Users\User\Desktop\SEO_0807\会员首存报表.csv',encoding='gbk')
data = pd.read_excel(r'C:\Users\User\Desktop\SEO_0807\data\今日数据.xlsx')
data_2 = pd.read_excel(r'C:\Users\User\Desktop\SEO_0807\data\今日数据.xlsx','趋势分析')
daili = pd.read_excel(r'C:\Users\User\Desktop\SEO_0807\SEO每日模板-每日更新.xlsx','代理总表')

user['注册时间']=pd.to_datetime(user['注册时间'])
hour_user= pd.merge(user,daili,how = 'left',left_on='代理',right_on='代理线')
hour_user['小时数']= hour_user['注册时间'].dt.hour
firChargeUser['注册时间']=pd.to_datetime(firChargeUser['注册时间'])
hour_charge = pd.merge(firChargeUser,daili,how='left',left_on='所属代理',right_on='代理线')
hour_charge['小时数']= hour_charge['注册时间'].dt.hour
dic ={'日期':(datetime.datetime.now()+datetime.timedelta(days=-4)).strftime('%Y/%m/%d'),
      '人员':[i for i in ['Paddy', 'Tony', 'Max', 'Martin', 'Zed', 'Hugo', 'Aber', 'DK', 'Ben'] for j in range(7)],'指标':['接收率','发送IP数','接收IP数','注册','注册率','开户','开户转化率']*9, '总计':0, '0-2':0, '2-4':0, '4-6':0, '6-8':0, '8-10':0, '10-12':0, '12-14':0, '14-16':0, '16-18':0, '18-20':0, '20-22':0, '22-24':0}
df = pd.DataFrame(dic)

data_2['PV'] = pd.to_numeric(data_2['PV'],errors='coerce',downcast='integer')
data_2['UV'] = pd.to_numeric(data_2['UV'],errors='coerce',downcast='integer')
data_2['IP'] = pd.to_numeric(data_2['IP'],errors='coerce',downcast='integer')

# 1发送IP数
df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'0-2'] =data_2[data_2['网站名(domain)'].str.contains('redquan.com') & (data_2['时间']<2)]['IP'].sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'2-4'] =data_2[data_2['网站名(domain)'].str.contains('redquan.com') &(data_2['时间']>=2) &(data_2['时间']<4)]['IP'].sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'4-6'] =data_2[data_2['网站名(domain)'].str.contains('redquan.com') &(data_2['时间']>=4)& (data_2['时间']<6)]['IP'].sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'6-8'] =data_2[data_2['网站名(domain)'].str.contains('redquan.com') &(data_2['时间']>=6)& (data_2['时间']<8)]['IP'].sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'8-10'] =data_2[data_2['网站名(domain)'].str.contains('redquan.com') &(data_2['时间']>=8)& (data_2['时间']<10)]['IP'].sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'10-12'] =data_2[data_2['网站名(domain)'].str.contains('redquan.com') &(data_2['时间']>=10)& (data_2['时间']<12)]['IP'].sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'12-14'] =data_2[data_2['网站名(domain)'].str.contains('redquan.com') &(data_2['时间']>=12)& (data_2['时间']<14)]['IP'].sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'14-16'] =data_2[data_2['网站名(domain)'].str.contains('redquan.com') &(data_2['时间']>=14)& (data_2['时间']<16)]['IP'].sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'16-18'] =data_2[data_2['网站名(domain)'].str.contains('redquan.com') &(data_2['时间']>=16)& (data_2['时间']<18)]['IP'].sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'18-20'] =data_2[data_2['网站名(domain)'].str.contains('redquan.com') &(data_2['时间']>=18)& (data_2['时间']<20)]['IP'].sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'20-22'] =data_2[data_2['网站名(domain)'].str.contains('redquan.com') &(data_2['时间']>=20)& (data_2['时间']<22)]['IP'].sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'22-24'] =data_2[data_2['网站名(domain)'].str.contains('redquan.com')&(data_2['时间']>=22) & (data_2['时间']<24)]['IP'].sum()

# 2接收IP数
df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'0-2'] =data_2[data_2['网站名(domain)'].str.contains('martin.bty') & (data_2['时间']<2)]['IP'].sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'2-4'] =data_2[data_2['网站名(domain)'].str.contains('martin.bty') &(data_2['时间']>=2) &(data_2['时间']<4)]['IP'].sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'4-6'] =data_2[data_2['网站名(domain)'].str.contains('martin.bty') &(data_2['时间']>=4)& (data_2['时间']<6)]['IP'].sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'6-8'] =data_2[data_2['网站名(domain)'].str.contains('martin.bty') &(data_2['时间']>=6)& (data_2['时间']<8)]['IP'].sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'8-10'] =data_2[data_2['网站名(domain)'].str.contains('martin.bty') &(data_2['时间']>=8)& (data_2['时间']<10)]['IP'].sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'10-12'] =data_2[data_2['网站名(domain)'].str.contains('martin.bty') &(data_2['时间']>=10)& (data_2['时间']<12)]['IP'].sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'12-14'] =data_2[data_2['网站名(domain)'].str.contains('martin.bty') &(data_2['时间']>=12)& (data_2['时间']<14)]['IP'].sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'14-16'] =data_2[data_2['网站名(domain)'].str.contains('martin.bty') &(data_2['时间']>=14)& (data_2['时间']<16)]['IP'].sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'16-18'] =data_2[data_2['网站名(domain)'].str.contains('martin.bty') &(data_2['时间']>=16)& (data_2['时间']<18)]['IP'].sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'18-20'] =data_2[data_2['网站名(domain)'].str.contains('martin.bty') &(data_2['时间']>=18)& (data_2['时间']<20)]['IP'].sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'20-22'] =data_2[data_2['网站名(domain)'].str.contains('martin.bty') &(data_2['时间']>=20)& (data_2['时间']<22)]['IP'].sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'22-24'] =data_2[data_2['网站名(domain)'].str.contains('martin.bty')&(data_2['时间']>=20) & (data_2['时间']<24)]['IP'].sum()

# 3注册
df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'0-2'] =len(hour_user[(hour_user['seo变化数据团队']=='martin') & (hour_user['小时数']<2)])
df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'2-4'] =len(hour_user[(hour_user['seo变化数据团队']=='martin') & (hour_user['小时数']>=2)& (hour_user['小时数']<4)])
df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'4-6'] =len(hour_user[(hour_user['seo变化数据团队']=='martin') & (hour_user['小时数']>=4)& (hour_user['小时数']<6)])
df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'6-8'] =len(hour_user[(hour_user['seo变化数据团队']=='martin') & (hour_user['小时数']>=6)& (hour_user['小时数']<8)])
df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'8-10'] =len(hour_user[(hour_user['seo变化数据团队']=='martin') & (hour_user['小时数']>=8)& (hour_user['小时数']<10)])
df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'10-12'] =len(hour_user[(hour_user['seo变化数据团队']=='martin') & (hour_user['小时数']>=10)& (hour_user['小时数']<12)])
df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'12-14'] =len(hour_user[(hour_user['seo变化数据团队']=='martin') & (hour_user['小时数']>=12)& (hour_user['小时数']<14)])
df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'14-16'] =len(hour_user[(hour_user['seo变化数据团队']=='martin') & (hour_user['小时数']>=14)& (hour_user['小时数']<16)])
df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'16-18'] =len(hour_user[(hour_user['seo变化数据团队']=='martin') & (hour_user['小时数']>=16)& (hour_user['小时数']<18)])
df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'18-20'] =len(hour_user[(hour_user['seo变化数据团队']=='martin') & (hour_user['小时数']>=18)& (hour_user['小时数']<20)])
df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'20-22'] =len(hour_user[(hour_user['seo变化数据团队']=='martin') & (hour_user['小时数']>=20)& (hour_user['小时数']<22)])
df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'22-24'] =len(hour_user[(hour_user['seo变化数据团队']=='martin') & (hour_user['小时数']>=22)& (hour_user['小时数']<24)])

# 4注册率
df.loc[(df['人员']=='Martin') & (df['指标']=='注册率'),'0-2'] =round(len(hour_user[(hour_user['seo变化数据团队']=='martin') & (hour_user['小时数']<2)])/df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'0-2'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='注册率'),'2-4'] =round(len(hour_user[(hour_user['seo变化数据团队']=='martin') & (hour_user['小时数']>=2)& (hour_user['小时数']<4)])/df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'2-4'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='注册率'),'4-6'] =round(len(hour_user[(hour_user['seo变化数据团队']=='martin') & (hour_user['小时数']>=4)& (hour_user['小时数']<6)])/df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'4-6'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='注册率'),'6-8'] =round(len(hour_user[(hour_user['seo变化数据团队']=='martin') & (hour_user['小时数']>=6)& (hour_user['小时数']<8)])/df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'6-8'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='注册率'),'8-10'] =round(len(hour_user[(hour_user['seo变化数据团队']=='martin') & (hour_user['小时数']>=8)& (hour_user['小时数']<10)])/df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'8-10'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='注册率'),'10-12']=round(len(hour_user[(hour_user['seo变化数据团队']=='martin') & (hour_user['小时数']>=10)& (hour_user['小时数']<12)])/df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'10-12'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='注册率'),'12-14']=round(len(hour_user[(hour_user['seo变化数据团队']=='martin') & (hour_user['小时数']>=12)& (hour_user['小时数']<14)])/df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'12-14'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='注册率'),'14-16']=round(len(hour_user[(hour_user['seo变化数据团队']=='martin') & (hour_user['小时数']>=14)& (hour_user['小时数']<16)])/df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'14-16'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='注册率'),'16-18']=round(len(hour_user[(hour_user['seo变化数据团队']=='martin') & (hour_user['小时数']>=16)& (hour_user['小时数']<18)])/df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'16-18'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='注册率'),'18-20']=round(len(hour_user[(hour_user['seo变化数据团队']=='martin') & (hour_user['小时数']>=18)& (hour_user['小时数']<20)])/df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'18-20'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='注册率'),'20-22']=round(len(hour_user[(hour_user['seo变化数据团队']=='martin') & (hour_user['小时数']>=20)& (hour_user['小时数']<22)])/df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'20-22'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='注册率'),'22-24']=round(len(hour_user[(hour_user['seo变化数据团队']=='martin') & (hour_user['小时数']>=22)& (hour_user['小时数']<24)])/df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'22-24'].iloc[0]*100,2)

# 5开户
df.loc[(df['人员']=='Martin') & (df['指标']=='开户'),'0-2'] =len(hour_charge[(hour_charge['seo变化数据团队']=='martin') & (hour_charge['小时数']<2)])
df.loc[(df['人员']=='Martin') & (df['指标']=='开户'),'2-4'] =len(hour_charge[(hour_charge['seo变化数据团队']=='martin') & (hour_charge['小时数']>=2)& (hour_charge['小时数']<4)])
df.loc[(df['人员']=='Martin') & (df['指标']=='开户'),'4-6'] =len(hour_charge[(hour_charge['seo变化数据团队']=='martin') & (hour_charge['小时数']>=4)& (hour_charge['小时数']<6)])
df.loc[(df['人员']=='Martin') & (df['指标']=='开户'),'6-8'] =len(hour_charge[(hour_charge['seo变化数据团队']=='martin') & (hour_charge['小时数']>=6)& (hour_charge['小时数']<8)])
df.loc[(df['人员']=='Martin') & (df['指标']=='开户'),'8-10'] =len(hour_charge[(hour_charge['seo变化数据团队']=='martin') & (hour_charge['小时数']>=8)& (hour_charge['小时数']<10)])
df.loc[(df['人员']=='Martin') & (df['指标']=='开户'),'10-12'] =len(hour_charge[(hour_charge['seo变化数据团队']=='martin') & (hour_charge['小时数']>=10)& (hour_charge['小时数']<12)])
df.loc[(df['人员']=='Martin') & (df['指标']=='开户'),'12-14'] =len(hour_charge[(hour_charge['seo变化数据团队']=='martin') & (hour_charge['小时数']>=12)& (hour_charge['小时数']<14)])
df.loc[(df['人员']=='Martin') & (df['指标']=='开户'),'14-16'] =len(hour_charge[(hour_charge['seo变化数据团队']=='martin') & (hour_charge['小时数']>=14)& (hour_charge['小时数']<16)])
df.loc[(df['人员']=='Martin') & (df['指标']=='开户'),'16-18'] =len(hour_charge[(hour_charge['seo变化数据团队']=='martin') & (hour_charge['小时数']>=16)& (hour_charge['小时数']<18)])
df.loc[(df['人员']=='Martin') & (df['指标']=='开户'),'18-20'] =len(hour_charge[(hour_charge['seo变化数据团队']=='martin') & (hour_charge['小时数']>=18)& (hour_charge['小时数']<20)])
df.loc[(df['人员']=='Martin') & (df['指标']=='开户'),'20-22'] =len(hour_charge[(hour_charge['seo变化数据团队']=='martin') & (hour_charge['小时数']>=20)& (hour_charge['小时数']<22)])
df.loc[(df['人员']=='Martin') & (df['指标']=='开户'),'22-24'] =len(hour_charge[(hour_charge['seo变化数据团队']=='martin') & (hour_charge['小时数']>=22)& (hour_charge['小时数']<24)])

# 6开户转化率
df.loc[(df['人员']=='Martin') & (df['指标']=='开户转化率'),'0-2'] =round(len(hour_charge[(hour_charge['seo变化数据团队']=='martin') & (hour_charge['小时数']<2)])/df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'0-2'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='开户转化率'),'2-4'] =round(len(hour_charge[(hour_charge['seo变化数据团队']=='martin') & (hour_charge['小时数']>=2)& (hour_charge['小时数']<4)])/df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'2-4'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='开户转化率'),'4-6'] =round(len(hour_charge[(hour_charge['seo变化数据团队']=='martin') & (hour_charge['小时数']>=4)& (hour_charge['小时数']<6)])/df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'4-6'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='开户转化率'),'6-8'] =round(len(hour_charge[(hour_charge['seo变化数据团队']=='martin') & (hour_charge['小时数']>=6)& (hour_charge['小时数']<8)])/df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'6-8'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='开户转化率'),'8-10'] =round(len(hour_charge[(hour_charge['seo变化数据团队']=='martin') & (hour_charge['小时数']>=8)& (hour_charge['小时数']<10)])/df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'8-10'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='开户转化率'),'10-12']=round(len(hour_charge[(hour_charge['seo变化数据团队']=='martin') & (hour_charge['小时数']>=10)& (hour_charge['小时数']<12)])/df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'10-12'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='开户转化率'),'12-14']=round(len(hour_charge[(hour_charge['seo变化数据团队']=='martin') & (hour_charge['小时数']>=12)& (hour_charge['小时数']<14)])/df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'12-14'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='开户转化率'),'14-16']=round(len(hour_charge[(hour_charge['seo变化数据团队']=='martin') & (hour_charge['小时数']>=14)& (hour_charge['小时数']<16)])/df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'14-16'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='开户转化率'),'16-18']=round(len(hour_charge[(hour_charge['seo变化数据团队']=='martin') & (hour_charge['小时数']>=16)& (hour_charge['小时数']<18)])/df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'16-18'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='开户转化率'),'18-20']=round(len(hour_charge[(hour_charge['seo变化数据团队']=='martin') & (hour_charge['小时数']>=18)& (hour_charge['小时数']<20)])/df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'18-20'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='开户转化率'),'20-22']=round(len(hour_charge[(hour_charge['seo变化数据团队']=='martin') & (hour_charge['小时数']>=20)& (hour_charge['小时数']<22)])/df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'20-22'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='开户转化率'),'22-24']=round(len(hour_charge[(hour_charge['seo变化数据团队']=='martin') & (hour_charge['小时数']>=22)& (hour_charge['小时数']<24)])/df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'22-24'].iloc[0]*100,2)

# 7总计
df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'总计'] =df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'0-2':].T.sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'总计'] =df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'0-2':].T.sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'总计'] =df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'0-2':].T.sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='开户'),'总计'] =df.loc[(df['人员']=='Martin') & (df['指标']=='开户'),'0-2':].T.sum()
df.loc[(df['人员']=='Martin') & (df['指标']=='开户转化率'),'总计'] =round(df.loc[(df['人员']=='Martin') & (df['指标']=='开户'),'总计'].iloc[0] / df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'总计'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='注册率'),'总计'] =round(df.loc[(df['人员']=='Martin') & (df['指标']=='注册'),'总计'].iloc[0] / df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'总计'].iloc[0]*100,2)

# 8接收率
df.loc[(df['人员']=='Martin') & (df['指标']=='接收率'),'总计'] =round(df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'总计'].iloc[0] / df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'总计'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='接收率'),'0-2'] =round(df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'0-2'].iloc[0] / df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'0-2'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='接收率'),'2-4'] =round(df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'2-4'].iloc[0] / df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'2-4'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='接收率'),'4-6'] =round(df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'4-6'].iloc[0] / df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'4-6'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='接收率'),'6-8'] =round(df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'6-8'].iloc[0] / df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'6-8'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='接收率'),'8-10'] =round(df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'8-10'].iloc[0] / df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'8-10'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='接收率'),'10-12'] =round(df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'10-12'].iloc[0] / df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'10-12'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='接收率'),'12-14'] =round(df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'12-14'].iloc[0] / df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'12-14'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='接收率'),'14-16'] =round(df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'14-16'].iloc[0] / df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'14-16'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='接收率'),'16-18'] =round(df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'16-18'].iloc[0] / df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'16-18'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='接收率'),'18-20'] =round(df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'18-20'].iloc[0] / df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'18-20'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='接收率'),'20-22'] =round(df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'20-22'].iloc[0] / df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'20-22'].iloc[0]*100,2)
df.loc[(df['人员']=='Martin') & (df['指标']=='接收率'),'22-24'] =round(df.loc[(df['人员']=='Martin') & (df['指标']=='接收IP数'),'22-24'].iloc[0] / df.loc[(df['人员']=='Martin') & (df['指标']=='发送IP数'),'22-24'].iloc[0]*100,2)

print(df[df['人员']=='Martin'])