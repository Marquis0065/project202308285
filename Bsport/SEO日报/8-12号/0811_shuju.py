import pandas as pd
import numpy as np
import datetime
import xlwings as xw
pd.set_option('display.max_colwidth', None) #显示单元格完整信息
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

user = pd.read_csv(r'C:\Users\User\Desktop\SEO\_0811\会员列表导出.csv',encoding='gbk')
firChargeUser = pd.read_csv(r'C:\Users\User\Desktop\SEO\_0811\会员首存报表.csv',encoding='gbk')
data = pd.read_excel(r'C:\Users\User\Desktop\SEO\_0811\今日数据.xlsx')
daili = pd.read_excel(r'C:\Users\User\Desktop\SEO\SEO-每日更新.xlsx','代理总表')

shuju = pd.DataFrame({'人员':['Paddy', 'Tony', 'Max', 'Martin', 'Zed', 'Hugo', 'Aber', 'DK', 'Ben','当日汇总'],
                      '日期':(datetime.datetime.now()+datetime.timedelta(days=-3)).strftime('%Y/%m/%d'),
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
his_data  = pd.read_excel(r'C:\Users\User\Desktop\SEO\_0807\SEO每日模板-每日更新.xlsx','历史')
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

# 向历史数据中追加今日数据
# app = xw.App(visible=False,add_book=False)
# book = app.books.open(r'C:\Users\User\Desktop\SEO\SEO-每日更新.xlsx')
# sheet = book.sheets['历史']
# sheet.range('A' + str(sheet.cells.last_cell.row + 1)).value = shuju
# book.close()
# app.quit()
# print(shuju)
# ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V']
# shuju = shuju.rename(columns = {'日期':'A', '人员':'B', '发送IP':'C', '接受IP':'D', '注册':'E', '注册率(%)':'F',
# '开户':'G', '转化率(%)':'H', '当日注册并开户':'I', '当日注册激活率(%)':'J', '对比昨天(总IP)':'K', '对比前3天均值(总IP)':'L',
# '对比前5天均值(总IP)':'M','对比前7天均值(总IP)':'N', '对比昨天(总注册)':'O', '对比前3天均值(总注册)':'P', '对比前5天均值(总注册)':'Q',
# '对比前7天均值(总注册)':'R', '对比昨天(总开户)':'S', '对比前3天均值(总开户)':'T', '对比前5天均值(总开户)':'U','对比前7天均值(总开户)':'V'})
# shuju.reset_index(drop=True,inplace=True)
print(shuju)
# shuju['A'] = shuju['A'].astype('str')
# from openpyxl import Workbook,load_workbook
# book = load_workbook(r'C:\Users\User\Desktop\SEO每日更新_814.xlsx')
# sheet_names=book.sheetnames
# sheet = book.get_sheet_by_name('Sheet1')
# sheet.append(shuju.to_dict(orient='list'))
# book.save()
# book.close()

shuju.to_csv(r'C:\Users\User\Desktop\SEO每日更新_811.csv',index=False,header=False)
