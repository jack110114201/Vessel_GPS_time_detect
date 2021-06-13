import pandas as pd
import time
from datetime import datetime, date, time, timedelta

vessel_list = list(("裕穩101","裕穩301","百富103","百富301","大慶666","慶豐787","慶豐767",
                "日友168","日友768","日友668","日友868","日友968","日友568","豐國188","豐國189","豐國828","豐國866",
                "豐國889","豐國688","協豐788","協豐789","華偉707","興富華707","興成發707","興華發707","興旺發707","興永發707",
                "富冠808","穩發626","穩發666","穩發618","穩發636"))

GPStime_column_name ='GPS時間'
vessel_column_name = '中文船名'
df = pd.read_csv('C:/Users/Tibame_25/Desktop/vessel.csv',encoding = 'big5',engine='python')


def pursine(df=df,GPStime_column_name=GPStime_column_name, vessel_column_name=vessel_column_name, vessel_list=vessel_list):
    df2 = df.copy()
    df[GPStime_column_name] = pd.to_datetime(df[GPStime_column_name], format='%Y/%m/%d %H:%M:%S') 
    df_group = df.groupby(vessel_column_name)
    for i in vessel_list:
        try:
            df = df_group.get_group(i)
            print()
            print(i)
            for e in range(0,9999):  # 有成功
                try:
                    if df[GPStime_column_name][e]+timedelta(minutes=30) < df[GPStime_column_name][e+1] :
                        if df[GPStime_column_name][e]+timedelta(minutes=30)*2 < df[GPStime_column_name][e+1] :
                            print(df[GPStime_column_name][e]+timedelta(minutes=30),df[GPStime_column_name][e]+timedelta(minutes=30)*2)
                            for r in range(3,9999):
                                if df[GPStime_column_name][e]+timedelta(minutes=30)*r < df[GPStime_column_name][e+1] :
                                    print(df[GPStime_column_name][e]+timedelta(minutes=30)*r)
                                    new_column_lst = [] 
                                    new_column_lst.append({vessel_column_name:df[vessel_column_name][0],GPStime_column_name:df[GPStime_column_name][e]+timedelta(minutes=30)})
                                    new_column_lst.append({vessel_column_name:df[vessel_column_name][0],GPStime_column_name:df[GPStime_column_name][e]+timedelta(minutes=30)*2})
                                    new_column_lst.append({vessel_column_name:df[vessel_column_name][0],GPStime_column_name:df[GPStime_column_name][e]+timedelta(minutes=30)*r})
                                    df = df.append(new_column_lst)
                                    df = df.sort_values(GPStime_column_name,ignore_index=True) #新增資料後，排序，並修改原本的df
                                else:
                                    break      
                    else:
                        continue
                except (ValueError,KeyError):
                    pass
        except KeyError as e:
            print()
            print(i)
            print("NO Data")

    print('----------------------------------------------------------------------------------------------------')

    df2[GPStime_column_name] = pd.to_datetime(df2[GPStime_column_name], format='%Y/%m/%d %H:%M:%S') 

    df2_group = df2.groupby(vessel_column_name)

    for q in vessel_list:
        try:
            df3 = df2_group.get_group(q)
            df3 = df3.sort_values(GPStime_column_name,ignore_index=True,ascending=False) 
            print()
            print(q)
            for x in range(0,1):
                for r in range(1,48):
                    if df3[GPStime_column_name][0]+timedelta(minutes=30) < datetime.strptime("2021-05-04", "%Y-%m-%d") :
                        if df3[GPStime_column_name][x]+timedelta(minutes=30)*r < datetime.strptime("2021-05-04", "%Y-%m-%d") : 
                            print(df3[GPStime_column_name][x]+timedelta(minutes=30)*r)             
                            new_column_lst = []
                            new_column_lst.append({vessel_column_name:df2[vessel_column_name][0],GPStime_column_name:df2[GPStime_column_name][x]+timedelta(minutes=30)})
                            df3 = df3.append(new_column_lst)
                            df3 = df3.sort_values(GPStime_column_name,ignore_index=True,ascending=False) 
        except KeyError as e:
            print()
            print(q)
            print("NO Data")

if __name__ == '__main__':
    pursine(df=df,GPStime_column_name=GPStime_column_name, vessel_column_name=vessel_column_name, vessel_list=vessel_list)