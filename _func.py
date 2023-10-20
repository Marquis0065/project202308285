import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import os

import common_func as cf

def func_huiyuan_rate(df,list_columnstr): #会员报表：汇总+计算比率 
    # 日期 币种 一级部门index
    list_column_zhuce=list_columnstr.copy()
    list_column_zhuce.append('注册时间')
    list_column_shoucun=list_columnstr.copy()
    list_column_shoucun.append('首存时间')
    
    df_huiyuan_zhuce=df.groupby(list_column_zhuce).agg({'会员账号': 'nunique', '绑定手机号人数': 'sum','注册当天首存人数': 'sum' })
    df_huiyuan_zhuce.reset_index(inplace=True)
    df_huiyuan_zhuce.rename(columns={'会员账号': '注册人数','注册时间': '日期'},inplace=True) 

    df.to_csv('ml.csv')

    df_huiyuan_shoucun=df.groupby(list_column_shoucun).agg({'首存人数': 'sum','绑定并首存人数': 'sum','首存金额': 'sum'})#'首存金额': 'sum',
    df_huiyuan_shoucun.reset_index(inplace=True)
    df_huiyuan_shoucun.rename(columns={'首存时间': '日期'},inplace=True) 
    list_columnstr.insert(0,'日期')
    df_huiyuan_daily= df_huiyuan_zhuce.merge(df_huiyuan_shoucun,on=list_columnstr,how='outer')  
    # df_huiyuan_daily['首存金额']=df_huiyuan_daily['首存金额'].astype(float) # 首存金额 格式  
    # 筛选和排序
    df_huiyuan_daily=df_huiyuan_daily[(df_huiyuan_daily['日期']>=df_huiyuan_daily['开始日期'])&(df_huiyuan_daily['日期']<=df_huiyuan_daily['结束日期'])]
    df_huiyuan_daily.drop('开始日期', axis=1, inplace=True)#drop操作 列
    df_huiyuan_daily.drop('结束日期', axis=1, inplace=True)#drop操作 列
    for i in ['开始日期','结束日期']:    
        list_columnstr.remove(i)
    df_huiyuan_daily.sort_values(['日期', '注册人数'], ascending=[True, False],inplace=True)
    # 增加 累计 行
    df_huiyuan_daily.set_index('日期', inplace=True) 
    df_huiyuan_daily.loc['1999-9-9']=df_huiyuan_daily.sum(numeric_only=True)
    df_huiyuan_daily.reset_index(inplace=True)
    # 注册首存计算
    df_huiyuan_daily['转化率']=np.where(df_huiyuan_daily['注册人数']>0,df_huiyuan_daily['首存人数']/df_huiyuan_daily['注册人数'],0)
    df_huiyuan_daily['注册当天首存比率']=np.where(df_huiyuan_daily['注册人数']>0,df_huiyuan_daily['注册当天首存人数']/df_huiyuan_daily['注册人数'],0)
    df_huiyuan_daily['绑定手机号比率']=np.where(df_huiyuan_daily['注册人数']>0,df_huiyuan_daily['绑定手机号人数']/df_huiyuan_daily['注册人数'],0)
    df_huiyuan_daily['绑定并首存比率']=np.where(df_huiyuan_daily['注册人数']>0,df_huiyuan_daily['绑定并首存人数']/df_huiyuan_daily['注册人数'],0)
    list_columnstr.extend(['注册人数','首存人数','首存金额','转化率','注册当天首存人数','注册当天首存比率','绑定手机号人数','绑定手机号比率','绑定并首存人数','绑定并首存比率']) #,'首存金额'
    df_huiyuan_daily=df_huiyuan_daily[list_columnstr]
    return df_huiyuan_daily

