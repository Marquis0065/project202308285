# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import os,sys,re
import common_func as cf
import _func as of

pd.set_option('display.max_colwidth', None) #显示单元格完整信息
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

sys.path.append(os.path.dirname(os.path.abspath(os.getcwd())))


# 电维1会员输赢总数据
def work_dianwei1_shuying():
    # 最新电维1名单表格
    df_dianwei1 = cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\bty手工表格\\电维1名单')
    df_dianwei1=df_dianwei1[['会员账号','经理','分配日期']]
    df_dianwei1['经理'] = df_dianwei1['经理'].str.lower().str.replace(('\t|\r|\n| '), '',regex=True) #经理转小写&去除符号
    df_dianwei1.drop_duplicates(inplace=True)# 去重复
    # 匹配当月输赢表格
    df_shuying=cf.func_read_folderdate(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\会员输赢报表\\原始数据')# 读取+增加日期
    for i in ['存款金额','提款金额','平台坐庄-投注金额','平台坐庄-下注金额','平台坐庄-派彩金额','平台坐庄-公司输赢','玩家对战-下投注额','玩家对战-玩家输赢','玩家对战-公司抽水','公司总盈利(代理)','红利金额','返水金额','投注次数','有效投注金额']:
        df_shuying.loc[df_shuying[i]!=0,'重要数值']=1
    df_shuying=df_shuying[df_shuying['重要数值']==1]
    for i in ['首存人数','首存金额','存款人数','取款人数','加币','减币','存款手续费','提款手续费','上分总额','上分次数','用户类型']:
        df_shuying.drop(i, axis=1, inplace=True)#drop操作 列
    df_shuying2= cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\会员输赢报表\\同事汇总') #读取同事处理过的输赢报表
    df_shuying=pd.concat([df_shuying,df_shuying2],ignore_index=True)
    df_shuying.drop_duplicates(inplace=True)
    df_shuying.rename(columns={'账户名': '会员账号'}, inplace=True)#列 更改名称
    df_shuying=df_shuying[['日期','币种','会员账号','上级代理','存款金额','有效投注金额','公司总盈利(代理)']]
    # 修改时间段函数，增加 文件夹参数
    df_shuying=cf.func_shijianduan(df_shuying,['日期'],'两月')  # 根据df的
    df_dianwei1=df_dianwei1.merge(df_shuying,on='会员账号',how='left')
    df_dianwei1.to_csv('river数据\\'+'营销数据输赢.csv', encoding='utf_8_sig',index=False)  #river
    for df in [df_dianwei1]:
        for i in ['存款金额','有效投注金额','公司总盈利(代理)']:
            df.loc[df['币种']=='VND',i]=df.loc[df['币种']=='VND',i]/3300
            df.loc[df['币种']=='USDT',i]=df.loc[df['币种']=='USDT',i]*7
    return df_dianwei1

# 每日前10
def work3(df_dianwei1):
    df_dianwei1_copy=df_dianwei1.copy()
    df_dianwei1_copy = df_dianwei1_copy.dropna(subset=['经理'])
    df_dianwei1_copy.drop('开始日期', axis=1, inplace=True)#drop操作 列
    df_dianwei1_copy=cf.func_shijianduan(df_dianwei1_copy,['日期'],'本月')  # 根据df的
    df_dianwei1_shuying=pd.DataFrame()      #分日期新建一个表
    for i in df_dianwei1_copy['日期'].drop_duplicates().tolist():   #对日期去重
        df_shuying_child=df_dianwei1_copy[(df_dianwei1_copy['日期']==i)]
        df_shuying_child['每日排序有效投注金额'] = df_shuying_child['有效投注金额'].astype(float).rank(ascending=False)        #增加列项，对公司盈利排序
        df_dianwei1_shuying=pd.concat([df_dianwei1_shuying,df_shuying_child],ignore_index=True)
    df_dianwei1_shuying.to_csv('river数据\\'+'营销数据流水排名.csv', encoding='utf_8_sig',index=False)  #river
    df_dianwei1_shuying.loc[df_dianwei1_shuying['每日排序有效投注金额']>=11,'每日排序有效投注金额'] = np.nan
    df_dianwei1_shuying=df_dianwei1_shuying[df_dianwei1_shuying['每日排序有效投注金额'].notnull()]
    # 	添加游戏平台数据（注单记录）
    df_dianwei1_mingdan=df_dianwei1_shuying['会员账号'].drop_duplicates().to_frame() #名单
    df_dianwei1_touzhu=of.func_touzhu_readnprocess(df_dianwei1_mingdan,['派彩时间','会员账号','场馆类型','游戏平台','子游戏','币种'],'大客注单记录')
    df_dianwei1_touzhu['游戏杀率']=np.where(df_dianwei1_touzhu['有效投注']>0,df_dianwei1_touzhu['公司盈利']/df_dianwei1_touzhu['有效投注'],0)# 增加游戏杀率列
    df_dianwei1_touzhu['游戏杀率百分号']=(df_dianwei1_touzhu['游戏杀率']).map(lambda n: '{:.2%}'.format(n))
    df_dianwei1_touzhu.sort_values(by='公司盈利',inplace=True)  # 排序-游戏详情根据盈亏排序
    integer_columns = df_dianwei1_touzhu.select_dtypes(include=['int64','float64']).columns #千分号
    for i in integer_columns:
        df_dianwei1_touzhu[i]=df_dianwei1_touzhu[i].astype(int).apply('{:,}'.format) #整列
    df_dianwei1_touzhu['游戏详情']=df_dianwei1_touzhu['游戏平台']+'-'+df_dianwei1_touzhu['子游戏']+',下注'+df_dianwei1_touzhu['有效投注'].astype(str)+',公司盈利'+df_dianwei1_touzhu['公司盈利'].astype(str)+',杀率'+df_dianwei1_touzhu['游戏杀率百分号'] # 新增列 游戏详情
    df_dianwei1_touzhu=df_dianwei1_touzhu.groupby(['派彩时间','会员账号']).agg({'游戏详情':'; '.join,'游戏平台':'; '.join}) # 会员账号groupby
    df_dianwei1_touzhu.reset_index(inplace=True)
    df_dianwei1_touzhu['游戏平台']=df_dianwei1_touzhu['游戏平台'].astype(str).str.split('; ').apply(set).str.join('; ')
    df_dianwei1_touzhu.rename(columns={'派彩时间':'日期'},inplace=True)

    # touzhu与玲珑 merge，获得最终表格
    df_dianwei1_top10=df_dianwei1_shuying.merge(df_dianwei1_touzhu,on=['日期','会员账号'],how='left')
    df_dianwei1_top10.sort_values(by=['日期','每日排序有效投注金额'], ascending=[True, True],inplace=True)
    return df_dianwei1_top10

def func_2sheet(df_jingli,month): #将一张表格根据月份 分成2张表格
    df_jingli_month=df_jingli[df_jingli['月份']==month]
    for i in df_jingli_month.select_dtypes(include=['int64','float64']).columns:
        df_jingli_month.rename(columns={i:str(month)+'月'+i},inplace=True)
    return df_jingli_month
def work4(df_dianwei1):  # 经理两月数据
    df_dianwei1['月份']=pd.to_datetime(df_dianwei1['日期']).dt.month
    df_dianwei1=df_dianwei1[df_dianwei1['分配日期']==min(df_dianwei1['分配日期'].dropna())]
    df_dianwei1.to_csv('river数据\\'+'营销数据经理数据.csv', encoding='utf_8_sig',index=False)  #river
    df_mingxia=df_dianwei1.groupby(['经理'])[['会员账号']].agg('nunique') # 经理和名下人数 表格
    df_mingxia.reset_index(inplace=True)
    df_mingxia.rename(columns={'会员账号':'名下人数'},inplace=True)
    # 经理 昨日数据
    df_dianwei1_zuori=df_dianwei1[df_dianwei1['日期']==max(df_dianwei1['日期'].dropna())]
    df_huiyuan_zuori=df_dianwei1_zuori.groupby(['经理','会员账号'])[['存款金额','有效投注金额','公司总盈利(代理)']].agg('sum')
    df_huiyuan_zuori.reset_index(inplace=True)
    df_huiyuan_zuori.loc[df_huiyuan_zuori['有效投注金额']>0,'投注人数']=1
    df_jingli_zuori=df_huiyuan_zuori.groupby(['经理']).agg({'投注人数':'sum','存款金额':'sum','有效投注金额':'sum','公司总盈利(代理)':'sum'})
    df_jingli_zuori.reset_index(inplace=True)

    # 经理 币种 月份 index 名下人数 投注人数 78月流水 差额 比率
    df_huiyuan=df_dianwei1.groupby(['经理','月份','会员账号'])[['存款金额','有效投注金额','公司总盈利(代理)']].agg('sum')
    df_huiyuan.reset_index(inplace=True)
    df_huiyuan.loc[df_huiyuan['有效投注金额']>0,'投注人数']=1
    df_jingli=df_huiyuan.groupby(['经理','月份']).agg({'投注人数':'sum','存款金额':'sum','有效投注金额':'sum','公司总盈利(代理)':'sum'})
    df_jingli.reset_index(inplace=True)
    # 月份拆分 然后merge 差额和比率
    df_jingli_min = func_2sheet(df_jingli,min(df_jingli['月份'])) #将一张表格根据月份 分成2张表格
    df_jingli_max = func_2sheet(df_jingli,max(df_jingli['月份'])) #将一张表格根据月份 分成2张表格
    df_jingli_2month=df_mingxia.merge(df_jingli_zuori,on='经理',how='outer').merge(df_jingli_min,on='经理',how='outer').merge(df_jingli_max,on=['经理'],how='outer')
    for i in ['存款金额','有效投注金额','公司总盈利(代理)']:
        df_jingli_2month[i+'差值']=df_jingli_2month[str(max(df_jingli['月份']))+'月'+i]-df_jingli_2month[str(min(df_jingli['月份']))+'月'+i]
        df_jingli_2month[i+'比率']=np.where(df_jingli_2month[str(min(df_jingli['月份']))+'月'+i]>0,df_jingli_2month[str(max(df_jingli['月份']))+'月'+i]/df_jingli_2month[str(min(df_jingli['月份']))+'月'+i],0)
    return df_jingli_2month

def main():
    df_dianwei1 = work_dianwei1_shuying() # 电维1会员输赢总数据
    df_dianwei1_top10 = work3(df_dianwei1)  # 每日前10
    df_jingli_2month = work4(df_dianwei1)  # 经理两月数据
    cf.func_multidf([df_dianwei1_top10,df_jingli_2month],['每日前10','月对比'],'图片数据\\'+str(max(df_dianwei1_top10['日期']))+'BTY营销数据.xlsx','noindex')

main()

