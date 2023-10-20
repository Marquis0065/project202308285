import pandas as pd
import os,re
from datetime import datetime
import numpy as np

# 读取文件夹excel上下并表
def func_concat(folderpath): # os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\会员输赢报表'
    df_all=pd.DataFrame()# 总表用来上下并表
    for filename in os.listdir(folderpath):# 先读取所有文件
        print(datetime.now().strftime('%H:%M:%S'),'开始读取',filename)
        path=folderpath+'\\'+filename# 文件路径
        if filename.endswith('.xlsx'):# 判断文件格式以及读取
            dfname=pd.ExcelFile(path)
            df_child=pd.DataFrame()
            for sheetname in dfname.sheet_names:
                print(datetime.now().strftime('%H:%M:%S'),'sheet',sheetname)
                df_sheet=pd.read_excel(path,sheet_name=sheetname)
                df_child=pd.concat([df_child,df_sheet],ignore_index=True)
        elif filename.endswith('.txt'):
            df_child=pd.read_csv(path,sep='\t')
        elif filename.endswith('.csv'):
            df_child=pd.read_csv(path,sep=',')
        else:
            print(folderpath,'的文件不是xlsx/txt/后台csv格式')
        df_all=pd.concat([df_all,df_child],ignore_index=True)# 并表
    df_all.drop_duplicates(inplace=True)# 去重复
    return df_all

# 读取以及获得名单
def func_mingdan(foldername):
    df_mingdan = func_concat(foldername)
    for i in df_mingdan.columns:
        df_mingdan[i] =df_mingdan[i].astype(str).apply(lambda x: x.strip('\t'))# 去除首尾空格
    df_mingdan['会员账号']=df_mingdan['会员账号'].str.replace(('\t|\r|\n| '), '',regex=True) #获得名单
    df_mingdan=df_mingdan[df_mingdan['会员账号']!='总计']
    df_mingdan_ndup=df_mingdan['会员账号'].drop_duplicates().str.replace(('\t|\r|\n| '), '',regex=True) #获得名单
    df_mingdan_ndup=df_mingdan_ndup.to_frame()
    return df_mingdan_ndup,df_mingdan
# df_mingdan_ndup,df_mingdan = cf.func_mingdan('原始数据'+'\\'+'名单')

# 输出函数，大数据量,1df多表格
def func_multisheet(dfname,excelpath,sheetlength):
    print(datetime.now().strftime('%H:%M:%S'),'开始输出',excelpath)
    if len(dfname)>1048576:
        writer = pd.ExcelWriter(excelpath)
        for i in range(0, len(dfname), sheetlength):
            print(datetime.now().strftime('%H:%M:%S'),i,'行到',i+sheetlength,'行写入','Row {}'.format(i),'工作表')
            dfname.iloc[i:i+sheetlength,].to_excel(writer, sheet_name='Row {}'.format(i),index=False, freeze_panes=(1, 4))
        writer.close()
    else:
        dfname.to_excel(excelpath,index=False, freeze_panes=(1, 4))
    # cf.func_multisheet(df_linglong,'脚本数据.xlsx',1000000)
def func_multicsv(dfname,sheetlength):
    print(datetime.now().strftime('%H:%M:%S'),'开始输出')
    if len(dfname)>1048576:
        for i in range(0, len(dfname), sheetlength):
            print(datetime.now().strftime('%H:%M:%S'),i,'行到',i+sheetlength,'行写入','Row {}'.format(i),'csv')
            dfname.iloc[i:i+sheetlength,].to_csv('Row {}'.format(i)+'.csv',index=False)
    else:
        dfname.to_csv('Row {}'.format(len(dfname))+'.csv',index=False)
    # cf.func_multicsv(df_linglong,1000000)

# 小数据量,多df多表格
def func_multidf(list_df,list_dfname,excelpath,str_index):
    print(datetime.now().strftime('%H:%M:%S'),'开始输出',excelpath)
    writer = pd.ExcelWriter(excelpath)
    for (i,j) in zip(list_df, list_dfname):
        print(datetime.now().strftime('%H:%M:%S'),'写入',j,'工作表')
        if str_index=='noindex':
            i.to_excel(writer, sheet_name=j,index=False, freeze_panes=(1, 4))
        else:
            i.to_excel(writer, sheet_name=j, freeze_panes=(1, 4))
    writer.close()
import itertools
# cf.func_multidf(list_df,list_dfname,'脚本数据.xlsx','noindex')