def func_shuying_jisuan(df): #输赢表格处理和计算非比率
    df.rename(columns={'账户名': '会员账号'}, inplace=True)#列 更改名称
    df.loc[(df['存款金额']!=0)|(df['平台坐庄-投注金额']!=0),'活跃人数']=1# 增加活跃
    df.loc[(df['存款金额']!=0),'存款人数']=1        #存款人数； 
    df.loc[(df['平台坐庄-投注金额']!=0),'投注人数']=1 #投注人数；
    df['存提差']=df['存款金额']-df['提款金额']
    df['毛利']=df['平台坐庄-公司输赢']+df['玩家对战-公司抽水']-df['红利金额']-df['返水金额']
    return df
def func_ml_ribao_jisuan(df): #会员总报表处理和计算非比率
    df.loc[(df['充值金额']!=0)|(df['有效投注']!=0),'活跃人数']=1# 增加活跃
    df.loc[(df['充值金额']!=0),'存款人数']=1        #存款人数； 
    df.loc[(df['有效投注']!=0),'投注人数']=1 #投注人数；
    df['存提差']=df['充值金额']-df['提现金额']
    return df

def func_bujiesuan(df): # 匹配不结算会员
    df_nonjiesuan = cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\不结算会员代理')
    df=df.merge(df_nonjiesuan['不结算会员'].drop_duplicates().to_frame(),left_on='会员账号',right_on='不结算会员',how='left')
    df=df.merge(df_nonjiesuan['不结算代理'].drop_duplicates().to_frame(),left_on='上级代理',right_on='不结算代理',how='left')
    df.loc[(df['不结算会员'].notnull())&(df['不结算代理'].notnull()),'不结算人数']=1
    df.loc[(df['不结算人数'].isnull())&(df['会员属性'].isnull()),'结算非测试人数']=1
    return df
def func_wuxiao(df): # 匹配无效会员
    df_nonjiesuan = cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\ml手工表格\\无效会员代理')
    df=df.merge(df_nonjiesuan['无效会员'].drop_duplicates().to_frame(),left_on='会员账号',right_on='无效会员',how='left')
    df=df.merge(df_nonjiesuan['无效代理'].drop_duplicates().to_frame(),left_on='上级代理',right_on='无效代理',how='left')
    df.loc[(df['无效会员'].notnull())&(df['无效代理'].notnull()),'无效人数']=1
    df.loc[df['无效人数'].isnull(),'无效人数']=0
    return df

def func_shuying_rate(df,list_columnstr): #输赢报表：汇总+计算比率  
    df_shuying=df.groupby(list_columnstr)[['活跃人数','存款人数','存款金额','提款金额','存提差','投注人数','有效投注金额','平台坐庄-公司输赢','玩家对战-公司抽水','公司总盈利(代理)','红利金额','返水金额','毛利']].agg('sum')
    df_shuying.reset_index(inplace=True)
    for i in ['活跃人数','存款人数','存款金额','提款金额','存提差','投注人数','有效投注金额','平台坐庄-公司输赢','玩家对战-公司抽水','公司总盈利(代理)','红利金额','返水金额','毛利']:
        df_shuying[i] = df_shuying[i].astype(float)    # 计算
    df_shuying['杀率']=np.where(df_shuying['有效投注金额']!=0,df_shuying['平台坐庄-公司输赢']/df_shuying['有效投注金额'].abs(),0)
    df_shuying['红利/流水比率']=np.where(df_shuying['有效投注金额']!=0,df_shuying['红利金额']/df_shuying['有效投注金额'].abs(),0)
    df_shuying['返水/流水比率']=np.where(df_shuying['有效投注金额']!=0,df_shuying['返水金额']/df_shuying['有效投注金额'].abs(),0)
    df_shuying['流水/存款两位小数']=np.where(df_shuying['存款金额']!=0,df_shuying['有效投注金额']/df_shuying['存款金额'].abs(),0)
    return df_shuying
