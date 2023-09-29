import pandas as pd
import datetime
import xlwings as xw

pd.set_option('display.max_colwidth', None) #显示单元格完整信息
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# 读取会员列表
member = pd.read_csv(r'C:\Users\User\Desktop\文件\追击\0928\会员列表导出.csv',encoding='gbk')
# 读取交易失败列表
fail_trade = pd.read_csv(r'C:\Users\User\Desktop\文件\追击\0928\交易明细报表.csv',encoding='gbk')
#读取P图诈单
pitu = pd.read_csv(r'C:\Users\User\Desktop\文件\追击\0928\P图骗分名单.csv',encoding='gbk')
#读取既往名单
pre_member = pd.read_excel(r'C:\Users\User\Desktop\文件\追击\0928\电销追击928.xlsx','本月名单汇总')
#读取代理线
daili = pd.read_excel(r'C:\Users\User\Desktop\文件\追击\0928\电销追击928.xlsx','代理线')
#去除重复代理线
daili.drop_duplicates('代理线',inplace = True)

#-----------------------开始处理-----------------------
member2 = member.merge(pitu['用户名'],left_on='会员账号',right_on='用户名',how='left')
member2 = member2.rename(columns = {'用户名':'P图骗分'})

fail_trade2 = fail_trade.drop_duplicates('账户名')
member3 = member2.merge(fail_trade2[['账户名','状态']],left_on='会员账号',right_on='账户名',how='left')
member3=member3.rename(columns={'状态_x':'状态','状态_y':'提单失败'})
member3.drop('账户名',axis=1,inplace=True)


member4 = member3.merge(daili,left_on='代理',right_on='代理线',how='left')

member5 = member4.merge(pre_member[['会员账号','提供时间']],on='会员账号',how='left')
member5=member5.rename(columns={'提供时间':'已提供'})

#最终提供名单
result = member5.loc[(member5['手机号码'].apply(lambda x: len(str(x)))==11)&(member5['状态']=='正常')&(member5['VIP等级']=='VIP0') \
                     &(member5['提单失败']=='失败')&(member5['已提供'].isna())&(member5['P图骗分'].isna())&(~member5['代理线'].isna()),]
result = result[['会员账号','手机号码','代理','VIP等级','注册时间','状态']]
result.insert(0,'提供时间',datetime.datetime.now().strftime('%Y%m%d')+'-12')
# result['提供时间']= datetime.datetime.now().strftime('%Y%m%d')+'-12'
# 筛选新增代理线
# 筛选新增代理线
result2 = member5.loc[(member5['手机号码'].apply(lambda x: len(str(x)))==11)&(member5['状态']=='正常')&(member5['VIP等级']=='VIP0')&(member5['提单失败']=='失败')&(member5['已提供'].isna())&(member5['P图骗分'].isna())&(member5['代理线'].isna()),]
add_daili = result2.loc[result2['代理'].str.startswith(('btyseo','btydl','wbdl')),]['代理']


print(result)
print(result.shape)
print(add_daili.shape)
print(add_daili)

#写入本月工作簿
app = xw.App(visible=False,add_book=False)
book = app.books.open(r'C:\Users\User\Desktop\文件\追击\0928\电销追击928.xlsx')
sheet_daili= book.sheets['代理线']
row_daili = sheet_daili.used_range.last_cell.row

sheet= book.sheets['本月名单汇总']
row = sheet.used_range.last_cell.row
#增加名单
if len(result)>0:
    sheet['A'+str(row+1)].options(index=False,header = False).value = result
#增加代理线
if len(add_daili)>0:
    sheet_daili['A'+str(row_daili+1)].options(index=False,header = False).value = add_daili
curr_sheet = book.sheets['今日名单(12点)']
curr_sheet.clear_contents()
if len(result)>0:
    curr_sheet['A1'].options(index=False,header = True).value = result
book.save()
book.close()
app.quit()


