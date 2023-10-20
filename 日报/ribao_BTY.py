# -*- coding: utf-8 -*-
import pandas as pd
import os
from datetime import datetime,timedelta
import numpy as np
import common_func as cf
import _func as of
from langdetect import detect
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.getcwd())))

pd.set_option('display.max_colwidth', None) #显示单元格完整信息
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def func_detect_lan(x):
    try:
        return detect(x)
    except:
        return 'error'
# 注册首存表格
def work1():
    #读取会员列表
    df_huiyuan = cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\会员列表')
    df_huiyuan.drop_duplicates(subset=['会员账号'],inplace=True) # 会员账号去重复
    df_huiyuan.drop('币种', axis=1, inplace=True) # 会员列表的币种 不正确
    # 匹配组织关系
    df_huiyuan=cf.func_zuzhi(df_huiyuan)
    # 匹配测试账号
    df_ceshi = cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\bty手工表格\\测试账号')
    df_huiyuan=df_huiyuan.merge(df_ceshi,on='会员账号',how='left')
    df_huiyuan['会员属性'].fillna('正常',inplace=True)
    # 匹配首存报表
    df_shoucun=cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\会员首存报表')
    df_shoucun.to_csv('river数据\\历史首存.csv', encoding='utf_8_sig',index=False) # river
    df_shoucun=df_shoucun[['会员名','交易时间','金额','币种']]
    df_shoucun.rename(columns={'会员名': '会员账号','交易时间': '首存时间','金额': '首存金额','币种': '首存币种'},inplace=True)
    df_huiyuan=df_huiyuan.merge(df_shoucun,on=['会员账号'],how='left')
    # 币种换算 首存usdt换算cny
    for df in [df_huiyuan]:
        for i in ['首存金额']:
            df.loc[df['首存币种']=='USDT',i]=df.loc[df['首存币种']=='USDT',i]*7
    # 非测试数据带首存
    df_huiyuan=df_huiyuan[df_huiyuan['会员属性']=='正常']
    # 会员归属地筛选
    # 第一步粗筛
    # # 处理手机号码
    df_huiyuan['手机号码'] = df_huiyuan['手机号码'].replace((' '), '',regex=True) # 小写与去除符号
    df_huiyuan['手机号码'] = df_huiyuan['手机号码'].astype(str).str.split('.').str[0]
    df_huiyuan['手机号码'] = df_huiyuan['手机号码'].replace(('nan'), '',regex=True) # 小写与去除符号
    df_huiyuan['手机号长度']=df_huiyuan['手机号码'].str.len()
    df_huiyuan.loc[df_huiyuan['一级部门'].str.contains('-越'),'国家']='越南'# 代理线（手机号）
    df_huiyuan.loc[(df_huiyuan['一级部门'].str.contains('-越'))&(df_huiyuan['手机号长度']==11),'国家']='中国'
    for (i,j) in zip(['CNY','VND','MYR','THB','MXN','BRL','USD','EGP'],['中国','越南','马来西亚','泰国','墨西哥','巴西','日本','埃及']):     # 首存币种
        df_huiyuan.loc[df_huiyuan['首存币种']==i,'国家']=j
        # 第二步 精筛无首存币种/USDT 手机号长度和姓名
    df_huiyuan.loc[df_huiyuan['首存币种'].isin([np.nan,'USDT'])&(df_huiyuan['手机号长度']==11),'国家']='中国' # 电话号码位数 确定中国
    df_huiyuan2=df_huiyuan[df_huiyuan['首存币种'].isin([np.nan,'USDT'])&(df_huiyuan['国家']!='中国')&(df_huiyuan['姓名'].notnull())].sort_values(by='姓名',ascending=True).tail(10000) #非中国姓名 筛选中国 泰国
    print(datetime.now().strftime('%H:%M:%S'),'开始识别姓名字体')
    df_huiyuan2['姓名字体']=df_huiyuan2['姓名'].astype(str).apply(lambda x: func_detect_lan(x))
    print(datetime.now().strftime('%H:%M:%S'),'结束识别姓名字体')
    # df_huiyuan2.to_csv('df_huiyuan2.csv')
    df_huiyuan2=df_huiyuan2[['会员账号','姓名字体']]
    df_huiyuan=df_huiyuan.merge(df_huiyuan2,on='会员账号',how='left')
    df_huiyuan.loc[df_huiyuan['姓名字体'].isin(['ko','zh-cn','zh-tw']),'国家']='中国'
    df_huiyuan.loc[df_huiyuan['姓名字体']=='th','国家']='泰国'
    #river数据 输出 中国区 越南区  泰国  巴西    其他国家
    for i in ['注册时间','首存时间']:
        df_huiyuan[i]=pd.to_datetime(df_huiyuan[i]).dt.date
    df_huiyuan_2022=df_huiyuan[(df_huiyuan['注册时间']<pd.to_datetime('2023-1-1').date())&(df_huiyuan['国家']=='中国')] # 2022中国
    df_huiyuan_2023=df_huiyuan[(df_huiyuan['注册时间']>=pd.to_datetime('2023-1-1').date())&(df_huiyuan['国家']=='中国')] # 2023中国
    df_huiyuan_vi=df_huiyuan[(df_huiyuan['国家']=='越南')]  # 越南
    df_huiyuan_th=df_huiyuan[(df_huiyuan['国家']=='泰国')]  # 泰国
    df_huiyuan_brl=df_huiyuan[(df_huiyuan['国家']=='巴西')]  # 巴西
    df_huiyuan_other=df_huiyuan[(~df_huiyuan['国家'].isin(['中国','越南','泰国','巴西']))]  # 其他国家
    df_huiyuan_2022.to_csv('river数据\\注册-中国2022.csv', encoding='utf-8',index=False)
    df_huiyuan_2023.to_csv('river数据\\注册-中国2023.csv',  encoding='utf-8',index=False)
    df_huiyuan_vi.to_csv('river数据\\注册-越南.csv',  encoding='utf-8',index=False)
    cf.func_multidf([df_huiyuan_th,df_huiyuan_brl,df_huiyuan_other],['泰国','巴西','其他国家'],'river数据\\注册-泰国巴西其他.xlsx','noindex')
    # 根据df的list_column_date标注数据的时间段
    df_huiyuan=cf.func_shijianduan(df_huiyuan,['注册时间','首存时间'],'本月日报')
    # 注册首存计算
    df_huiyuan.loc[df_huiyuan['首存时间']>df_huiyuan['结束日期'],'首存时间']=np.nan
    df_huiyuan.loc[df_huiyuan['首存时间'].notnull(),'首存人数']=1 #首存人数
    df_huiyuan.loc[df_huiyuan['注册时间']==df_huiyuan['首存时间'],'注册当天首存人数']=1 #注册当天首存人数
    df_huiyuan.loc[df_huiyuan['手机号码'].notnull(),'绑定手机号人数']=1
    df_huiyuan.loc[(df_huiyuan['首存时间'].notnull())&(df_huiyuan['手机号码'].notnull()),'绑定并首存人数']=1 #绑定并首存人数
    df_huiyuan.drop_duplicates(subset=['会员账号'],inplace=True) #去重复 也可全表去重复
    #river
    df_huiyuan.to_csv('river数据\\BTY注册首存-本月.csv',encoding='utf_8_sig',index=False)
    #会员报表：汇总+计算比率
    df_huiyuan_daily_bz=of.func_huiyuan_rate(df_huiyuan,['开始日期','结束日期','国家'])
    df_huiyuan_daily_bzyiji=of.func_huiyuan_rate(df_huiyuan,['开始日期','结束日期','国家','一级部门','二级部门','小组','上级代理'])  #会员报表：汇总+计算比率

    cf.func_multidf([df_huiyuan_daily_bz,df_huiyuan_daily_bzyiji],['国家数据','代理数据'],'图片数据\\'+str(max(df_huiyuan['注册时间']))+'BTY当月注册首存.xlsx','noindex')