def func_ml_ribao_rate(df,list_columnstr): #ml日报：汇总+计算比率  
    df_ml_ribao=df.groupby(list_columnstr)[['活跃人数','存款人数','充值金额','提现金额','存提差','投注人数','有效投注','公司输赢']].agg('sum')
    df_ml_ribao.reset_index(inplace=True)
    for i in ['活跃人数','存款人数','充值金额','提现金额','存提差','投注人数','有效投注','公司输赢']:
        df_ml_ribao[i] = df_ml_ribao[i].astype(float)    # 计算
    df_ml_ribao['杀率']=np.where(df_ml_ribao['有效投注']!=0,df_ml_ribao['公司输赢']/df_ml_ribao['有效投注'].abs(),0)
    df_ml_ribao['流水/存款两位小数']=np.where(df_ml_ribao['充值金额']!=0,df_ml_ribao['有效投注']/df_ml_ribao['充值金额'].abs(),0)
    return df_ml_ribao

def func_liushi_jisuan(df): # 会员流失留存计算
    df.loc[df['VIP等级']=='VIP0','未存款流失人数']=1 # 未存款流失人数
    df.loc[(df['未存款人数-流失'].isnull())&(df['活跃人数'].isnull()),'首存流失人数']=1# 首存流失人数
    df.loc[df['注册时间']<df['结束日期'],'满足流失留存注册时间的人数']=1 # 满足流失留存注册时间要求 时间段的结束日期 小一天
    df.loc[df['首存时间']==df['结束日期'],'满足流失留存首存时间的人数']=1 # 满足流失留存首存时间要求 时间段的结束日期 相等
    df.loc[df['投注次数']!=0,'投注次数不为0']=1 # 投注次数不为0
    return df

def func_changguan_rate(df_dalei):    # 分表合并计算变化
    df_dalei   = df_dalei[['日期','币种','游戏平台', '总有效投注', '公司总盈利(代理)', '游戏人数']]
    df_dalei_max=df_dalei[df_dalei['日期']==max(df_dalei['日期'])]# max日期获得一张新表格，列更改为，最后一日，最后一日vip等级
    df_dalei_max.rename(columns={'日期': '最后一日', '总有效投注': '最后一日总有效投注', '公司总盈利(代理)': '最后一日公司总盈利(代理)', '游戏人数': '最后一日游戏人数'}, inplace=True)
    df_dalei_min=df_dalei[df_dalei['日期']==max(df_dalei['日期'])-timedelta(days=1)]# min日期获得一张新表格，列更改为，第1日，第1日vip等级
    df_dalei_min.rename(columns={'日期': '最后第2日',  '总有效投注': '最后第2日总有效投注', '公司总盈利(代理)': '最后第2日公司总盈利(代理)', '游戏人数': '最后第2日游戏人数'}, inplace=True)
    df_dalei=df_dalei_max.merge(df_dalei_min,on=['币种','游戏平台'],how='outer')# index 会员账号 merge两张表格，新增列 31天等级变化=最后一日vip等级-第1日vip等级
    df_dalei.fillna(0, inplace=True)# minus的列不能有nan，需要填充0
    # df_dalei.set_index('游戏平台',inplace=True)
    # df_dalei.loc['平台']=df_dalei.sum(numeric_only=True)# 一级部门数据增加平台行
    df_dalei.reset_index(inplace=True)
    for i in ['总有效投注', '公司总盈利(代理)','游戏人数']:
        df_dalei[i+'差值']=df_dalei['最后一日'+i]-df_dalei['最后第2日'+i]
        df_dalei[i+'变化幅度']=np.where(df_dalei['最后第2日'+i]!=0,df_dalei[i+'差值']/df_dalei['最后第2日'+i].abs(),0)
    return df_dalei
