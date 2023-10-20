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


def main():
    # 读取存款
    df_cun=cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\存提数据\\充值记录')
    df_cun.drop_duplicates(subset=['充值单号'],inplace=True) # 去重复
    df_cun=df_cun[['到账时间','币种','账户名','存款商户','到账金额']]
    df_cun = df_cun[df_cun['币种']=='CNY']
    df_cun['方式']='存款'
    df_cun.rename(columns={'到账时间':'到账/出款时间','账户名':'会员账号','存款商户':'存款/出款商户','到账金额':'到账/出款金额'},inplace=True)
    df_ti=cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\存提数据\\提现订单记录')# 读取线下红利
    df_ti=df_ti[['出款时间','币种','账户名','出款商户/充值会员','出款金额' ]]
    df_ti = df_ti[df_ti['币种']=='CNY']
    df_ti['方式']='提款'
    df_ti.rename(columns={'出款时间':'到账/出款时间','账户名':'会员账号','出款商户/充值会员':'存款/出款商户','出款金额':'到账/出款金额'},inplace=True)
    df_cunti=pd.concat([df_cun,df_ti],ignore_index=True)#并表
    df_cunti['到账/出款时间']= pd.to_datetime(df_cunti['到账/出款时间']).dt.date #到账/出款时间格式
    df_cunti['存款/出款商户'].fillna('未知',inplace=True)

    # 格式
    df_cunti['到账/出款金额']=df_cunti['到账/出款金额'].astype(float)
    # index 方式 到账/出款时间 存款/出款商户 agg 人数 金额
    # index 方式 到账/出款时间 agg 人数 金额
    # merge
    df_cunti_qudao = df_cunti.groupby(['方式','到账/出款时间','存款/出款商户']).agg({'会员账号': 'nunique',  '到账/出款金额': 'sum'}) #汇总
    df_cunti_qudao.reset_index(inplace=True)
    df_cunti_qudao.rename(columns={'会员账号': '人数'},inplace=True)
    df_cunti_pingtai = df_cunti.groupby(['方式','到账/出款时间']).agg({'会员账号': 'nunique',  '到账/出款金额': 'sum'}) #汇总
    df_cunti_pingtai.reset_index(inplace=True)
    df_cunti_pingtai.rename(columns={'会员账号': '平台人数','到账/出款金额': '平台到账/出款金额'},inplace=True)
    df_cunti_daily=df_cunti_qudao.merge(df_cunti_pingtai,on=['方式','到账/出款时间'],how='left')

    df_cunti_daily=df_cunti_daily[df_cunti_daily['存款/出款商户'].isin(['C2C支付','EBPay','佳运支付'])]

    # rate 人数比例 金额比例
    df_cunti_daily['人数占比']=np.where(df_cunti_daily['平台人数']>0,df_cunti_daily['人数']/df_cunti_daily['平台人数'],0)
    df_cunti_daily['金额占比']=np.where(df_cunti_daily['平台到账/出款金额']>0,df_cunti_daily['到账/出款金额']/df_cunti_daily['平台到账/出款金额'].abs(),0)

    # 调整列顺序
    # 分表格
    df_cun_daily=df_cunti_daily[df_cunti_daily['方式']=='存款']
    df_ti_daily=df_cunti_daily[df_cunti_daily['方式']=='提款']

    df_cun_daily_pivot=df_cun_daily.pivot(index=['方式', '到账/出款时间','平台人数','平台到账/出款金额'], columns='存款/出款商户', values=['人数','人数占比','到账/出款金额','金额占比']) #透视表
    df_cun_daily_pivot.reset_index(inplace=True)
    df_ti_daily_pivot=df_ti_daily.pivot(index=['方式', '到账/出款时间','平台人数','平台到账/出款金额'], columns='存款/出款商户', values=['人数','人数占比','到账/出款金额','金额占比']) #透视表
    # 汇总人数
    df_ti_daily_pivot.reset_index(inplace=True)
    df_renshu_sum = df_cunti.groupby(['方式']).agg({'会员账号': 'nunique'}) #汇总
    df_renshu_sum.reset_index(inplace=True)
    df_renshu_sum2 = df_cunti.groupby(['方式','存款/出款商户']).agg({'会员账号': 'nunique'}) #汇总
    df_renshu_sum2.reset_index(inplace=True)
    df_renshu_sum=pd.concat([df_renshu_sum,df_renshu_sum2],ignore_index=True)
    df_renshu_sum['存款/出款商户'].fillna('平台',inplace=True) #行+列 选中列填充nan

    cf.func_multidf([df_cun_daily_pivot,df_ti_daily_pivot,df_renshu_sum],['存款','提款','汇总人数'],'图片数据\\'+str(max(df_cun_daily['到账/出款时间']))+'存提'+'.xlsx','you')

main()

