# # -*- coding: utf-8 -*-
# import pandas as pd
# import numpy as np
# from datetime import datetime,timedelta
# import os,sys,re
# pd.set_option('display.max_colwidth', None) #显示单元格完整信息
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
#
# sys.path.append(os.path.dirname(os.path.abspath(os.getcwd())))
# import common_func as cf
# import _func as of
#
#
# # 输出
# print(datetime.now().strftime('%H:%M:%S'),'开始输出')# 输出excel
# df.to_excel(r"df.xlsx",index=False)
# with open('txt_yichang.txt','a',encoding='UTF-8') as txt_yichang:# 输出文本
#     txt_yichang.write(str(e))
#     txt_yichang.write('\n')
#
# # 选中
# df=df.loc[(d3['有效投注额']!=0) | (df['存款金额']!=0)] #选中
# df=df[df.columns[0]]
# df_hongli_canyuzhe=df_hongli_all_filled[df_hongli_all_filled['会员账号'].isin(list_mingdan)] #~
# df=df.loc[df['日期']=='总计','红利':] #loc[列条件 选中行/index:index，列名称 选中行]
# variable_format=df['开赛日期'][i] #行+列 选中列的第i行
# df.fillna('',inplace=True)#null操作
# df['一级部门'].fillna('代理部',inplace=True) #行+列 选中列填充nan
# df.fillna({'最后登录时间': 0, '注册时间': 0, '首存时间': 0}, inplace=True)# 计算(不能有nan 需要填充0)
# df['上级代理'].notnull()
# df['上级代理'].isnull()
# df.drop('VIP等级', axis=1, inplace=True)#drop操作 列
# df.drop(["哈希"], inplace = True) #行
# df = df.dropna(subset=['sms'])
# df_hongli_all_filled.drop_duplicates(subset=['订单号'],inplace=True) #去重复 也可全表去重复
# (df['date'] > '2000-6-1') & (df['date'] <= '2000-6-10') #日期范围
# df.iloc[[0, -1]]#第一行 和 最后一行
# df_dakeshuying.tail(10).head(9) #取得倒数第2行到倒数第10行
# df.replace(0, np.nan, inplace=True) #值替换
# df.at[行index, 列名称str]
#
# # 并表
# df=pd.concat([df,df_temp],ignore_index=True) #上下并表
# df=pd.concat([df,df],axis=1)#concat 左右
# df=df.merge(df1,left_on='会员账号',right_on=0,  how='outer').merge(df2,on='日期', how='outer') #左右并表
# df=df.merge(df, left_index=True, right_index=True)#merge
#
# #格式
# df['team1char1'] = df['team1'].astype(str)
# df = df.astype({'有效投注额':'int',"公司输赢":"int"})#整数格式
# date = pd.to_datetime(single_date).date() #variable 得到日期
# df['首存时间']= pd.to_datetime(df['首存时间']).dt.date #日期格式
# df.OpenTime=pd.to_datetime(df.OpenTime, unit='ms') #timestamp to datetime  , unit='ms'
# df_1minkline.OpenTime=df_1minkline.OpenTime+timedelta(hours=8) #convert to gmt+8
# df['开赛时间']= pd.to_datetime(df['开赛时间']).dt.time #时间格式
# df_linglong['第几周']=df_linglong['日期'].dt.isocalendar().week
#
# # str操作
# df['投注详情'].str.contains(team1kwd, case=False) #包含关键字
# df_hongli_blank.loc[df_hongli_blank['申请备注'].str.contains(r'^(?=.*代理)(?=.*借支)'),['活动标题']]='代理借支'
# df['team1char1'] = df['team1'].str[0] # 截取字符
# df.columns = df.columns.str.lower().str.replace(('\t|\r|\n| '), '',regex=True) # 小写与去除符号
# df['投注详情'] = df['投注详情'].str.lower().str.replace(('\t|\r|\n| '), '',regex=True)
# df[['team1','team2']]=df[['team1','team2']].apply(lambda x: x.str.strip())# 去除首尾空格
# df[df.columns[2]]=df[df.columns[2]].apply(lambda x: x.split('*')[1:])# 分割成list
# df[['team1','team2']] = pd.DataFrame(df[df.columns[2]].tolist())# list列成新表格 （已知分割后列数量）
# df=pd.DataFrame(df[df.columns[2]].tolist(), df.index).add_prefix('team_')# list列成新表格 （未知分割后数量）
# df_huiyuan['手机号长度']=df_huiyuan['手机号码'].str.len()
#
# # 计算
# df.set_index('场馆名称',inplace=True)#求和
# df.loc['平台']=df.sum()
# df.reset_index(inplace=True)
# df1=df.sum()[1:].to_frame(name=i) #转df 加columnName i
# series=df4['留存'].value_counts() #不同值出现次数
# df['第几日']=(df['自然日期']-df['首存日期']).dt.days+1  #日期计算
# date=max(df['首存时间']) # 最大日期
# (date-timedelta(days=(j-1))) #日期加减天数-一致的天数
# df_shuying_huiyuan['天数']=df_shuying_huiyuan['结束日期']-df_shuying_huiyuan['开始日期']+timedelta(days=1)
# df_shuying_huiyuan['天数']=(df_shuying_huiyuan['天数']/ np.timedelta64(1, 'D')).astype(int)
# df['体育类投注天数']=np.where((df['体育类有效投注'] >0), 1, 0) #列 判断+新列赋值
#
# # 表格操作
# df['游戏明细'] =''#新增
# df['游戏明细'] =np.nan
# df['Animals'] = myList #写数据
# df = df[['一级部门','二级部门','小组','代理名称','首存人数']]#调整顺序 截取
# df.rename(columns={'oldName1': 'newName1', 'oldName2': 'newName2'}, inplace=True) #更改名称
# df.sort_values(by='一级部门',ascending=False,inplace=True)#排序
# df.sort_values(['a', 'b'], ascending=[True, False],inplace=True)
# if df.empty or df is None:#判断空或者不存在
#     df=df1.copy()#复制
# df=pd.DataFrame(columns=['代理名称','首存人数'])#表格 新建
# df=df.groupby(['代理账号','首存时间']).agg({'用户名称': 'nunique', '次日留存': '; '.join, '3日留存': 'sum', '4日留存': 'sum', '5日留存': 'sum', '7日留存': 'sum', '10日留存': 'sum', '15日留存': 'sum', '20日留存': 'sum', '25日留存': 'sum', '30日留存': 'sum'}) #汇总
# df.reset_index(inplace=True)
# df_pivot=df_linglong.pivot(index=['会员账号', '存款挡位'], columns='第几日', values='存款额') #透视表
# df_pivot.reset_index(inplace=True)
# df=pd.pivot_table(df, values='红利金额(元)', index='活动标题', columns='发放日期', aggfunc='sum',margins=True, margins_name='总计', sort=True)#透视表 #, fill_value=None,  dropna=True, observed=False
# df.reset_index(inplace=True)
# df_touzhu=df_touzhu.T #行列转换
# df_touzhu.reset_index(inplace=True)
#
# #————————————————————————————————————————————————————————————————————————————————————————————————————————————————————#
# # 行、header、index等操作
# df.index.values.tolist() #index
# df.columns.values.tolist() #列 得到list
# .values.flatten().tolist() #行变list
# df_idxmax_vol=df.groupby(np.arange(len(df.index)) // 2500)[['Volume']].idxmax()# 分区间，找volume最大值4个点的index
# df_idxmax_vol_rows = df.loc[df_idxmax_vol.Volume]
# df['投注天数总计']=df.loc[:,'体育类投注天数':'捕鱼类投注天数'].sum(axis=1)# 行求和
# df['最后活跃日期']=df[['最后登录','注册','首存','最后下注','最后存款','最后取款']].values.max(axis=1) # 行最大值
# .tolist() #列变list
# def get_date(start_date,p_days):# 日期加减天数-不一致的天数
#     return start_date-timedelta(days=p_days)
# df['活动前开始时间'] = df.apply(lambda x: get_date(x['活动开始日期'], x['参与天数']), axis=1)
# df.set_index('场馆类别', inplace=True) # 重新设置index列
# df.loc['彩票'] += df.loc['哈希'] # 把 哈希 并入 彩票
# df.loc[len(df)]=list_shuju #最后一行 写数据
#
# #————————————————————————————————————————————————————————————————————————————————————————————————————————————————————#
#
#
#
# #####################      生成图片时操作      ####################
# ['red' if x<df['投注人数'].mean() else 'black' for x in df['投注人数'].tolist()]#低于平均标红
# df['体育']=(df['体育类投注天数']/df['投注天数总计']).apply(lambda x: round(x, 4))#保留4位小数
# integer_columns = df.select_dtypes(include=['int64','float64']).columns#改千分位 整列
# for i in integer_columns:
#     df[i]=df[i].apply('{:,}'.format)
# '{:,}'.format(df.at[0,'公司输赢'])#改千分位 一个单元格
# for j in [2,3,4,5,7,10,15,20,25,30]:# 生成比率 大于等于0生成百分号
#     df[str(j)+'日留存率'] = (df[str(j)+'日留存人数']/df[str(j)+'日首存人数'])
#     df[str(j)+'日留存率']=np.where((df[str(j)+'日留存率'] >0), df[str(j)+'日留存率'].map(lambda n: '{:.2%}'.format(n)), 0) #一列
# second_day_ratio='{:.2%}'.format(second_day_number/daili_clients_number)#一个单元格
# df['投注人数占比']=(df['投注人数占比']).map(lambda n: '{:.2%}'.format(n))#改百分号
# import json# 输出json
# with open('whole_tree.json', 'w', encoding='utf-8') as f:
#     json.dump(content, f, ensure_ascii=False, indent=4)
# with open(r'whole_tree.json', encoding='utf8') as f:# 读取json文件
#     d = json.load(f)
#
# ######################python####################
# # list
# # 不用赋值，method会改变并保存list
# lst.append(4)
# lst.extend([5, 6, 7])
# lst.extend((8, 9, 10))
# list_dfname.insert(4,'全平台')
# if not list #如果list为空
#     if i in [] # not in
#     if i== or i==
# # []左包含，右不包含
# # re
# # 选中string中的数值
# import re
# date=re.search(r'\d+', filename).group(0)
#
# ############################# 业务函数  ##########################
# if foldername in ['安博自营馆','LPL夏季赛','电竞包赔大作战','女足世界杯早盘投注','虚拟币存款']:
#     df.reset_index(inplace=True)
#     df.rename(columns={str(df.columns[3]):0,str(df.columns[2]):'申请时间',str(df.columns[1]):'会员等级',str(df.columns[0]):'会员账号'},inplace=True)
#
# df_dengji=pd.DataFrame()
# for filename1 in os.listdir(os.path.abspath(os.getcwd())+'\\'+'原始数据'+'\\'+'等级变动'):
#     for filename2 in os.listdir(os.path.abspath(os.getcwd())+'\\'+'原始数据'+'\\'+'等级变动'+'\\'+filename1):
#         df_dengji_child = cf.func_concat('原始数据'+'\\'+'等级变动'+'\\'+filename1+'\\'+filename2)# 读取文件
#         df_dengji=pd.concat([df_dengji,df_dengji_child],ignore_index=True)
# df_dengji.drop_duplicates(inplace=True)
#
# df_dengji.sort_values(['会员账号', '变化时间'], ascending=[True, True],inplace=True) # 根据会员账号 变化时间 排序
# df_dengji.drop_duplicates(subset=['会员账号'],inplace=True, keep='last') # 会员账号去重复 保留最新的变化时间
#
# .abs()
#
# df_dake['游戏平台'].astype(str).str.split('; ').apply(set).str.join('; ')
#
# df_huiyuan=df_dianwei1.groupby(['经理','币种','月份','会员账号'])[['存款金额','有效投注金额','公司总盈利(代理)']].agg('sum')
#
# df_shoucun.to_csv('历史首存.csv', encoding='utf_8_sig',index=False) # river
#
# # # 名单匹配vip等级变动
# # df_mingdan_1=df_huiyuan[(df_huiyuan['非雨燕GTkk178']==1)]['会员账号'] # 得到名单
# # df_vip_1 = cf.func_read_vip(df_mingdan_1,os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\vip等级变动')
# # df_vip_1['开始日期']=pd.to_datetime(df_vip_1['调整时间']).dt.date    # 截取所需时间
# # df_vip_1=cf.func_shijianduan(df_vip_1,['调整时间'],'本月')  # 根据df的list_column_date标注数据的时间段
# # df_vip_1=df_vip_1[df_vip_1['结束日期'].notnull()] #保留结束日期之前的数据
# # df_vip_1.sort_values(['会员账号', '调整时间'], ascending=[True, True],inplace=True) #  排序后去除# 根据会员账号 变化时间 排序
# # df_vip_1.drop_duplicates(subset=['会员账号'],inplace=True, keep='last') # 会员账号去重复 保留最新的变化时间
# # df_vip_1 = df_vip_1[['会员账号','调整后']] # 保留需要的列
# # df_vip_1.rename(columns={'调整后':'最新vip等级电维1'},inplace=True)
# # df_huiyuan=df_huiyuan.merge(df_vip_1,on='会员账号',how='left')# 会员列表匹配vip等级
# # df_huiyuan.loc[df_huiyuan['最新vip等级电维1'].isnull(),'最新vip等级电维1']=df_huiyuan.loc[df_huiyuan['最新vip等级电维1'].isnull(),'VIP等级']# null填充注册表格的vip
#
#
# # # 处理手机号码
# # df_huiyuan['手机号码'] = df_huiyuan['手机号码'].replace((' '), '',regex=True) # 小写与去除符号
# # df_huiyuan['手机号码'] = df_huiyuan['手机号码'].astype(str).str.split('.').str[0]
# # df_huiyuan['手机号码'] = df_huiyuan['手机号码'].replace(('nan'), '',regex=True) # 小写与去除符号
# # df_huiyuan['手机号长度']=df_huiyuan['手机号码'].str.len()
#
# # # VND换算成CNY
# # for df in [df_huiyuan_daily]:
# #     for i in ['首存金额']:
# #         df.loc[df['国家']=='越南',i]=df.loc[df['国家']=='越南',i]/3300
#
# # from langdetect import detect
# # def func_detect_lan(x):
# #     try:
# #         return detect(x)
# #     except:
# #         return 'error'
# # df_huiyuan['姓名字体']=df_huiyuan['姓名'].astype(str).apply(lambda x: func_detect_lan(x))
