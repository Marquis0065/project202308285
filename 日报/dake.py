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


def work1():# 业务1：处理输赢表格
    # 读取输赢报表
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
    df_shuying=df_shuying[['日期','币种','会员账号','vip','上级代理','存款金额','有效投注金额','公司总盈利(代理)','红利金额','返水金额']]

    df_ceshi = cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\bty手工表格\\测试账号')# 匹配会员属性
    df_shuying=df_shuying.merge(df_ceshi,on='会员账号',how='left')
    df_shuying=cf.func_zuzhi(df_shuying)  #匹配组织关系
    # 匹配不结算会员
    df_nonjiesuan = cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\bty手工表格\\不结算会员代理')
    df_shuying=df_shuying.merge(df_nonjiesuan['不结算会员'].drop_duplicates().to_frame(),left_on='会员账号',right_on='不结算会员',how='left')
    df_shuying=df_shuying.merge(df_nonjiesuan['不结算代理'].drop_duplicates().to_frame(),left_on='上级代理',right_on='不结算代理',how='left')
    df_shuying.loc[(df_shuying['不结算会员'].notnull())&(df_shuying['不结算代理'].notnull()),'不结算人数']=1
    df_shuying.loc[(df_shuying['不结算人数'].isnull())&(df_shuying['会员属性'].isnull()),'结算非测试人数']=1

    # 正常会员的表格-不是不结算会员，不是测试会员
    df_shuying=df_shuying[df_shuying['结算非测试人数']==1]

    df_dake_shuying=pd.DataFrame()                                   #分日期新建一个表
    for i in df_shuying['日期'].drop_duplicates().tolist():          #对日期去重
        for j in ['CNY','VND']:
            df_shuying_child=df_shuying[(df_shuying['日期']==i)&(df_shuying['币种']==j)]
            df_shuying_child['每日公司赢利排序'] = df_shuying_child['公司总盈利(代理)'].astype(float).rank(ascending=False)        #增加列项，对公司盈利排序
            df_shuying_child['每日有效投注排序'] = df_shuying_child['有效投注金额'].astype(float).rank(ascending=False)           #增加列项，对有效投注额排序
            df_shuying_child['每日公司输钱排序'] = df_shuying_child['公司总盈利(代理)'].astype(float).rank(ascending=True)        #增加列项，对公司输钱排序
            df_shuying_child=df_shuying_child[(df_shuying_child['每日公司赢利排序']<=30)|(df_shuying_child['每日有效投注排序']<=30)|(df_shuying_child['每日公司输钱排序']<=30)]
            df_dake_shuying=pd.concat([df_dake_shuying,df_shuying_child],ignore_index=True)
    for i in ['每日公司赢利排序','每日有效投注排序','每日公司输钱排序']:
        df_dake_shuying.loc[df_dake_shuying[i]>30,i] = np.nan

    # VND换算成CNY
    for df in [df_dake_shuying]:
        for i in ['存款金额','有效投注金额','公司总盈利(代理)']:
            df.loc[df['币种']=='VND',i]=df.loc[df['币种']=='VND',i]/3300
    return df_dake_shuying,df_shuying

