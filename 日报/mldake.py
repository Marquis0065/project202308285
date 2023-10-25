# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import common_func as cf
import _func as of
import re
import os,sys,re

# pd.set_option('display.max_colwidth', None) #显示单元格完整信息
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

sys.path.append(os.path.dirname(os.path.abspath(os.getcwd())))

def work1():# 业务1：处理输赢表格
    df_huiyuan = cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\ml会员总报表\\日报会员总报表\\同事汇总')
    df_huiyuan2=cf.func_read_filedate(None,os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\ml会员总报表\\日报会员总报表\\原始数据')# 读取+增加日期
    for df in [df_huiyuan,df_huiyuan2]: #同事表格中日期格式没有秒 原始数据带秒，处理格式不同的问题
        df.loc[df['首存时间']=='-','首存时间']=np.nan
        for i in ['注册时间','首存时间']:
            df[i]=pd.to_datetime(df[i]).dt.date
    df_huiyuan=pd.concat([df_huiyuan,df_huiyuan2],ignore_index=False)
    df_huiyuan.drop_duplicates(inplace=True)
    for i in ['充值金额','提现金额','投注金额','公司输赢']:# 删除充值、提款、投注、公司输赢四项都为0的行
        df_huiyuan.loc[df_huiyuan[i]!=0,'重要数值']=1
    df_huiyuan=df_huiyuan[df_huiyuan['重要数值']==1]
    df_huiyuan=of.func_wuxiao(df_huiyuan)  # 匹配无效会员
    df_huiyuan=df_huiyuan[df_huiyuan['无效人数']==0]  # 得到有效会员row
    df_huiyuan=df_huiyuan[['日期','会员账号','vip等级','上级代理','充值金额','有效投注','公司输赢']]
    df_huiyuan['日期']=pd.to_datetime(df_huiyuan['日期']).dt.date
    # 匹配 每日 会员 index 的红利返水
    df_honglifanshui = cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\ml交易明细\\红利返水')
    df_honglifanshui.rename(columns={'账户名':'会员账号'},inplace=True)
    df_honglifanshui['账变时间']=pd.to_datetime(df_honglifanshui['账变时间']).dt.date
    df_honglifanshui=df_honglifanshui[(df_honglifanshui['状态']=='成功')&(df_honglifanshui['交易类型'].isin(['红利','返水']))]
    df_honglifanshui=df_honglifanshui.groupby(['账变时间','会员账号','交易类型']).agg({'应到账': 'sum'}) #汇总
    df_honglifanshui.reset_index(inplace=True)
    df_honglifanshui=df_honglifanshui.pivot(index=['账变时间','会员账号'], columns='交易类型', values='应到账') #透视表
    df_honglifanshui.reset_index(inplace=True)
    df_honglifanshui.rename(columns={'账变时间':'日期','红利':'红利金额','返水':'返水金额'},inplace=True)
    df_honglifanshui=df_honglifanshui[['日期','会员账号','红利金额','返水金额']]
    df_huiyuan=df_huiyuan.merge(df_honglifanshui,on=['日期','会员账号'],how='outer') #所有红利和输赢数据

    df_dake_huiyuan=pd.DataFrame()                                   #分日期新建一个表
    for i in df_huiyuan['日期'].drop_duplicates().tolist():          #对日期去重
        df_huiyuan_child=df_huiyuan[(df_huiyuan['日期']==i)]
        df_huiyuan_child['每日公司赢利排序'] = df_huiyuan_child['公司输赢'].astype(float).rank(ascending=False)        #增加列项，对公司盈利排序
        df_huiyuan_child['每日有效投注排序'] = df_huiyuan_child['有效投注'].astype(float).rank(ascending=False)           #增加列项，对有效投注额排序
        df_huiyuan_child['每日公司输钱排序'] = df_huiyuan_child['公司输赢'].astype(float).rank(ascending=True)        #增加列项，对公司输钱排序
        df_huiyuan_child=df_huiyuan_child[(df_huiyuan_child['每日公司赢利排序']<=30)|(df_huiyuan_child['每日有效投注排序']<=30)|(df_huiyuan_child['每日公司输钱排序']<=30)]
        df_dake_huiyuan=pd.concat([df_dake_huiyuan,df_huiyuan_child],ignore_index=True)
    for i in ['每日公司赢利排序','每日有效投注排序','每日公司输钱排序']:
        df_dake_huiyuan.loc[df_dake_huiyuan[i]>30,i] = np.nan #大客名单
    df_dake_huiyuan.to_csv('river数据\\'+'ml会员排名.csv') #检查
    # df_huiyuan.to_csv('df_huiyuan.csv') #检查
    return df_dake_huiyuan,df_huiyuan

def work2(df_dake_huiyuan): #昨日输赢+注单
    df_dake_huiyuan_copy=df_dake_huiyuan.copy()
    df_huiyuan_zuori=cf.func_shijianduan(df_dake_huiyuan_copy,['日期'],'昨日')  # 昨日大客名单
    df_dake_mingdan=df_huiyuan_zuori['会员账号'].drop_duplicates().to_frame()
    # 读取注单记录
    df_dake_touzhu=of.func_touzhu_readnprocess(df_dake_mingdan,['派彩时间','会员账号','游戏平台','子游戏'],'ml大客注单记录')
    df_dake_touzhu['游戏杀率']=np.where(df_dake_touzhu['有效投注']>0,df_dake_touzhu['公司盈利']/df_dake_touzhu['有效投注'],0)# 增加游戏杀率列
    df_dake_touzhu['游戏杀率百分号']=(df_dake_touzhu['游戏杀率']).map(lambda n: '{:.2%}'.format(n))
    df_dake_touzhu.sort_values(by='公司盈利',inplace=True)  # 排序-游戏详情根据盈亏排序
    integer_columns = df_dake_touzhu.select_dtypes(include=['int64','float64']).columns #千分号
    for i in integer_columns:
        df_dake_touzhu[i]=df_dake_touzhu[i].astype(int).apply('{:,}'.format) #整列
    df_dake_touzhu['游戏详情']=df_dake_touzhu['游戏平台']+'-'+df_dake_touzhu['子游戏']+',下注'+df_dake_touzhu['有效投注'].astype(str)+',公司盈利'+df_dake_touzhu['公司盈利'].astype(str)+',杀率'+df_dake_touzhu['游戏杀率百分号'] # 新增列 游戏详情
    df_dake_touzhu=df_dake_touzhu.groupby(['派彩时间','会员账号']).agg({'游戏详情':'; '.join,'游戏平台':'; '.join}) # 会员账号groupby
    df_dake_touzhu.reset_index(inplace=True)
    df_dake_touzhu['游戏平台']=df_dake_touzhu['游戏平台'].astype(str).str.split('; ').apply(set).str.join('; ')
    df_dake_touzhu.rename(columns={'派彩时间':'日期'},inplace=True)
    # touzhu与玲珑 merge，获得最终表格
    df_dake=df_huiyuan_zuori.merge(df_dake_touzhu,on=['日期','会员账号'],how='left')
    df_dake.sort_values(by='公司输赢',ascending=False,inplace=True)
    # 计算总杀率
    df_dake['当日杀率']=(df_dake['公司输赢']/df_dake['有效投注']).map(lambda n: '{:.2%}'.format(n))
    df_dake.loc[df_dake['公司输赢']<0,'会员赢钱']=df_dake.loc[df_dake['公司输赢']<0,'公司输赢']
    df_dake.loc[df_dake['公司输赢']<0,'公司输赢']=np.nan
    # 截取 会员账号 有效投注 公司输赢 杀率 游戏详情
    df_dake = df_dake[['每日公司赢利排序','每日公司输钱排序','日期','会员账号','vip等级','上级代理','每日有效投注排序','有效投注','公司输赢','红利金额','返水金额','会员赢钱','游戏平台','游戏详情', '充值金额']]
    return df_dake

def work3(df_dake_huiyuan,df_huiyuan): #本月汇总数据
    # 名单的输赢数据
    df_dake_huiyuan=cf.func_shijianduan(df_dake_huiyuan,['日期'],'本月')  # 本月大客名单
    df_huiyuan_mingdan=df_dake_huiyuan['会员账号'].drop_duplicates().to_frame()
    df_huiyuan_yue=df_huiyuan.merge(df_huiyuan_mingdan,on='会员账号',how='right')
    df_huiyuan_yue=cf.func_shijianduan(df_huiyuan_yue,['日期'],'本月')  # 根据df的
    # vip变动和代理线变动的情况，取最新的     ,
    df_huiyuan_vip=df_huiyuan_yue[['会员账号', '日期','vip等级','上级代理']]
    df_huiyuan_vip=df_huiyuan_vip[df_huiyuan_vip['vip等级'].notnull()]
    df_huiyuan_vip.sort_values(['会员账号', '日期'], ascending=[True, True],inplace=True) # 根据会员账号 变化时间 排序
    df_huiyuan_vip.drop_duplicates(subset=['会员账号'], keep='last',inplace=True) # 会员账号去重复 保留最新的变化时间
    df_huiyuan_yue=df_huiyuan_yue.groupby(['会员账号']).agg({ '有效投注': 'sum', '公司输赢': 'sum', '红利金额': 'sum', '返水金额': 'sum'}) #汇总
    df_huiyuan_yue.reset_index(inplace=True)
    df_huiyuan_yue=df_huiyuan_yue.merge(df_huiyuan_vip,on='会员账号',how='left')
    df_huiyuan_yue['毛利']=df_huiyuan_yue['公司输赢']-df_huiyuan_yue['红利金额']-df_huiyuan_yue['返水金额'] # 毛利=公司输赢-红利-返水
    df_huiyuan_yue['盈利率']=np.where(df_huiyuan_yue['有效投注']!=0,df_huiyuan_yue['公司输赢']/df_huiyuan_yue['有效投注'].abs(),0) # ，盈利率=公司输赢/流水
    return df_huiyuan_yue

def main():
    df_dake_huiyuan,df_huiyuan= work1() # 业务1：处理输赢表格
    df_dake= work2(df_dake_huiyuan)  #昨日输赢+注单
    df_yue= work3(df_dake_huiyuan,df_huiyuan)  #本月汇总数据
    cf.func_multidf([df_dake,df_yue],['昨日','本月'],'图片数据\\'+str(max(df_dake['日期']))+'ML会员排名.xlsx','noindex')

# work1()

main()