import pandas as pd
import numpy as np
import datetime
pd.set_option('display.max_colwidth', None) #显示单元格完整信息
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

user = pd.read_csv(r'C:\Users\User\Desktop\SEO_0807\会员列表导出.csv',encoding='gbk')
firChargeUser = pd.read_csv(r'C:\Users\User\Desktop\SEO_0807\会员首存报表.csv',encoding='gbk')
data = pd.read_excel(r'C:\Users\User\Desktop\SEO_0807\data\今日数据.xlsx')
daili = pd.read_excel(r'C:\Users\User\Desktop\SEO_0807\SEO每日模板-每日更新.xlsx','代理总表')

shuju = pd.DataFrame({'人员':['Paddy', 'Tony', 'Max', 'Martin', 'Zed', 'Hugo', 'Aber', 'DK', 'Ben'],
                      '日期':(datetime.datetime.now()+datetime.timedelta(days=-3)).strftime('%Y/%m/%d'),
                      '发送IP':[i for i in range(9)],'接受IP':[i for i in range(9)]})
shuju.set_index('人员',inplace = True)
shuju.sort_index(inplace=True)

data['IP']=pd.to_numeric(data['IP'],errors='coerce').replace(np.nan,0)
grp=data.groupby('网站名(domain)').agg({'IP':sum})

shuju.loc['Paddy','发送IP']=grp.loc['paddy.com','IP']
shuju.loc['Paddy','接受IP']=grp.loc['paddy.bty','IP']
shuju.loc['Tony','发送IP']=grp.loc['tonyb.com','IP']/2
shuju.loc['Tony','接受IP']=grp.loc['tonyb.com','IP']
shuju.loc['Max','发送IP']=grp.loc['mulu.com','IP']
shuju.loc['Max','接受IP']=grp.loc['max.bty','IP']
shuju.loc['Martin','发送IP']=grp.loc['redquan.com','IP']
shuju.loc['Martin','接受IP']=grp.loc['martin.bty','IP']
shuju.loc['Zed','发送IP']=grp.loc['zed.com','IP']
shuju.loc['Zed','接受IP']=grp.loc['zed.bty','IP']
shuju.loc['Hugo','发送IP']=grp.loc['hugo.com','IP']
# shuju.loc['Hugo','接受IP']=grp.loc['hugo.bty','IP']
shuju.loc['Hugo','接受IP']=0

shuju.loc['Aber','发送IP']=grp.loc['aber.com','IP']/2
shuju.loc['Aber','接受IP']=grp.loc['aber.bty','IP']
shuju.loc['DK','发送IP']=grp.loc['dk.com','IP']/2
shuju.loc['DK','接受IP']=grp.loc['dk.bty','IP']
shuju.loc['Ben','发送IP']=grp.loc['ben.com','IP']/2
shuju.loc['Ben','接受IP']=grp.loc['ben.bty','IP']

shuju['日期'] = pd.to_datetime(shuju['日期'])
shuju.insert(1,'人员2',shuju.index)
shuju['人员2']=shuju['人员2'].str.lower()
shuju.reset_index(inplace=True)

merge_user = pd.merge(user,daili,how = 'left',left_on='代理',right_on='代理线')
grpSEO = merge_user.groupby('seo变化数据团队').agg({'seo变化数据团队':len})
grpSEO.rename(columns={'seo变化数据团队':'注册'},inplace=True)
grpSEO.reset_index(inplace=True)
grpSEO['人员2'] = grpSEO['seo变化数据团队'].str.lower()
grpSEO.set_index('seo变化数据团队',inplace=True)

# 第1次merge
shuju = pd.merge(shuju,grpSEO,on='人员2')
shuju['注册率'] = shuju['注册']/shuju['发送IP']*100

merge_charge = pd.merge(firChargeUser,daili,how='left',left_on='所属代理',right_on='代理线')
grpCHARGE = merge_charge.groupby('seo变化数据团队').agg({'seo变化数据团队':len})
grpCHARGE= grpCHARGE.rename(columns={'seo变化数据团队':'开户'})
grpCHARGE.reset_index(inplace=True)
grpCHARGE['seo变化数据团队']=grpCHARGE['seo变化数据团队'].str.lower()
grpCHARGE= grpCHARGE.rename(columns={'seo变化数据团队':'人员2'})

# 第2次merge
shuju = pd.merge(shuju,grpCHARGE,how='left',on='人员2')
shuju['转化率'] = shuju['开户']/shuju['注册']*100

grp3  = merge_charge[merge_charge['注册时间'].str[:9]==merge_charge['交易时间'].str[:9]].groupby('seo变化数据团队').agg({'seo变化数据团队':len})
grp3.rename(columns = {'seo变化数据团队':'当日注册并开户'},inplace=True)
grp3.reset_index(inplace=True)
grp3['seo变化数据团队'] =grp3['seo变化数据团队'].str.lower()
grp3.rename(columns = {'seo变化数据团队':'人员2'},inplace=True)
# 第3次merge
shuju  = pd.merge(shuju,grp3,how='left',on='人员2')
shuju['当日注册激活率'] = shuju['当日注册并开户']/shuju['注册']*100
print(shuju)


his_data  = pd.read_excel(r'C:\Users\User\Desktop\SEO_0807\SEO每日模板-每日更新.xlsx','历史')
be_data = his_data[his_data['日期']==(shuju['日期'][0]+datetime.timedelta(days=-2))][:-1]

shuju.set_index('人员',inplace=True)
shuju.sort_index(inplace=True)
be_data.set_index('人员',inplace=True)
be_data.sort_index(inplace=True)


be3_data = his_data[his_data['日期']>(shuju['日期'][0]+datetime.timedelta(days=-3))]
be3_data = be3_data.groupby('人员').mean()[:-1]
be5_data = his_data[his_data['日期']>(shuju['日期'][0]+datetime.timedelta(days=-5))]
be5_data = be5_data.groupby('人员').mean()[:-1]
be7_data = his_data[his_data['日期']>(shuju['日期'][0]+datetime.timedelta(days=-7))]
be7_data = be7_data.groupby('人员').mean()[:-1]

all_ip= shuju.iloc[:,:3]
all_ip['对比昨天(总IP)']=shuju['发送IP']-be_data['总IP']
all_ip['对比前3天均值(总IP)']= shuju['发送IP']-be3_data['总IP']
all_ip['对比前5天均值(总IP)']= shuju['发送IP']-be5_data['总IP']
all_ip['对比前7天均值(总IP)']= shuju['发送IP']-be7_data['总IP']

all_ip['对比昨天(总注册)']=shuju['发送IP']-be_data['总IP']
all_ip['对比前3天均值(总注册)']= shuju['注册']-be3_data['注册']
all_ip['对比前5天均值(总注册)']= shuju['注册']-be5_data['注册']
all_ip['对比前7天均值(总注册)']= shuju['注册']-be7_data['注册']

all_ip['对比昨天(总开户)']=shuju['发送IP']-be_data['总IP']
all_ip['对比前3天均值(总开户)']= shuju['开户']-be3_data['开户']
all_ip['对比前5天均值(总开户)']= shuju['开户']-be5_data['开户']
all_ip['对比前7天均值(总开户)']= shuju['开户']-be7_data['开户']
# 纵向连接表格
shuju=shuju.join(all_ip,rsuffix='_2')
shuju.drop(['日期_2','人员2_2','发送IP_2'],inplace=True,axis=1)


print(shuju)
