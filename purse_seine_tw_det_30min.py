import pandas as pd
import time
from datetime import datetime, date, time, timedelta

df = pd.read_csv('C:/Users/Tibame_25/Desktop/vessel.csv',encoding='big5')

df["GPS時間"] = pd.to_datetime(df["GPS時間"], format='%Y/%m/%d %H:%M:%S') 

df_group = df.groupby("中文船名")

vessel_list = list(("裕穩101","裕穩301","百富103","百富301","大慶666","慶豐787","慶豐767",
                "日友168","日友768","日友668","日友868","日友968","日友568","豐國188","豐國189","豐國828","豐國866",
                "豐國889","豐國688","協豐788","協豐789","華偉707","興富華707","興成發707","興華發707","興旺發707","興永發707",
                "富冠808","穩發626","穩發666","穩發618","穩發636"))


for i in vessel_list:
    try:
        df = df_group.get_group(i)
        print()
        print(i)
        for e in range(0,9999):  # 有成功
            try:
                if df["GPS時間"][e]+timedelta(minutes=30) < df["GPS時間"][e+1] :
                    if df["GPS時間"][e]+timedelta(minutes=30)*2 < df["GPS時間"][e+1] :
                        print(df["GPS時間"][e]+timedelta(minutes=30),df["GPS時間"][e]+timedelta(minutes=30)*2)
                        for r in range(3,9999):
                            if df["GPS時間"][e]+timedelta(minutes=30)*r < df["GPS時間"][e+1] :
                                print(df["GPS時間"][e]+timedelta(minutes=30)*r)
                                new_column_lst = [] 
                                new_column_lst.append({"中文船名":df["中文船名"][0],"GPS時間":df["GPS時間"][e]+timedelta(minutes=30)})
                                new_column_lst.append({"中文船名":df["中文船名"][0],"GPS時間":df["GPS時間"][e]+timedelta(minutes=30)*2})
                                new_column_lst.append({"中文船名":df["中文船名"][0],"GPS時間":df["GPS時間"][e]+timedelta(minutes=30)*r})
                                df = df.append(new_column_lst)
                                df = df.sort_values("GPS時間",ignore_index=True) #新增資料後，排序，並修改原本的df
                            else:
                                break      
                else:
                    continue
            except (ValueError,KeyError):
                pass
    except KeyError as e:
        print()
        print(i)
        print("查無資料")

print('----------------------------------------------------------------------------------------------------')

df = pd.read_csv('C:/Users/Tibame_25/Desktop/vessel.csv',encoding='big5')

df["GPS時間"] = pd.to_datetime(df["GPS時間"], format='%Y/%m/%d %H:%M:%S') 

df_group = df.groupby("中文船名")

for q in vessel_list:
    try:
        df2 = df_group.get_group(q)
        df2 = df2.sort_values("GPS時間",ignore_index=True,ascending=False) 
        print()
        print(q)
        for x in range(0,1):
            for r in range(1,99):
                if df2["GPS時間"][0]+timedelta(minutes=30) < datetime.strptime("2021-05-04", "%Y-%m-%d") :
                    if df2["GPS時間"][x]+timedelta(minutes=30)*r < datetime.strptime("2021-05-04", "%Y-%m-%d") : 
                        print(df2["GPS時間"][x]+timedelta(minutes=30)*r)             
                        new_column_lst = []
                        new_column_lst.append({"中文船名":df["中文船名"][0],"GPS時間":df["GPS時間"][x]+timedelta(minutes=30)})
                        df2 = df2.append(new_column_lst)
                        df2 = df2.sort_values("GPS時間",ignore_index=True,ascending=False) 
    except KeyError as e:
        print()
        print(q)
        print("查無資料")