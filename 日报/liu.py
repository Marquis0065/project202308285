# -*- coding: utf-8 -*-
import pandas as pd
import os
from datetime import datetime,timedelta
import numpy as np
import sys
import common_func as cf
import _func as of
import re
import liucun_func as lf

sys.path.append(os.path.dirname(os.path.abspath(os.getcwd())))

def work1():  # 制作留存率
    # 交易明细-充值代充
    df_jiaoyi=cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\交易明细\\充值代充') # 读取交易明细
    df_jiaoyi_1=df_jiaoyi[(df_jiaoyi['交易类型']=='代充')&(df_jiaoyi['细分类型']=='代充')] # 合并 两种交易类型
    df_jiaoyi_2=df_jiaoyi[(df_jiaoyi['交易类型']=='充值')]
    df_jiaoyi=pd.concat([df_jiaoyi_1,df_jiaoyi_2],ignore_index=True)
    df_jiaoyi=df_jiaoyi[df_jiaoyi['状态']=='成功']
    df_jiaoyi.rename(columns={'账变时间':'最后行为日期','账户名':'会员账号','交易金额':'充值代充金额'},inplace=True)  # 自然日数据
    df_jiaoyi['最后行为日期']=pd.to_datetime(df_jiaoyi['最后行为日期']).dt.date
    df_jiaoyi=df_jiaoyi.groupby(['最后行为日期','会员账号','币种']).agg({'充值代充金额': 'sum'}) #汇总
    df_jiaoyi.reset_index(inplace=True) # 汇总 最后行为日期 会员账号 index 交易金额 sum
    # 输赢报表
    df_shuying=cf.func_read_folderdate(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\会员输赢报表\\原始数据')# 读取+增加日期
    for i in ['存款金额','提款金额','平台坐庄-投注金额','平台坐庄-下注金额','平台坐庄-派彩金额','平台坐庄-公司输赢','玩家对战-下投注额','玩家对战-玩家输赢','玩家对战-公司抽水','公司总盈利(代理)','红利金额','返水金额','投注次数','有效投注金额']:
        df_shuying.loc[df_shuying[i]!=0,'重要数值']=1
    df_shuying=df_shuying[df_shuying['重要数值']==1]
    for i in ['首存人数','首存金额','存款人数','取款人数','加币','减币','存款手续费','提款手续费','上分总额','上分次数','用户类型']:
        df_shuying.drop(i, axis=1, inplace=True)#drop操作 列
    df_shuying2= cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\会员输赢报表\\同事汇总') #读取同事处理过的输赢报表
    df_shuying=pd.concat([df_shuying,df_shuying2],ignore_index=True)
    df_shuying.drop_duplicates(inplace=True)
    df_shuying.rename(columns={'日期': '最后行为日期','账户名': '会员账号','币种':'输赢币种'}, inplace=True)#列 更改名称
    df_shuying['最后行为日期']=pd.to_datetime(df_shuying['最后行为日期']).dt.date
    df_shuying=df_shuying[['最后行为日期','会员账号','有效投注金额','输赢币种','存款金额','提款金额','平台坐庄-公司输赢']]
    # 首存报表
    df_shoucun=cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\会员首存报表')    # 读取首存 表格
    df_shoucun.drop_duplicates(subset=['会员名'],inplace=True) #去重复 也可全表去重复
    df_shoucun=df_shoucun[['会员名','交易时间','所属代理']] # 获得 首存时间 和 会员账号
    df_shoucun.rename(columns={'会员名': '会员账号','交易时间': '首存时间','所属代理':'上级代理'},inplace=True)
    df_shoucun['首存时间']=pd.to_datetime(df_shoucun['首存时间']).dt.date
    # 首存报表匹配测试账号，去除测试账号
    df_ceshi=cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\bty手工表格\\测试账号')    # 读取首存 表格
    df_shoucun=df_shoucun.merge(df_ceshi,on='会员账号',how='left')  # 匹配会员属性
    df_shoucun_nontest=df_shoucun[df_shoucun['会员属性'].isnull()]
    # 交易明细 输赢报表 得到 最后行为日期
    df_liucun=df_jiaoyi.merge(df_shuying,on=['最后行为日期','会员账号'],how='outer').merge(df_shoucun_nontest,on='会员账号',how='outer')
    # 匹配会员列表
    # df_huiyuan=cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\会员列表最新')
    # df_huiyuan=df_huiyuan[['会员账号','状态']]
    # df_liucun=df_liucun.merge(df_huiyuan,on='会员账号',how='left')
    # df_liucun=df_liucun[df_liucun['状态']=='正常']

    # 数据处理
    for i in df_liucun.select_dtypes(include=['int64','float64']).columns:
        df_liucun[i].fillna(0,inplace=True)

    df_liucun=cf.func_shijianduan(df_liucun,['最后行为日期'],'近30日')  # 根据df的list_column_date选取数据的时间段
    df_liucun=df_liucun[(df_liucun['首存时间']>=df_liucun['开始日期'])&(df_liucun['首存时间']<=df_liucun['结束日期'])]  # 首存时间也需要满足
    df_liucun=cf.func_zuzhi(df_liucun)  #匹配组织关系
    df_liucun.loc[df_liucun['币种'].isnull(),'币种']=df_liucun.loc[df_liucun['币种'].isnull(),'输赢币种'] #列调整
    df_liucun.loc[df_liucun['充值代充金额']==0,'充值代充金额']=df_liucun.loc[df_liucun['充值代充金额']==0,'存款金额']
    df_liucun=lf.func_liucun_jisuan(df_liucun)# 新增列 有效性为 第几日 n日留存

    df_liucun.to_csv('river数据\\'+'留存.csv',index=False,encoding='utf_8_sig') #river

    # 选择CNY和VND
    df_liucun=df_liucun[df_liucun['币种'].isin(['CNY','VND'])]
    df_shijian_bz = lf.func_liucun_shijian(df_liucun,'币种','一级部门') #制作bz首存时间留存率
    df_shijian_pingtai = lf.func_liucun_shijian(df_liucun,'币种',None)

    # 制作汇总留存率
    df_liucun_cny=df_liucun[df_liucun['币种'].isin(['CNY'])]
    df_daili=lf.func_liucun_daili(df_liucun_cny)
    # # df_erji = lf.func_liucun_bumen(df_daili,'一级部门','二级部门',None)
    df_yiji= lf.func_liucun_bumen(df_daili,'一级部门',None,None)
    # df_liucun_vnd=df_liucun[df_liucun['币种'].isin(['VND'])]

    # cf.func_multidf([df_yiji,df_erji,df_daili,df_shijian_pingtai,df_shijian_bz,],['一级部门数据','二级部门数据','代理数据','平台每日数据','币种每日数据'],str(max(df_liucun['最后行为日期']))+'近30日首存留存BTY【CNY&VND】.xlsx','noindex')
    cf.func_multidf([df_shijian_pingtai,df_shijian_bz,df_yiji],['币种每日数据','一级部门每日数据','一级汇总'],'图片数据\\'+str(max(df_liucun['最后行为日期']))+'BTY近30日首存留存【CNY&VND】.xlsx','noindex')
    return df_liucun

def work2(df_liucun): #一次性
    # 代理
    # VND换算成CNY
    for df in [df_liucun]:
        for i in ['充值代充金额','提款金额','有效投注金额','平台坐庄-公司输赢']:
            df.loc[df['币种']=='VND',i]=df.loc[df['币种']=='VND',i]/3300
    df_liucun.loc[df_liucun['有效投注金额']>0,'有效投注天数']=1

    df_liucun_huiyuan=df_liucun.groupby(['一级部门','二级部门','上级代理','会员账号','币种','首存时间']).agg({'充值代充金额': 'sum', '提款金额': 'sum', '有效投注金额': 'sum', '平台坐庄-公司输赢': 'sum', '有效投注天数': 'sum','有效行为天数': 'sum'}) #汇总
    df_liucun_huiyuan.reset_index(inplace=True)
    # 一次性会员人数、存款低于百元会员人数、小额投注人数
    df_liucun_huiyuan.loc[(df_liucun_huiyuan['有效投注天数']==1)&(df_liucun_huiyuan['首存时间']<=max(df_liucun_huiyuan['首存时间'])-timedelta(days=2)),'一次性会员人数']=1
    df_liucun_huiyuan.loc[(df_liucun_huiyuan['充值代充金额']<100),'存款低于百元会员人数']=1
    df_liucun_huiyuan.loc[(df_liucun_huiyuan['有效投注金额']<100),'流水低于百元会员人数']=1
    df_liucun_huiyuan['存提差']=df_liucun_huiyuan['充值代充金额']-df_liucun_huiyuan['提款金额']

    for i in ['充值代充金额', '提款金额', '有效投注金额', '平台坐庄-公司输赢', '有效行为天数','存提差']:
        for j in ['一次性会员人数','存款低于百元会员人数','流水低于百元会员人数']:
            df_liucun_huiyuan.loc[(df_liucun_huiyuan[j]==1),j[:-2]+i]=df_liucun_huiyuan.loc[(df_liucun_huiyuan[j]==1),i]

    df_liucun_huiyuan.to_csv('river数据\\'+'一次性.csv',index=False,encoding='utf_8_sig') #river

    df_ycx_bz=lf.func_ycx_rate(df_liucun_huiyuan,'币种')  #一次性报表计算
    # df_ycx_daili=lf.func_ycx_rate(df_liucun_huiyuan,'上级代理')  #一次性报表计算
    # df_ycx_erji=lf.func_ycx_rate(df_liucun_huiyuan,'二级部门')  #一次性报表计算
    # df_ycx_yiji=lf.func_ycx_rate(df_liucun_huiyuan,'一级部门')  #一次性报表计算

    # cf.func_multidf([df_ycx_yiji,df_ycx_erji,df_ycx_daili],['一级部门数据','二级部门数据','代理数据'],str(max(df_liucun_huiyuan['首存时间']))+'近30日一次性BTY【CNY&VND】.xlsx','noindex')
    cf.func_multidf([df_ycx_bz],['币种数据'],'图片数据\\'+str(max(df_liucun_huiyuan['首存时间']))+'BTY近30日一次性【CNY&VND】.xlsx','noindex')


def work3(): #制作流失
    #注册首存常规操作
    df_ceshi,df_huiyuan=of.func_huiyuan_shoucun()  #合并会员和首存,加上时间段
    df_huiyuan=cf.func_zuzhi(df_huiyuan)  #匹配组织关系
    df_huiyuan_nonyiji=df_huiyuan[df_huiyuan['一级部门']=='空白']
    # 输出测试，和一级部门为空白的数据
    cf.func_multidf([df_ceshi,df_huiyuan_nonyiji],['测试账号','一级部门数据'],'脚本数据-测试一级.xlsx','noindex')
    # 输赢报表常规操作
    df_shuying=cf.func_read_shuying('会员输赢报表')# 读取+增加日期
    df_shuying=of.func_shuying_jisuan(df_shuying)  #输赢表格处理和计算非比率

    ############################# 还在做 ##########################
    # df_shuying=
    df_huiyuan=df_huiyuan.merge()# 匹配活跃人数
    df_huiyuan = of.func_liushi(df_huiyuan)  # 会员流失计算


    print(len(df_shuying))
    # df_shuying.to_excel('ceshi.xlsx',index=False,freeze_panes=(1,2)) # 输出检查

    # 选取
    df_liu=df_shuying[(df_shuying['满足流失留存注册时间的人数']==1)&(df_shuying['满足流失留存首存时间的人数']==1)&(df_shuying['投注次数不为0']==1)]

    # 输出 每日index和每日币种index
    df_daily=df_liu.groupby(['日期']).agg({'会员账号': 'nunique', '未存款流失人数': 'sum', '首存流失人数': 'sum','首存人数': 'sum'}) #汇总
    df_daily.rename(columns={'会员账号': '注册人数'},inplace=True)
    df_daily.reset_index(inplace=True)

    df_daily_bz=df_liu.groupby(['日期','币种']).agg({'会员账号': 'nunique', '未存款流失人数': 'sum', '首存流失人数': 'sum','首存人数': 'sum'}) #汇总
    df_daily_bz.rename(columns={'会员账号': '注册人数'},inplace=True)
    df_daily_bz.reset_index(inplace=True)

def main():
    df_liucun=work1()
    work2(df_liucun)

main()