def func_daili_diff(df_dalei,str_column,list_index,list_value):    # 分表合并计算变化
    df_dalei_max=df_dalei[df_dalei[str_column]==max(df_dalei[str_column])]# max日期获得一张新表格，列更改为，最后一日，最后一日vip等级
    df_dalei_min=df_dalei[df_dalei[str_column]==min(df_dalei[str_column])]# min日期获得一张新表格，列更改为，第1日，第1日vip等级
    df_dalei_max.rename(columns={str_column: '最后一日'}, inplace=True)
    df_dalei_min.rename(columns={str_column: '最后第2日'}, inplace=True)
    for i in list_value:
        df_dalei_max.rename(columns={i: '最后一日'+i}, inplace=True)
        df_dalei_min.rename(columns={i: '最后第2日'+i}, inplace=True)
    df_dalei=df_dalei_max.merge(df_dalei_min,on=list_index,how='outer')
    df_dalei.fillna(0, inplace=True)# minus的列不能有nan，需要填充0
    df_dalei.reset_index(inplace=True)
    for i in list_value:
        df_dalei[i+'增量']=df_dalei['最后一日'+i]-df_dalei['最后第2日'+i]
        df_dalei[i+'增幅']=np.where(df_dalei['最后第2日'+i]!=0,df_dalei[i+'增量']/df_dalei['最后第2日'+i].abs(),0)
    return df_dalei

# 通用处理投注记录-不处理投注详情与开赛时间
def func_touzhu_single(df_touzhu_single):
    for i in ['注单号','赛事ID/局号']:
        df_touzhu_single[i]=df_touzhu_single[i].astype(str)
    for i in ['会员账号','注单号','赛事ID/局号']:#,'结算时间','下注时间'
        df_touzhu_single[i] = df_touzhu_single[i].str.strip('\t')# 去除tab
    for i in ['派彩时间','下注时间']:
        df_touzhu_single[i]=pd.to_datetime(df_touzhu_single[i]).dt.date
    df_touzhu_single['投注次数']=1
    df_touzhu_single = df_touzhu_single.astype({'有效投注':'float',"下注金额":"float","派彩金额":"float"}) #增加列 公司盈利
    if '公司盈利' not in df_touzhu_single.columns:
        df_touzhu_single['公司盈利'] = df_touzhu_single['下注金额']-df_touzhu_single['派彩金额']
    df_touzhu_single = df_touzhu_single.astype({"公司盈利":"float"})
    df_touzhu_single['联赛']= df_touzhu_single['投注内容'].astype(str).str.split(':').str[1].str.split('<').str[0]
    df_touzhu_single['队伍']= df_touzhu_single['投注内容'].astype(str).str.split(':').str[2].str.split('<').str[0]
    df_touzhu_single.drop_duplicates(subset=['注单号'],inplace=True) #去重复 也可全表去重复
    return df_touzhu_single