import re
def work2(): #日报
    # 读取输赢
    df_shuying=cf.func_read_folderdate(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\会员输赢报表\\原始数据')# 读取+增加日期
    for i in ['存款金额','提款金额','平台坐庄-投注金额','平台坐庄-下注金额','平台坐庄-派彩金额','平台坐庄-公司输赢','玩家对战-下投注额','玩家对战-玩家输赢','玩家对战-公司抽水','公司总盈利(代理)','红利金额','返水金额','投注次数','有效投注金额']:
        df_shuying.loc[df_shuying[i]!=0,'重要数值']=1
    df_shuying=df_shuying[df_shuying['重要数值']==1]
    for i in ['首存人数','首存金额','存款人数','取款人数','加币','减币','存款手续费','提款手续费','上分总额','上分次数','用户类型']:
        df_shuying.drop(i, axis=1, inplace=True)#drop操作 列
    df_shuying2= cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\会员输赢报表\\同事汇总') #读取同事处理过的输赢报表
    df_shuying=pd.concat([df_shuying,df_shuying2],ignore_index=True)
    df_shuying.drop_duplicates(inplace=True)
    # 根据df的list_column_date标注数据的时间段
    df_shuying=cf.func_shijianduan(df_shuying,['日期'],'本月日报')
    #输赢表格处理和计算非比率
    df_shuying=of.func_shuying_jisuan(df_shuying)
    # 匹配组织关系
    df_shuying=cf.func_zuzhi(df_shuying)
    # 匹配测试账号
    df_ceshi = cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\bty手工表格\\测试账号')
    df_shuying=df_shuying.merge(df_ceshi,on='会员账号',how='left')
    df_shuying['会员属性'].fillna('正常',inplace=True)
    # 匹配不结算会员
    df_nonjiesuan = cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\bty手工表格\\不结算会员代理')
    df_shuying=df_shuying.merge(df_nonjiesuan['不结算会员'].drop_duplicates().to_frame(),left_on='会员账号',right_on='不结算会员',how='left')
    df_shuying=df_shuying.merge(df_nonjiesuan['不结算代理'].drop_duplicates().to_frame(),left_on='上级代理',right_on='不结算代理',how='left')
    df_shuying.loc[(df_shuying['不结算会员'].notnull())&(df_shuying['不结算代理'].notnull()),'不结算人数']=1
    df_shuying.loc[(df_shuying['不结算人数'].isnull())&(df_shuying['会员属性']=='正常'),'结算非测试人数']=1
    # 按照river要求输出
    print(len(df_shuying))
    df_shuying_river=df_shuying[['会员账号','币种','日期','上级代理','vip','存款金额','提款金额','平台坐庄-投注金额','平台坐庄-下注金额','平台坐庄-派彩金额','平台坐庄-公司输赢','玩家对战-下投注额','玩家对战-玩家输赢','玩家对战-公司抽水','公司总盈利(代理)','红利金额','返水金额','投注次数','有效投注金额','会员属性','二级部门','活跃人数','一级部门','不结算人数','重要数值','开始日期','结束日期','存款人数','投注人数','存提差','毛利','小组','不结算会员','不结算代理','结算非测试人数']]
    df_shuying_river['月份'] =pd.to_datetime(df_shuying_river['日期']).dt.month
    df_shuying_river.fillna(0,inplace=True)
    df_shuying_benyue=df_shuying_river[df_shuying_river['月份']==max(df_shuying_river['月份'])]
    df_shuying_benyue[df_shuying_benyue['币种']=='CNY'].to_csv('river数据\\BTY日报【CNY】.csv', encoding='utf_8_sig',index=False) #river
    df_shuying_benyue[df_shuying_benyue['币种']=='VND'].to_csv('river数据\\BTY日报【VND】.csv', encoding='utf_8_sig',index=False) #river
    df_shuying_benyue[df_shuying_benyue['币种']=='USDT'].to_csv('river数据\\BTY日报【USDT】.csv', encoding='utf_8_sig',index=False) #river
    df_shuying_benyue[~(df_shuying_benyue['币种'].isin(['CNY','VND','USDT']))].to_csv('river数据\\BTY日报【其他】.csv', encoding='utf_8_sig',index=False) #river
    df_shuying_benyue_sum=df_shuying_benyue.groupby(['会员账号','币种','上级代理','会员属性','二级部门','一级部门','不结算人数'])[['存款金额','提款金额','平台坐庄-投注金额','平台坐庄-下注金额','平台坐庄-派彩金额','平台坐庄-公司输赢','玩家对战-玩家输赢','玩家对战-下投注额','玩家对战-公司抽水','公司总盈利(代理)','红利金额','返水金额','投注次数','有效投注金额']].agg('sum') #汇总
    df_shuying_benyue_sum.reset_index(inplace=True)
    df_shuying_benyue_sum.loc[(df_shuying_benyue_sum['存款金额']!=0)|(df_shuying_benyue_sum['平台坐庄-投注金额']!=0),'活跃人数']=1# 增加活跃
    df_shuying_benyue_sum['活跃人数'].fillna(0,inplace=True)
    df_shuying_benyue_sum=df_shuying_benyue_sum[['会员账号','币种','上级代理','存款金额','提款金额','平台坐庄-投注金额','平台坐庄-下注金额','平台坐庄-派彩金额','平台坐庄-公司输赢','玩家对战-下投注额','玩家对战-玩家输赢','玩家对战-公司抽水','公司总盈利(代理)','红利金额','返水金额','投注次数','有效投注金额','会员属性','二级部门','活跃人数','一级部门','不结算人数']]
    df_shuying_benyue_sum.to_csv('river数据\\BTY日报【会员汇总】.csv', encoding='utf_8_sig',index=False) #river
    # 正常会员的表格-不是不结算会员，不是测试会员
    df_shuying=df_shuying[df_shuying['结算非测试人数']==1]
    # 代理线每日数据 更改一级部门之前
    df_shuying_daili=of.func_shuying_rate(df_shuying,['日期','币种','一级部门','二级部门','小组','上级代理']) #输赢报表：汇总+计算比率     # 更改代理线
    df_shuying.loc[df_shuying['一级部门'].isin(['鲲鹏seo','鲲鹏其他','外代']),'一级部门']='BTY鲲鹏' # 更改一级部门
    df_shuying.loc[df_shuying['一级部门'].isin(['雨燕直播']),'一级部门']='BTY雨燕'
    df_shuying.loc[(df_shuying['一级部门'].str.contains('GT')),'一级部门']='BTY-GT'
    # 输出
    df_shuying_bz=of.func_shuying_rate(df_shuying,['日期','币种']) #输赢报表：汇总+计算比率
    # 选中 上述三个一级部门
    df_shuying_yiji=df_shuying[df_shuying['一级部门'].isin(['BTY鲲鹏','BTY雨燕','BTY-GT'])]
    df_shuying_yiji=of.func_shuying_rate(df_shuying_yiji,['日期','币种','一级部门']) #输赢报表：汇总+计算比率
    # 选中 BTY鲲鹏; 日期 一级部门 vip 为index
    df_shuying_vip=df_shuying[df_shuying['一级部门'].isin(['BTY鲲鹏'])]
    df_shuying_vip=of.func_shuying_rate(df_shuying_vip,['日期','币种','一级部门','vip']) #输赢报表：汇总+计算比率
    # 币种换算
    for df in [df_shuying_bz,df_shuying_yiji,df_shuying_vip,df_shuying_daili]:
        for i in ['存款金额','提款金额','存提差','有效投注金额','平台坐庄-公司输赢','玩家对战-公司抽水','红利金额','返水金额','毛利','公司总盈利(代理)']:
            df.loc[df['币种']=='VND',i]=df.loc[df['币种']=='VND',i]/3300
            df.loc[df['币种']=='USDT',i]=df.loc[df['币种']=='USDT',i]*7

    cf.func_multidf([df_shuying_bz,df_shuying_yiji,df_shuying_vip,df_shuying_daili],['币种数据','一级部门数据','BTY鲲鹏vip数据','代理数据'],'图片数据\\'+str(max(df_shuying_bz['日期']))+'BTY当月平台数据.xlsx','noindex')

# 会员账号 groupby
work1()
work2()



