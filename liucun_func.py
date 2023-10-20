import pandas as pd
from datetime import datetime,timedelta
import numpy as np

# 新增列 有效性为 第几日 n日留存
def func_liucun_jisuan(df):
    df.loc[(df['有效投注金额']+df['充值代充金额'])>0,'有效行为天数']=1# 增加列 有效行为天数
    df['第几日']=(df['最后行为日期']-df['首存时间'])+timedelta(days=1)# 增加列 第几日留存
    df.loc[df['有效行为天数'].isnull(),'第几日']=np.nan# 有效行为天数NaN，第几日就为0
    for i in [2,3,4,5,7,10,15,20,25,30]:# 增加列 2日留存等等
        df.loc[df['第几日'] ==timedelta(days=i),str(i)+'日留存']=1
    return df

# 每一个代理的留存率
def func_liucun_daili_row(df_daili,df):
    list_shuju=df_daili.head(1).values.flatten().tolist()[:3]# 数据list
    int_shoucun_all=df_daili['会员账号'].sum()# '首存人数'
    list_shuju.append(int_shoucun_all)
    for j in [2,3,4,5,7,10,15,20,25,30]:# 计算 留存数据
        date=max(df['首存时间'])# 报表首存时间最近的日期
        int_liucun=df_daili[str(j)+'日留存'].sum()# 计算留存人数
        int_shoucun=df_daili[df_daili['首存时间']<=(date-timedelta(days=(j-1)))]['会员账号'].sum()# 计算2日首存人数 首存时间 <=date-timedelta(days=2-1)
        perc_ciri=int_liucun/int_shoucun if int_liucun>0 else np.nan# 计算2日数量和比例
        list_shuju.extend([int_liucun,int_shoucun, perc_ciri])
    return list_shuju
#计算代理摘要
def func_liucun_daili(df):
    df_daili_all=df.groupby(['一级部门','二级部门','上级代理','首存时间']).agg({'会员账号': 'nunique', '2日留存': 'sum', '3日留存': 'sum', '4日留存': 'sum', '5日留存': 'sum', '7日留存': 'sum', '10日留存': 'sum', '15日留存': 'sum', '20日留存': 'sum', '25日留存': 'sum', '30日留存': 'sum'}) #gruopby(['会员账号','上级代理'])
    df_daili_all.reset_index(inplace=True)
    list_daili=df_daili_all['上级代理'].drop_duplicates().to_list()# 计算每一个代理留存率，循环每一位代理
    df_daili=pd.DataFrame(columns=['一级部门','二级部门','上级代理','首存人数','2日留存人数','2日首存人数','2日留存率','3日留存人数','3日首存人数','3日留存率','4日留存人数','4日首存人数','4日留存率','5日留存人数','5日首存人数','5日留存率','7日留存人数','7日首存人数','7日留存率','10日留存人数','10日首存人数','10日留存率','15日留存人数','15日首存人数','15日留存率','20日留存人数','20日首存人数','20日留存率','25日留存人数','25日首存人数','25日留存率','30日留存人数','30日首存人数','30日留存率'])# 用来储存留存数据 每次循环后写数据
    print(datetime.now().strftime('%H:%M:%S'),'开始循环',len(list_daili),'次')
    n=0
    for i in list_daili:
        n=n+1 # 循环进度
        if n % 100 == 0:
            print(datetime.now().strftime('%H:%M:%S'),'已处理',n,'位代理')
        df_daili_one=df_daili_all[df_daili_all['上级代理'] == i ]# 选中一个代理
        list_shuju=func_liucun_daili_row(df_daili_one,df)
        df_daili.loc[len(df_daili)]=list_shuju# 写数据
    df_daili.sort_values(by='首存人数',ascending=False,inplace=True)# 排序
    return df_daili
#计算小组与部门摘要
def func_liucun_bumen(df_daili,x,y,z):
    list_param=[]
    for i in [x,y,z]:
        if i is not None:
            list_param.append(i)
    df_bumen=df_daili.groupby(list_param).agg({'首存人数': 'sum', '2日留存人数': 'sum', '2日首存人数': 'sum', '3日留存人数': 'sum', '3日首存人数': 'sum', '4日留存人数': 'sum', '4日首存人数': 'sum', '5日留存人数': 'sum', '5日首存人数': 'sum', '7日留存人数': 'sum', '7日首存人数': 'sum', '10日留存人数': 'sum', '10日首存人数': 'sum', '15日留存人数': 'sum', '15日首存人数': 'sum', '20日留存人数': 'sum', '20日首存人数': 'sum', '25日留存人数': 'sum', '25日首存人数': 'sum', '30日留存人数': 'sum', '30日首存人数': 'sum'}) 
    if list_param==['一级部门']:
        df_bumen.loc['平台']=df_bumen.sum()
    df_bumen.reset_index(inplace=True)
    for j in [2,3,4,5,7,10,15,20,25,30]:# 生成比率 大于等于0生成百分号
        df_bumen[str(j)+'日留存率'] = (df_bumen[str(j)+'日留存人数']/df_bumen[str(j)+'日首存人数'])
        df_bumen[str(j)+'日留存率']=np.where((df_bumen[str(j)+'日留存率'] >0), df_bumen[str(j)+'日留存率'] , 0) #.map(lambda n: '{:.2%}'.format(n))
    list_param.extend(['首存人数','2日留存人数','2日留存率','3日留存人数','3日留存率','4日留存人数','4日留存率','5日留存人数','5日留存率','7日留存人数','7日留存率','10日留存人数','10日留存率','15日留存人数','15日留存率','20日留存人数','20日留存率','25日留存人数','25日留存率','30日留存人数','30日留存率'])
    df_bumen = df_bumen[list_param]
    df_bumen.sort_values(by='首存人数',ascending=False,inplace=True)# 排序
    return df_bumen