# 读取和groupby投注记录
def func_touzhu_readnprocess(df_mingdan,list_col,childfolder):
    df_touzhu_all=pd.DataFrame()
    for filename in os.listdir(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\'+childfolder):
        df_touzhu_single=cf.func_concat(os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\'+childfolder+'\\'+filename)
        df_touzhu_single= func_touzhu_single(df_touzhu_single)
        if df_mingdan is not None:
            df_touzhu_single=df_touzhu_single.merge(df_mingdan,on='会员账号',how='right')
        df_touzhu_single=df_touzhu_single.groupby(list_col).agg({ '有效投注': 'sum','投注次数': 'sum', '公司盈利': 'sum'})#,'注单流水号':','.join
        df_touzhu_single.reset_index(inplace=True)
        df_touzhu_all=pd.concat([df_touzhu_all,df_touzhu_single])
        print('截至',filename,'文件夹，投注记录总表长度',len(df_touzhu_all))
    df_touzhu_all['天数']=1 # 处理总表格 加一列 天数 填充1
    df_touzhu_all=df_touzhu_all.groupby(list_col).agg({ '有效投注': 'sum','投注次数': 'sum', '公司盈利': 'sum','天数': 'sum'})# 汇总,'注单流水号':','.join
    df_touzhu_all.reset_index(inplace=True)
    return df_touzhu_all
# df_touzhu=tf.func_touzhu_readnprocess(df_mingdan,['会员账号','游戏类型','平台名称','游戏名称','结算时间'],'投注记录')# 读取和groupby投注记录,'游戏编号'

def func_hongli_biaoti(df_hongli_all):# 处理红利记录标题
    df_hongli_all['活动标题']=df_hongli_all['申请备注']
    df_hongli_all.loc[df_hongli_all['申请备注'].str.contains("男篮世界杯 决战马尼拉"),['活动标题']]='男篮世界杯 决战马尼拉'
    df_hongli_all.loc[df_hongli_all['申请备注'].str.contains("神助攻"),['活动标题']]='B体育神助攻'
    df_hongli_all.loc[df_hongli_all['申请备注'].str.contains("c2c提现", case=False),['活动标题']]='c2c提现'
    df_hongli_all.loc[df_hongli_all['申请备注'].str.contains("NBA总决赛投注加码", case=False),['活动标题']]='NBA总决赛投注加码'
    df_hongli_all.loc[df_hongli_all['申请备注'].str.contains("包赔"),['活动标题']]='包赔'
    df_hongli_all.loc[df_hongli_all['申请备注'].str.contains("测试"),['活动标题']]='测试'
    df_hongli_all.loc[df_hongli_all['申请备注'].str.contains("好友"),['活动标题']]='好友推荐'
    df_hongli_all.loc[df_hongli_all['申请备注'].str.contains("好友邀请奖励VIP1", case=False),['活动标题']]='好友邀请奖励VIP1-越'
    df_hongli_all.loc[df_hongli_all['申请备注'].str.contains("轮盘"),['活动标题']]='轮盘系统'
    df_hongli_all.loc[df_hongli_all['申请备注'].str.contains("补偿"),['活动标题']]='C2C补偿彩金'
    df_hongli_all.loc[df_hongli_all['申请备注'].str.contains("新会员首存送豪礼"),['活动标题']]='首存活动'
    df_hongli_all.loc[df_hongli_all['申请备注'].str.contains("屠榜"),['活动标题']]='屠榜礼'
    df_hongli_all.loc[df_hongli_all['申请备注'].str.contains("首存保险双奖励"),['活动标题']]='首存保险双奖励'
    df_hongli_all.loc[df_hongli_all['申请备注'].str.contains("直播"),['活动标题']]='直播'
    df_hongli_all.loc[df_hongli_all['申请备注'].str.contains(r'^(?=.*USDT)(?=.*1%)', case=False),['活动标题']]='USDT存款 专享1%加赠'
    df_hongli_all.loc[df_hongli_all['申请备注'].str.contains(r'^(?=.*欧冠)(?=.*负利)', case=False),['活动标题']]='欧冠决赛 负利返还'
    df_hongli_all.loc[df_hongli_all['申请备注'].str.contains(r'^(?=.*预约)(?=.*提现)', case=False),['活动标题']]='预约提现'
    df_hongli_all.loc[df_hongli_all['申请备注'].str.contains("周度礼金"),['活动标题']]='周度礼金'
    df_hongli_all.loc[df_hongli_all['申请备注'].str.contains("升级礼金"),['活动标题']]='升级礼金'
    df_hongli_all.loc[df_hongli_all['申请备注'].str.contains("生日"),['活动标题']]='生日礼金'
    df_hongli_all.loc[df_hongli_all['申请备注'].str.contains("充值抽奖送不停"),['活动标题']]='充值抽奖送不停'
    df_hongli_all.loc[df_hongli_all['申请备注'].str.contains("手动发放"),['活动标题']]='手动发放'
    df_hongli_all.loc[df_hongli_all['申请备注'].str.contains("manually release", case=False),['活动标题']]='测试'
    df_hongli_all.loc[df_hongli_all['申请备注'].str.contains("首存保险"),['活动标题']]='首存保险双奖励'
    df_hongli_all.loc[df_hongli_all['申请备注'].str.contains("每周好礼"),['活动标题']]='周度礼金'
    df_hongli_all.loc[df_hongli_all['申请备注'].str.contains("王者回归"),['活动标题']]='王者回归'
    # 不在上述种类的活动标题 标注为 未知
    df_hongli_all.loc[df_hongli_all['活动标题'].isnull(),['活动标题']]='#未知'

    return df_hongli_all
