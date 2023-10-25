# -*- coding: utf-8 -*-
import pandas as pd
import os
from datetime import datetime,timedelta
import numpy as np
import sys
import common_func as cf
import _func as of

pd.set_option('display.max_colwidth', None) #显示单元格完整信息
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

sys.path.append(os.path.dirname(os.path.abspath(os.getcwd())))

def work1(): # 注册首存表格
    df_huiyuan=cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\ml会员总报表\\注册会员总报表')# 读取+增加日期
    df_huiyuan=of.func_wuxiao(df_huiyuan)  # 匹配无效会员

    for i in ['首存时间','手机号','首存金额']:
        df_huiyuan.loc[df_huiyuan[i]=='-',i]=np.nan
    for i in ['注册时间','首存时间']:
        df_huiyuan[i]=pd.to_datetime(df_huiyuan[i]).dt.date
    df_huiyuan['手机号长度']=df_huiyuan['手机号'].str.len()
    df_huiyuan.loc[df_huiyuan['手机号长度']==11,'绑定手机号人数']=1  #非11位手机号不计算
    df_huiyuan.to_csv('river数据\\'+'ml注册首存.csv',index=False, encoding='utf_8_sig') #river
    df_huiyuan=cf.func_shijianduan(df_huiyuan,['注册时间','首存时间'],'本月日报')  # 根据df的list_column_date标注数据的时间段
    df_huiyuan.loc[df_huiyuan['首存时间']>df_huiyuan['结束日期'],'首存时间']=np.nan
    df_huiyuan.loc[df_huiyuan['首存时间'].notnull(),'首存人数']=1 #首存人数
    df_huiyuan.loc[df_huiyuan['注册时间']==df_huiyuan['首存时间'],'注册当天首存人数']=1 #注册当天首存人数
    df_huiyuan.loc[(df_huiyuan['首存时间'].notnull())&(df_huiyuan['绑定手机号人数']==1),'绑定并首存人数']=1 #绑定并首存人数

    df_huiyuan.to_csv('ml.csv')

    # 输出
    df_huiyuan_daily=of.func_huiyuan_rate(df_huiyuan,['开始日期','结束日期'])  #会员报表：汇总+计算比率
    df_huiyuan_daily_daili=of.func_huiyuan_rate(df_huiyuan,['开始日期','结束日期','上级代理'])  #会员报表：汇总+计算比率
    cf.func_multidf([df_huiyuan_daily,df_huiyuan_daily_daili],['每日数据','代理数据'],'图片数据\\'+str(max(df_huiyuan['注册时间']))+'ML当月注册首存.xlsx','noindex')
    return

# （第二部分公式参考源数据bty1）
import re
def work2(): #日报
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
    df_huiyuan=of.func_ml_ribao_jisuan(df_huiyuan)  #会员总报表处理和计算非比率

    # 按照river要求输出
    print(len(df_huiyuan))
    df_huiyuan_river=df_huiyuan[['会员账号','上级代理','登陆天数','vip等级','最高vip等级','等级状态','会员等级调整时间','剩余成长值','客户端','手机号','注册IP','注册域名','注册时间','最后登陆时间','首存时间','首存金额','最后充值日期','充值金额','提现金额','投注金额','有效投注','公司输赢','红利金额','返水金额','日期','无效人数','活跃人数','存款人数','投注人数','存提差']]
    df_huiyuan_river['月份'] =pd.to_datetime(df_huiyuan_river['日期']).dt.month
    df_huiyuan_river.fillna(0,inplace=True)
    df_huiyuan_benyue=df_huiyuan_river[df_huiyuan_river['月份']==max(df_huiyuan_river['月份'])]
    df_huiyuan_benyue.to_csv('river数据\\'+'ml日报-本月.csv',index=False, encoding='utf_8_sig')
    #river
    df_huiyuan_benyue_sum=df_huiyuan_benyue.groupby(['会员账号','上级代理'])[['活跃人数','存款人数','充值金额','提现金额','投注人数','有效投注','公司输赢','无效人数']].agg('sum') #汇总
    df_huiyuan_benyue_sum.reset_index(inplace=True)
    for i in ['活跃人数','存款人数','无效人数','投注人数']:
        df_huiyuan_benyue_sum[i].fillna(0,inplace=True)
        df_huiyuan_benyue_sum.loc[df_huiyuan_benyue_sum[i]>0,i]=1
    df_huiyuan_benyue_sum=df_huiyuan_benyue_sum[['会员账号','上级代理','活跃人数','存款人数','充值金额','提现金额','投注人数','有效投注','公司输赢','无效人数']]
    df_huiyuan_benyue_sum.to_csv('river数据\\ML日报【会员汇总】.csv', encoding='utf_8_sig',index=False) #river

    df_huiyuan=cf.func_shijianduan(df_huiyuan,['日期'],'本月日报')  # 根据df的list_column_date标注数据的时间段
    df_huiyuan_daily_wuxiao=of.func_ml_ribao_rate(df_huiyuan,['日期','无效人数']) #ml日报：汇总+计算比率
    df_huiyuan_daily_vip=of.func_ml_ribao_rate(df_huiyuan,['日期','无效人数','vip等级']) #ml日报：汇总+计算比率

    cf.func_multidf([df_huiyuan_daily_wuxiao,df_huiyuan_daily_vip],['每日有效无效数据','每日vip数据'],'图片数据\\'+str(max(df_huiyuan['日期']))+'ML当月平台数据.xlsx','noindex')

    # # excel生成文本

def main():
    work1()
    work2()

main()

# work2()