def func_zuzhi(df): #匹配组织关系
    df_zuzhi = func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\bty手工表格\\组织关系')
    for i in ['代理']:  #列 更改名称
        if i in df.columns:
            df.rename(columns={i: '上级代理'}, inplace=True)
    df=df.merge(df_zuzhi,on='上级代理',how='left')
    df.loc[df['一级部门'].isnull(),'一级部门']='空白'# 一级部门 空的数据
    # 处理 (一级部门 未知)&(上级代理 wbdl)的情况
    for i in df.columns:
        if '币种' in i:
            df.loc[(df[i].str.contains('CNY', case=False))&(df['一级部门']=='未知')&(df['上级代理'].str.contains('wbdl', case=False)),['一级部门','二级部门']]=['外代','wbdl'] #币种CNY 则是外代
            df.loc[(df[i].str.contains('VND', case=False))&(df['一级部门']=='未知')&(df['上级代理'].str.contains('wbdl', case=False)),['一级部门','二级部门']]=['外代-越','wbdl'] #币种VND 则是外代-越
    return df

# read daily vip level excels(merge namesheet with each excel)
def func_read_filedate(df_mingdan,folderpath): # os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\会员输赢报表'
    df_vip_all=pd.DataFrame()# 读取vip等级文件 加一列日期,
    for filename in os.listdir(folderpath):
        print(datetime.now().strftime('%H:%M:%S'),filename)
        date=re.search(r'\d+', filename).group(0)# 日期从文件名称获取,日期格式，列 第几周
        path=folderpath+'\\'+filename
        df_vip_child=pd.read_csv(path,sep=',')
        df_vip_child['日期']=pd.to_datetime(str(date), format='%Y%m%d')
        if df_mingdan!=None:
            df_vip_child=df_vip_child.merge(df_mingdan,on='会员账号',  how='inner')# 读取时比对名单，不然30个vip文件超出pandas一张sheet的处理能力
        df_vip_all=pd.concat([df_vip_all,df_vip_child],ignore_index=True)
    df_vip_all.drop_duplicates(inplace=True)
    return df_vip_all
def func_read_folderdate(folderpath): # os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\会员输赢报表'
    df_shuying_all=pd.DataFrame()# 读取shuying等级文件 加一列日期,
    for filename in os.listdir(folderpath):
        print(datetime.now().strftime('%H:%M:%S'),filename)
        date=re.search(r'\d+', filename).group(0)# 日期从文件名称获取,日期格式，列 第几周
        df_shuying_child=func_concat(folderpath+'\\'+filename)
        df_shuying_child['日期']=pd.to_datetime(str(date), format='%Y%m%d')
        df_shuying_all=pd.concat([df_shuying_all,df_shuying_child],ignore_index=True)
    df_shuying_all.drop_duplicates(inplace=True)
    return df_shuying_all

# 读取和匹配vip等级变动
def func_read_vip(df_mingdan,folderpath): # os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\会员输赢报表'
    df_vip_all=pd.DataFrame()# 读取vip等级文件 加一列日期,
    for filename in os.listdir(folderpath):
        print(datetime.now().strftime('%H:%M:%S'),filename)
        path=folderpath+'\\'+filename
        df_vip_child=pd.read_csv(path,sep=',')
        if df_mingdan is not None:
            df_vip_child=df_vip_child.merge(df_mingdan,on='会员账号',  how='inner')# 读取时比对名单，不然30个vip文件超出pandas一张sheet的处理能力
        df_vip_all=pd.concat([df_vip_all,df_vip_child],ignore_index=True)
    df_vip_all.drop_duplicates(inplace=True)
    return df_vip_all

def func_vip_diff2(df_vip_all):
    df_vip_max=df_vip_all[df_vip_all['日期']==max(df_vip_all['日期'])]# max日期获得一张新表格，列更改为，最后一日，最后一日vip等级
    df_vip_max.rename(columns={'日期': '最后一日', 'VIP等级': '最后一日vip等级'}, inplace=True)
    df_vip_min=df_vip_all[df_vip_all['日期']==min(df_vip_all['日期'])]# min日期获得一张新表格，列更改为，第1日，第1日vip等级
    df_vip_min.rename(columns={'日期': '第1日', 'VIP等级': '第1日vip等级'}, inplace=True)
    df_vip_diff2=df_vip_max.merge(df_vip_min,on='会员账号',how='outer')# index 会员账号 merge两张表格，新增列 31天等级变化=最后一日vip等级-第1日vip等级
    df_vip_diff2.fillna({'最后一日vip等级': 0, '第1日vip等级': 0}, inplace=True)# minus的列不能有nan，需要填充0
    df_vip_diff2['等级变化']=df_vip_diff2['最后一日vip等级']-df_vip_diff2['第1日vip等级']
    return df_vip_diff2
