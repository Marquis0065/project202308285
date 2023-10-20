# -*- coding: utf-8 -*-
import pandas as pd
import os
from datetime import datetime,timedelta
import numpy as np
pd.set_option('display.max_colwidth', None) #显示单元格完整信息
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import sys
sys.path.append(os.path.dirname(os.path.abspath(os.getcwd())))
import common_func as cf
import _func as of

# 该脚本用于每日更新 测试账号 组织关系
def main():
    df_huiyuan = cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\会员列表')
    df_huiyuan.drop_duplicates(subset=['会员账号'],inplace=True) #去重复 也可全表去重复
    # 更新组织关系
    df_huiyuan.rename(columns={'代理': '上级代理'}, inplace=True)
    df_daili_mingdan=df_huiyuan['上级代理'].drop_duplicates().to_frame()# 筛选出代理名单
    df_daili=cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\代理列表') # 匹配 代理列表 得到上级代理2
    df_daili=df_daili[['代理账号','代理']]
    df_daili.rename(columns={'代理账号':'上级代理','代理':'上级代理2'},inplace=True)
    df_daili_mingdan=df_daili_mingdan.merge(df_daili,on='上级代理',how='left')
    df_daili.rename(columns={'上级代理':'上级代理1'},inplace=True)
    for i in [2,3,4,5,6]:
        df_daili.rename(columns={'上级代理'+str(i-1):'上级代理'+str(i),'上级代理'+str(i):'上级代理'+str(i+1)},inplace=True) # 上级代理2 匹配代理列表 得到上级代理3
        df_daili_mingdan=df_daili_mingdan.merge(df_daili,on='上级代理'+str(i),how='left')
    # df_daili_mingdan.to_csv('df_daili_mingdan.csv')  #检查用
    df_daili_mingdan.loc[(df_daili_mingdan['上级代理2']=='admin'),'小组']=df_daili_mingdan.loc[(df_daili_mingdan['上级代理2']=='admin'),'上级代理']#上级代理2是admin 那么上级代理是 小组
    for i in [3,4,5,6,7]: #上级代理3是admin 那么上级代理2是 小组
        df_daili_mingdan.loc[(df_daili_mingdan['上级代理'+str(i)]=='admin'),'小组']=df_daili_mingdan.loc[(df_daili_mingdan['上级代理'+str(i)]=='admin'),'上级代理'+str(i-1)]# 上级代理4 notnull 得到一级部门 上级代理3得到小组
    df_daili_mingdan = df_daili_mingdan.dropna(subset=['上级代理'])
    df_daili_mingdan.loc[df_daili_mingdan['小组'].isnull(),'小组']=df_daili_mingdan.loc[df_daili_mingdan['小组'].isnull(),'上级代理'] #小组空填充上级代理 比如admin 比如qqty
    df_daili_mingdan=df_daili_mingdan[['上级代理','小组']]  #匹配 同事代理线 得到完整组织关系
    df_yiji=cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\bty手工表格\\同事代理线')
    df_daili_mingdan=df_daili_mingdan.merge(df_yiji,left_on='上级代理',right_on='上级代理或小组',how='left')
    df_daili_mingdan=df_daili_mingdan[['上级代理','小组','二级部门','一级部门']]
    df_daili_mingdan2=df_daili_mingdan[df_daili_mingdan['一级部门'].isnull()][['上级代理','小组']]
    df_yiji2=df_yiji[['二级部门','一级部门']].drop_duplicates()
    df_daili_mingdan2=df_daili_mingdan2.merge(df_yiji2,left_on='小组',right_on='二级部门',how='left')
    df_daili_mingdan2=df_daili_mingdan2[['上级代理','小组','二级部门','一级部门']]
    df_daili_mingdan2.loc[(df_daili_mingdan2['二级部门'].isnull())&(df_daili_mingdan2['小组'].str.contains('wbdl',case=False)),['二级部门','一级部门']] =['wbdl','外代']#未在同事代理线匹配到，小组 有 wbdl
    df_daili_mingdan2.loc[(df_daili_mingdan2['二级部门'].isnull()),['二级部门','一级部门']] =['未知','未知'] #剩余的标注为未知
    df_daili_mingdan2.loc[df_daili_mingdan2.duplicated(subset=['上级代理'], keep=False), '一级部门'] = '未知' #上级代理重复的 一级部门不同情况 一级部门标为未知
    df_daili_mingdan2.drop_duplicates(inplace=True)
    df_daili_mingdan=pd.concat([df_daili_mingdan,df_daili_mingdan2],ignore_index=True)
    df_daili_mingdan=df_daili_mingdan.dropna(subset=['一级部门'])
    df_daili_mingdan.to_csv(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\bty手工表格\\组织关系\\daili.csv',index=False,encoding='utf-8')
    df_huiyuan=cf.func_zuzhi(df_huiyuan) #匹配组织关系
    df_huiyuan_nonyiji=df_huiyuan[df_huiyuan['一级部门']=='空白'] #核对有无空白一级部门
    cf.func_multidf([df_huiyuan_nonyiji,df_daili_mingdan2],['空白一级部门数据','新代理数据'],'核对-一级.xlsx','noindex')
    # 规则判定 会员属性 测试/正常
    df_ceshi2 = cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\bty手工表格\\测试账号')# 读取同事测试账号名单
    df_huiyuan=df_huiyuan.merge(df_ceshi2,on='会员账号',how='left')
    for i in ['会员账号','姓名','玩家层级','备注']:
        df_huiyuan[i].fillna('脚本填充',inplace=True) #contains不能空
        for j in ['测试','ceshi','test']:
            df_huiyuan.loc[df_huiyuan[i].str.contains(j,case=False),'会员属性']='测试'
    df_huiyuan=df_huiyuan[df_huiyuan['会员账号']!='脚本填充']
    df_huiyuan = df_huiyuan.replace(('脚本填充'), np.nan,regex=True) # 小写与去除符号
    df_huiyuan['会员属性'].fillna('正常',inplace=True)
    # 测试名单
    df_huiyuan_test=df_huiyuan[df_huiyuan['会员属性']=='测试']
    df_ceshi=df_huiyuan_test[['会员账号','会员属性']]
    cf.func_multidf([df_huiyuan_test,df_ceshi],['测试','测试名单'],'river数据\\测试-完整&名单.xlsx','noindex')
    df_ceshi.to_csv(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\bty手工表格\\测试账号\\ceshi.csv',index=False)

main()

