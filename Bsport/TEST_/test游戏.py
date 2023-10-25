import pandas as pd
from datetime import datetime,timedelta
import os
import re



def func_read_filedate(df_mingdan,folderpath): # os.path.dirname(os.path.abspath(os.getcwd()))+'\\通用数据\\会员输赢报表'
    df_vip_all=pd.DataFrame()# 读取vip等级文件 加一列日期,
    for filename in os.listdir(folderpath):
        print(datetime.now().strftime('%H:%M:%S'),filename)
        date=re.search(r'\d+', filename).group(0)# 日期从文件名称获取,日期格式，列 第几周
        path=folderpath+'\\'+filename
        df_vip_child=pd.read_csv(path,sep=',')
        df_vip_child['日期']=pd.to_datetime(str(date), format='%Y%m%d')
        if df_mingdan!=None:
            df_vip_child=df_vip_child.merge(df_mingdan,on='会员账号',  how='inner')# 读取时比对名单，不然30个vip文件超出pandas一张sheet的处理能力
        df_vip_all=pd.concat([df_vip_all,df_vip_child],ignore_index=True)
    df_vip_all.drop_duplicates(inplace=True)
    return df_vip_all

#游戏
youxi = func_read_filedate(None,r'\\DESKTOP-OABVORH\Data\Code2023-10数据库版\输入参数\后台游戏输赢报表')