def func_vip_diff3(df_vip_all):
    df_vip_max=df_vip_all[df_vip_all['日期']==max(df_vip_all['日期'])]# max日期获得一张新表格，列更改为，最后一日，最后一日vip等级
    df_vip_max.rename(columns={'日期': '活动后', 'VIP等级': '活动后vip等级'}, inplace=True)
    df_vip_min=df_vip_all[df_vip_all['日期']==min(df_vip_all['日期'])]# min日期获得一张新表格，列更改为，第1日，第1日vip等级
    df_vip_min.rename(columns={'日期': '活动前', 'VIP等级': '活动前vip等级'}, inplace=True)
    df_vip_medium=df_vip_all[(df_vip_all['日期']>min(df_vip_all['日期']))&(df_vip_all['日期']<max(df_vip_all['日期']))]# min日期获得一张新表格，列更改为，第1日，第1日vip等级
    df_vip_medium.rename(columns={'日期': '活动期间', 'VIP等级': '活动期间vip等级'}, inplace=True)
    df_vip_diff2=df_vip_max.merge(df_vip_min,on='会员账号',how='outer').merge(df_vip_medium,on='会员账号',how='outer')
    df_vip_diff2.fillna({'活动后vip等级': 0, '活动前vip等级': 0, '活动期间vip等级': 0}, inplace=True)# minus的列不能有nan，需要填充0
    df_vip_diff2['活动期间等级变化']=df_vip_diff2['活动期间vip等级']-df_vip_diff2['活动前vip等级']
    df_vip_diff2['活动后等级变化']=df_vip_diff2['活动后vip等级']-df_vip_diff2['活动期间vip等级']
    return df_vip_diff2

# 解压文件(与程序相比还差3倍速度)
def func_unzip(path,extractpath):
    zip_ref = zipfile.ZipFile(path) # create zipfile object
    zip_ref.extractall(extractpath,pwd=b'123456') # extract file to dir
    zip_ref.close() # close file
    os.remove(path) # delete zipped file
import multiprocessing as mp
import zipfile
# def main():
#     list_path=[]# 得到文件路径list
#     list_extractpath=[]
#     for i in ['投注记录','大客']:#需要解压的文件夹名称
#         for filename_i in os.listdir(os.path.abspath(os.getcwd())+'\\'+'原始数据'+'\\'+i):
#             for filename_j in os.listdir(os.path.abspath(os.getcwd())+'\\'+'原始数据'+'\\'+i+'\\'+filename_i):
#                 if filename_j.endswith(".zip"): # check for ".zip" extension
#                     extractpath=os.path.abspath(os.getcwd())+'\\'+'原始数据'+'\\'+i+'\\'+filename_i
#                     path=os.path.abspath(os.getcwd())+'\\'+'原始数据'+'\\'+i+'\\'+filename_i+'\\'+filename_j
#                     list_extractpath.append(extractpath)
#                     list_path.append(path)
#     if __name__=="__main__":# 多进程解压
#         if len(list_path)>0:
#             print(datetime.now().strftime('%H:%M:%S'),'开始解压')
#             pool = mp.Pool(min(mp.cpu_count(), len(list_path))) # number of workers
#             pool.starmap(cf.func_unzip, zip(list_path, list_extractpath))
#             pool.close()
#             print(datetime.now().strftime('%H:%M:%S'),'结束解压')

#日期表格得到往前n天起的tianshu天
def func_riqi(tianshu,n):
    base = datetime.today().date()# merge完整日期，空白处填上0
    date_list = [base -timedelta(days=x) for x in range(tianshu+n)][n:]
    df_riqi=pd.DataFrame({'日期':date_list})
    df_riqi['日期']=pd.to_datetime(df_riqi['日期']).dt.date
    return df_riqi
from datetime import timedelta
# df_liushuicunkuan_huiyuan=func_riqi(df_liushuicunkuan_huiyuan)# 补全日期函数-空白处填上0
# df_liushuicunkuan_huiyuan.fillna({'流水存款上分额': 0, '有效投注': 0}, inplace=True)

def func_color(list_df):#上色
    list_df_color=[]
    for df in list_df:
        integer_columns = df.select_dtypes(include=['int64','float64']).columns#改千分位 整列
        for i in integer_columns:
            df[i].fillna(0,inplace=True)
            if '率' in i or '比例' in i:
                df[i]=df[i].map(lambda n: '{:.2%}'.format(n))
            elif '两位小数' in i :
                df[i]=df[i].apply(lambda x: round(x, 2))
                df.rename(columns={i:i[:-4]},inplace=True)
            else:
                df[i]=df[i].astype(int)
                df[i]=df[i].apply('{:,}'.format)
        df = df.style.set_properties(**{'background-color': '#FED8B1'}, subset=pd.IndexSlice[pd.to_datetime(df['日期']).dt.day%2!=0, df.columns])#日期行着色
        df = df.set_properties(**{'border': '1px black solid','font-family': 'Microsoft YaHei'})# 全表框线和字体
        df = df.applymap_index(lambda _: 'background-color: steelblue; color: white;font-family: Microsoft YaHei;', axis=1)#header着色
        # 列宽行宽
        list_df_color.append(df)
    return list_df_color