#制作一级部门首存时间留存率
def func_liucun_shijian(df,x,y):
    list_param=[]
    for i in [x,y]:
        if i is not None:
            list_param.append(i)
    list_param.append('首存时间')
    df_yiji_all=df.groupby(list_param).agg({'会员账号': 'nunique', '2日留存': 'sum', '3日留存': 'sum', '4日留存': 'sum', '5日留存': 'sum', '7日留存': 'sum', '10日留存': 'sum', '15日留存': 'sum', '20日留存': 'sum', '25日留存': 'sum', '30日留存': 'sum'}) 
    df_yiji_all.reset_index(inplace=True)
    for j in [2,3,4,5,7,10,15,20,25,30]:# 生成比率 大于0生成百分号
        df_yiji_all[str(j)+'日留存率'] = (df_yiji_all[str(j)+'日留存']/df_yiji_all['会员账号'])
        df_yiji_all[str(j)+'日留存率']=np.where((df_yiji_all[str(j)+'日留存率'] >0), df_yiji_all[str(j)+'日留存率'], np.nan) #.map(lambda n: '{:.2%}'.format(n)) #一列
    list_param.extend(['会员账号','2日留存','2日留存率','3日留存','3日留存率','4日留存','4日留存率','5日留存','5日留存率','7日留存','7日留存率','10日留存','10日留存率','15日留存','15日留存率','20日留存','20日留存率','25日留存','25日留存率','30日留存','30日留存率'])# 调整和截取列
    df_yiji_all = df_yiji_all[list_param]
    df_yiji_all.rename(columns={'首存时间': '首存日期', '会员账号': '首存人数','2日留存': '次日留存人数','2日留存率': '次日留存率','3日留存': '3日留存人数','4日留存': '4日留存人数','5日留存': '5日留存人数','7日留存': '7日留存人数','10日留存': '10日留存人数','15日留存': '15日留存人数','20日留存': '20日留存人数','25日留存': '25日留存人数','30日留存': '30日留存人数'}, inplace=True)# 更改列名称
    df_yiji_all.replace(0, np.nan, inplace=True)
    return df_yiji_all

def func_ycx_rate(df_liucun_huiyuan,str_column_bumen): #一次性报表计算
    df_ycx_daili=df_liucun_huiyuan.groupby([str_column_bumen]).agg({'会员账号':'nunique','充值代充金额':'sum','提款金额':'sum','有效投注金额':'sum','平台坐庄-公司输赢':'sum','有效投注天数':'sum','有效行为天数':'sum','一次性会员人数':'sum','存款低于百元会员人数':'sum','流水低于百元会员人数':'sum','一次性会员充值代充金额':'sum','存款低于百元会员充值代充金额':'sum','流水低于百元会员充值代充金额':'sum','一次性会员提款金额':'sum','存款低于百元会员提款金额':'sum','流水低于百元会员提款金额':'sum','一次性会员有效投注金额':'sum','存款低于百元会员有效投注金额':'sum','流水低于百元会员有效投注金额':'sum','一次性会员平台坐庄-公司输赢':'sum','存款低于百元会员平台坐庄-公司输赢':'sum','流水低于百元会员平台坐庄-公司输赢':'sum','一次性会员有效行为天数':'sum','存款低于百元会员有效行为天数':'sum','流水低于百元会员有效行为天数':'sum','存提差':'sum','一次性会员存提差':'sum','存款低于百元会员存提差':'sum','流水低于百元会员存提差':'sum'})
    if str_column_bumen=='一级部门':
        df_ycx_daili.loc['平台']=df_ycx_daili.sum()
    df_ycx_daili.reset_index(inplace=True)
    df_ycx_daili.rename(columns={'会员账号': '首存人数'},inplace=True)
    list_columns=[]
    for j in ['一次性会员人数','存款低于百元会员人数','流水低于百元会员人数']:
        df_ycx_daili[j+'占比']=np.where(df_ycx_daili['首存人数']!=0,df_ycx_daili[j]/df_ycx_daili['首存人数'].abs(),0)
        list_columns.append(j)
        list_columns.append(j+'占比')
        for i in ['充值代充金额', '提款金额','存提差', '有效投注金额', '平台坐庄-公司输赢', '有效行为天数']:
            df_ycx_daili[j[:-2]+i]=df_ycx_daili[j[:-2]+i].astype(float)
            df_ycx_daili[i]=df_ycx_daili[i].astype(float)
            df_ycx_daili[j[:-2]+i+'占比']=np.where(df_ycx_daili[i]!=0,df_ycx_daili[j[:-2]+i]/df_ycx_daili[i].abs(),0)
            list_columns.append(j[:-2]+i)
            list_columns.append(j[:-2]+i+'占比')
    list_columns[0:0]=[str_column_bumen,'首存人数']
    df_ycx_daili=df_ycx_daili[list_columns]
    df_ycx_daili.sort_values(by='首存人数',ascending=False,inplace=True)#排序
    return df_ycx_daili








