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

def work1(df_youxi): #最近2日场馆流水输赢日活变化
    df_dalei=df_youxi.groupby(['日期','币种','大类']).agg({'总有效投注': 'sum', '公司总盈利(代理)': 'sum', '游戏人数': 'sum'})  # 获得一单位表格
    df_dalei.reset_index(inplace=True)
    df_dalei['游戏平台']=df_dalei['大类']
    df_dalei=df_dalei[['日期','币种','游戏平台','总有效投注', '公司总盈利(代理)','游戏人数']] #截取所需列
    df_dalei=of.func_changguan_rate(df_dalei) # 分表合并计算变化
    df_changguan=df_youxi[['日期','币种','游戏平台','总有效投注', '公司总盈利(代理)','游戏人数']] #截取所需列
    df_changguan=of.func_changguan_rate(df_changguan) # 分表合并计算变化
    df=pd.concat([df_dalei,df_changguan],ignore_index=True)
    df=df[['币种','游戏平台','最后第2日公司总盈利(代理)','最后一日公司总盈利(代理)','公司总盈利(代理)差值','公司总盈利(代理)变化幅度','最后第2日总有效投注','最后一日总有效投注','总有效投注差值','总有效投注变化幅度','最后第2日游戏人数','最后一日游戏人数','游戏人数差值','游戏人数变化幅度','最后第2日','最后一日']]
    return df

def main():
    df_youxi=cf.func_read_filedate(None,os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\游戏输赢报表')
    print(df_youxi.head(3))
    for i in ['体育','真人','电竞','电子','捕鱼','棋牌','彩票','斗鸡']:#新增列 大类
        df_youxi.loc[df_youxi['游戏平台'].str.contains(i),'大类']=i
    # 选中CNY和VND
    df_youxi=df_youxi[df_youxi['币种'].isin(['CNY','VND'])]
    # df_youxi.to_csv('df_youxi.csv',index=False)
    # VND换算成CNY
    for df in [df_youxi]:
        for i in ['总有效投注','公司总盈利(代理)']:
            df.loc[df['币种']=='VND',i]=df.loc[df['币种']=='VND',i]/3300
    df_youxi=cf.func_shijianduan(df_youxi,['日期'],'近2日')  # 根据df的list_column_date标注数据的日期段
    df_youxi['游戏人数']=df_youxi['投注人数(公司)']+df_youxi['游戏人数(玩家对战)']

    df_changguan=work1(df_youxi) #最近2日场馆流水输赢日活变化
    df_changguan_cny=df_changguan[df_changguan['币种']=='CNY']
    df_changguan_vnd=df_changguan[df_changguan['币种']=='VND']
    cf.func_multidf([df_changguan_cny,df_changguan_vnd],['CNY数据','VND数据'],'图片数据\\'+str(max(df_youxi['日期']))+'BTY场馆数据.xlsx','noindex')



main()