def work2(df_dake_shuying): #昨日输赢+注单
    df_dake_shuying_copy=df_dake_shuying.copy()
    df_shuying_zuori=cf.func_shijianduan(df_dake_shuying_copy,['日期'],'昨日')  # 根据df的

    df_dake_mingdan=df_shuying_zuori['会员账号'].drop_duplicates().to_frame()

    # 读取注单记录
    df_dake_touzhu=of.func_touzhu_readnprocess(df_dake_mingdan,['派彩时间','会员账号','场馆类型','游戏平台','子游戏','币种'],'大客注单记录')
    # VND换算成CNY
    for df in [df_dake_touzhu]:
        for i in ['有效投注', '公司盈利']:
            df.loc[df['币种']=='VND',i]=df.loc[df['币种']=='VND',i]/3300
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
    df_dake=df_shuying_zuori.merge(df_dake_touzhu,on=['日期','会员账号'],how='left')
    df_dake.sort_values(by='公司总盈利(代理)',ascending=False,inplace=True)

    # 计算总杀率
    df_dake['当日杀率']=(df_dake['公司总盈利(代理)']/df_dake['有效投注金额']).map(lambda n: '{:.2%}'.format(n))
    df_dake.loc[df_dake['公司总盈利(代理)']<0,'会员赢钱']=df_dake.loc[df_dake['公司总盈利(代理)']<0,'公司总盈利(代理)']
    df_dake.loc[df_dake['公司总盈利(代理)']<0,'公司总盈利(代理)']=np.nan
    # 截取 会员账号 有效投注 公司输赢 杀率 游戏详情
    # df_dake = df_dake[['日期','会员账号','币种','上级代理','一级部门',  '二级部门','存款金额','有效投注金额','公司总盈利(代理)','当日杀率','游戏详情','游戏平台']]
    df_dake = df_dake[['每日公司赢利排序','每日公司输钱排序', '日期','币种','会员账号','vip','上级代理','一级部门','每日有效投注排序','有效投注金额','公司总盈利(代理)','会员赢钱','游戏平台','游戏详情','存款金额']]

    # 重命名表头
    # df_dake.rename(columns = {'存款金额':'当日存款','有效投注金额':'当日有效投注','公司总盈利(代理)':'当日公司输赢'}, inplace = True)
    return df_dake

def work3(df_dake_shuying,df_shuying): #本月汇总数据
    # 名单的输赢数据
    df_dake_shuying=cf.func_shijianduan(df_dake_shuying,['日期'],'本月')  # 根据df的
    df_shuying_mingdan=df_dake_shuying['会员账号'].drop_duplicates().to_frame()
    df_shuying_yue=df_shuying.merge(df_shuying_mingdan,on='会员账号',how='right')
    df_shuying_yue=cf.func_shijianduan(df_shuying_yue,['日期'],'本月')  # 根据df的
    df_shuying_yue.to_csv('river数据\\'+'BTY会员排名-月.csv') #river
    # vip变动和代理线变动的情况，取最新的     ,
    df_shuying_vip=df_shuying_yue[['会员账号', '日期','vip','上级代理','二级部门','一级部门']]
    df_shuying_vip.sort_values(['会员账号', '日期'], ascending=[True, True],inplace=True) # 根据会员账号 变化时间 排序
    df_shuying_vip.drop_duplicates(subset=['会员账号'], keep='last',inplace=True) # 会员账号去重复 保留最新的变化时间
    df_shuying_yue=df_shuying_yue.groupby(['会员账号','币种']).agg({ '有效投注金额': 'sum', '公司总盈利(代理)': 'sum', '红利金额': 'sum', '返水金额': 'sum'}) #汇总
    df_shuying_yue.reset_index(inplace=True)
    df_shuying_yue=df_shuying_yue.merge(df_shuying_vip,on='会员账号',how='left')
    return df_shuying_yue

def main():
    df_dake_shuying,df_shuying= work1() # 业务1：处理输赢表格
    df_dake= work2(df_dake_shuying)  #昨日输赢+注单
    df_dake_cny=df_dake[df_dake['币种']=='CNY']
    df_dake_vnd=df_dake[df_dake['币种']=='VND']
    df_yue= work3(df_dake_shuying,df_shuying)  #本月汇总数据
    df_yue_cny=df_yue[df_yue['币种']=='CNY']
    df_yue_vnd=df_yue[df_yue['币种']=='VND']

    cf.func_multidf([df_dake_cny,df_dake_vnd,df_yue_cny,df_yue_vnd],['昨日cny','昨日vnd','本月cny','本月vnd'],'图片数据\\'+str(max(df_dake['日期']))+'BTY会员排名.xlsx','noindex')

main()