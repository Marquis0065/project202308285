# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import os,sys,re
pd.set_option('display.max_colwidth', None) #显示单元格完整信息
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

sys.path.append(os.path.dirname(os.path.abspath(os.getcwd())))
import common_func as cf
import _func as of

def main():
    df_hongli_online=cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\交易明细\\红利')# 读取线上红利
    df_hongli_online=df_hongli_online[df_hongli_online['状态']=='成功']
    df_hongli_online.drop_duplicates(subset=['交易号'],inplace=True) # 去重复
    # 一些交易号的细分类型更改为 王者回归
    df_wzhg =cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\交易明细\\王者回归')
    df_wzhg['属于王者回归']=1
    df_hongli_online=df_hongli_online.merge(df_wzhg, on='交易号', how='left')
    df_hongli_online.loc[df_hongli_online['属于王者回归']==1, '细分类型']='王者回归'
    df_hongli_online =df_hongli_online[['账变时间','币种','账户名','细分类型','交易金额','所属代理']]
    df_hongli_online.rename(columns={'账变时间':'日期','账户名':'会员账号','细分类型':'申请备注','交易金额':'红利金额','所属代理':'上级代理'},inplace=True)
    df_hongli_online['线上线下']='线上'
    df_hongli_offline=cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\单笔审核明细')# 读取线下红利
    df_hongli_offline=df_hongli_offline[df_hongli_offline['发放状态']=='发放成功'] # “发放状态”为“发放成功”
    df_hongli_offline.drop_duplicates(subset=['审核id'],inplace=True) # 去重复
    df_hongli_offline=df_hongli_offline[['申请时间','币种','账户名','所属活动','奖品价值','所属代理' ]]
    df_hongli_offline.rename(columns={'申请时间':'日期','账户名':'会员账号','所属活动':'申请备注','奖品价值':'红利金额','所属代理':'上级代理'},inplace=True)
    df_hongli_offline['线上线下']='线下'
    df_hongli_all=pd.concat([df_hongli_online,df_hongli_offline],ignore_index=True)#并表
    df_hongli_all['日期']=pd.to_datetime(df_hongli_all['日期']).dt.date# 调整时间格式
    # 根据df的list_column_date标注数据的时间段
    df_hongli_all=cf.func_shijianduan(df_hongli_all,['日期'],'本月')
    # 处理红利记录标题
    df_hongli_all=of.func_hongli_biaoti(df_hongli_all)

    # 红利出现异常后定位问题
    # 匹配组织关系
    df_hongli_all=cf.func_zuzhi(df_hongli_all)
    # 匹配测试账号
    df_ceshi = cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\bty手工表格\\测试账号')
    df_hongli_all=df_hongli_all.merge(df_ceshi,on='会员账号',how='left')
    df_hongli_all['会员属性'].fillna('正常',inplace=True)
    # 匹配不结算会员
    df_nonjiesuan = cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\bty手工表格\\不结算会员代理')
    df_hongli_all=df_hongli_all.merge(df_nonjiesuan['不结算会员'].drop_duplicates().to_frame(),left_on='会员账号',right_on='不结算会员',how='left')
    df_hongli_all=df_hongli_all.merge(df_nonjiesuan['不结算代理'].drop_duplicates().to_frame(),left_on='上级代理',right_on='不结算代理',how='left')
    df_hongli_all.loc[(df_hongli_all['不结算会员'].notnull())&(df_hongli_all['不结算代理'].notnull()),'不结算人数']=1
    df_hongli_all.loc[(df_hongli_all['不结算人数'].isnull())&(df_hongli_all['会员属性']=='正常'),'结算非测试人数']=1

    # 只要币种CNY
    df_hongli_all=df_hongli_all[df_hongli_all['币种']=='CNY']

    # 输出
    df_hongli_all_online=df_hongli_all[df_hongli_all['线上线下']=='线上']
    df_hongli_daily_online=pd.pivot_table(df_hongli_all_online, values='红利金额', index=['线上线下','活动标题'], columns='日期', aggfunc='sum',margins=True, margins_name='总计', sort=True)#, fill_value=None,  dropna=True, observed=False
    df_hongli_daily_online.reset_index(inplace=True)
    df_hongli_daily_online_renshu=pd.pivot_table(df_hongli_all_online, values='会员账号', index=['线上线下','活动标题'], columns='日期', aggfunc='nunique',margins=True, margins_name='总计', sort=True)#, fill_value=None,  dropna=True, observed=False
    df_hongli_daily_online_renshu.reset_index(inplace=True)

    df_hongli_all_offline=df_hongli_all[df_hongli_all['线上线下']=='线下']
    df_hongli_daily_offline=pd.pivot_table(df_hongli_all_offline, values='红利金额', index=['线上线下','活动标题'], columns='日期', aggfunc='sum',margins=True, margins_name='总计', sort=True)#, fill_value=None,  dropna=True, observed=False
    df_hongli_daily_offline.reset_index(inplace=True)
    df_hongli_daily_offline_renshu=pd.pivot_table(df_hongli_all_offline, values='会员账号', index=['线上线下','活动标题'], columns='日期', aggfunc='nunique',margins=True, margins_name='总计', sort=True)#, fill_value=None,  dropna=True, observed=False
    df_hongli_daily_offline_renshu.reset_index(inplace=True)

    date_latest=max(df_hongli_all['日期'])
    cf.func_multidf([df_hongli_all_online,df_hongli_all_offline,df_hongli_daily_online,df_hongli_daily_offline,df_hongli_daily_online_renshu,df_hongli_daily_offline_renshu],['线上红利','线下红利','每日线上红利','每日线下红利','每日线上红利人数','每日线下红利人数'],'图片数据\\'+str(date_latest)+'红利'+'.xlsx','noindex')
    df_hongli_all.to_csv('river数据\\红利.csv', encoding='utf_8_sig',index=False) # river

main()