# list_df_color=cf.func_color(list_df)


def func_period_day(df_linglong,str_date):#截取当日数据
    if str_date=='昨天':# 目标数据准备日期
        date_latest=max(df_linglong['日期'])
        df_linglong=df_linglong[df_linglong['日期']==max(df_linglong['日期'])]#截取当日数据
    else:#‘2023-6-18’
        df_linglong=df_linglong[df_linglong['日期']==str_date]#截取当日数据
    return df_linglong,date_latest

def func_constlist(date_latest,date_first_this_month):#时间进度计算
    date_first_next_month = date_latest.replace(day=1).replace(month=date_latest.month+1)# date下月1日
    days_month_remain = (date_first_next_month - date_latest).days-1 # 本月剩余天数=下月1日-指定日期-1
    days_month_passed = (date_latest-date_first_this_month).days+1 # 本月度过天数=指定日期-本月1日+1
    days_whole_month=   (date_first_next_month-date_first_this_month).days  # 本月天数=下月1日-本月1日
    list_constant_header=['开始日期','结束日期','下月一号','本月剩余天数','本月度过天数','本月天数']
    list_constant=[date_first_this_month,date_latest,date_first_next_month,days_month_remain,days_month_passed,days_whole_month]
    return list_constant_header,list_constant
def func_period_inmonth(df_linglong,str_date):#截取多日数据
    if  str_date=='本月':#截取本月数据
        date_latest=max(df_linglong['日期'])
        date_first_this_month = date_latest.replace(day=1)# date本月1日
        df_linglong_period=df_linglong[(df_linglong['日期']<=date_latest)&(df_linglong['日期']>=date_first_this_month)]
    elif str_date=='本月到前一天':#截取本月到前一天数据
        date_latest=max(df_linglong['日期'])-timedelta(days=1)
        date_first_this_month = date_latest.replace(day=1)# date本月1日
        df_linglong_period=df_linglong[(df_linglong['日期']<=date_latest)&(df_linglong['日期']>=date_first_this_month)]
    list_constant_header,list_constant=func_constlist(date_latest,date_first_this_month)#一个日期划分一个月
    return df_linglong_period,list_constant_header,list_constant

def func_period_2month(df_pingtai):# 根据表格最新日期标注本月上月
    #截取数据准备
    date_latest=max(df_pingtai['日期'])#本月结束日期
    date_first_this_month = date_latest.replace(day=1)# date本月1日
    date_first_last_month = date_latest.replace(day=1).replace(month=date_latest.month-1)# date上月1日
    date_latest_last_month = date_latest.replace(month=date_latest.month-1)# date上月结束日期
    date_first_next_month = date_latest.replace(day=1).replace(month=date_latest.month+1)# date下月1日
    #截取本月数据
    print('报表本月结束日期为',str(date_latest))
    df_pingtai.loc[(df_pingtai['日期']<=date_latest)&(df_pingtai['日期']>=date_first_this_month),'月份']='本月'
    # 截取上月数据
    # 判断是否是最后一天
    if (date_first_next_month-date_latest).days==1:#当月最后一天，上月也取最后一天
        date_latest_last_month = date_first_this_month-timedelta(days=1)# date上月结束日期改为最后一天
    print('报表上月结束日期为',str(date_latest_last_month))
    df_pingtai.loc[(df_pingtai['日期']<=date_latest_last_month)&(df_pingtai['日期']>=date_first_last_month),'月份']='上月'
    return df_pingtai
# from datetime import timedelta

def func_shijianduan(df,list_column_date,childfolder): # 根据df的list_column_date标注数据的时间段
    df_shijian = func_concat(os.path.abspath(os.getcwd())+'\\时间参数\\'+childfolder)# 读取时间段
    for i in ['开始日期','结束日期']:
        df_shijian[i]=pd.to_datetime(df_shijian[i]).dt.date
    for i in list_column_date:
        df[i].replace('-', np.nan, inplace=True) #值替换
        df[i]=pd.to_datetime(df[i]).dt.date
    for i in df_shijian.index:
        for j in list_column_date:
            df.loc[(df[j]>=df_shijian.loc[i,'开始日期'])&(df[j]<=df_shijian.loc[i,'结束日期']),['开始日期','结束日期']]=[df_shijian.loc[i,'开始日期'],df_shijian.loc[i,'结束日期']]
    df.dropna(subset=['开始日期'],inplace=True)
    return df
# df=cf.func_shijianduan(df,list_column_date)  # 根据df的list_column_date标注数据的时间段
