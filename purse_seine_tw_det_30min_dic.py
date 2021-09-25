import pandas as pd
import time
import collections
from datetime import datetime, date, time, timedelta
import os

empty_dict = collections.defaultdict(list)

def pursine(df, GPStime_column_name, vessel_column_name, vessel_list, check_time) :
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
                            # print(df[GPStime_column_name][e]+timedelta(minutes=30),df[GPStime_column_name][e]+timedelta(minutes=30)*2)
                            empty_dict[i].append(str(df[GPStime_column_name][e] + timedelta(minutes=30)))
                            empty_dict[i].append(str(df[GPStime_column_name][e] + timedelta(minutes=30)* 2))
                            for r in range(3,9999):
                                if df[GPStime_column_name][e]+timedelta(minutes=30)*r < df[GPStime_column_name][e+1] :
                                    # print(df[GPStime_column_name][e]+timedelta(minutes=30)*r)
                                    empty_dict[i].append(str(df[GPStime_column_name][e] + timedelta(minutes=30) * r))
                                else:
                                    continue
                    else:
                        continue
                except (ValueError,KeyError):
                    pass
        except KeyError as e:
            print()
            print(i)
            # print("NO Data")
            empty_dict[i].append('NO Data')


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
                for r in range(2,9999):
                    if df3[GPStime_column_name][0]+timedelta(minutes=30) < datetime.strptime(check_time, "%Y-%m-%d") :
                        if df3[GPStime_column_name][0]+timedelta(minutes=30)*r < datetime.strptime(check_time, "%Y-%m-%d") :
                            # print(df3[GPStime_column_name][x]+timedelta(minutes=30)*r)
                            empty_dict[q].append(str(df3[GPStime_column_name][x]+timedelta(minutes=30)*r))
                            new_column_lst = []
                            new_column_lst.append({vessel_column_name:df2[vessel_column_name][0],GPStime_column_name:df2[GPStime_column_name][x]+timedelta(minutes=30)})
                            df3 = df3.append(new_column_lst)
                            df3 = df3.sort_values(GPStime_column_name,ignore_index=True,ascending=False)
        except KeyError as e:
            print()
            print(q)
            # print("NO Data")
            empty_dict[q].append('NO Data')
    return empty_dict

if __name__ == '__main__':
    vessel_list = list(("裕穩101", "裕穩301", "百富103", "百富301", "大慶666", "慶豐787", "慶豐767",
                        "日友168", "日友768", "日友668", "日友868", "日友968", "日友568", "豐國188", "豐國189", "豐國828", "豐國866",
                        "豐國889", "豐國688", "協豐788", "協豐789", "華偉707", "興富華707", "興成發707", "興華發707", "興旺發707", "興永發707",
                        "富冠808", "穩發626", "穩發666", "穩發618", "穩發636"))

    GPStime_column_name = 'GPS時間'
    vessel_column_name = '中文船名'
    check_time = '2021-09-24' # 輸入查詢日期
    df = pd.read_csv('./vessel.csv', encoding='big5', engine='python')
    pursine(df=df,GPStime_column_name=GPStime_column_name, vessel_column_name=vessel_column_name, vessel_list=vessel_list, check_time=check_time)
    # print(empty_dict)
    folderpath = "./vessel_record"  # 建立目錄用的
    datetime_dt = datetime.today()  # 獲得當地時間
    datetime_str = datetime_dt.strftime("%Y-%m-%d-%H-%M-%S")  # 格式化日期
    restore_time = datetime_str # 建立檔案名稱用的

    # 開始建立目錄
    try:
        os.makedirs(folderpath)
    # 檔案已存在的例外處理
    except FileExistsError:
        print("目錄已存在。")

    # 開始建立儲存資料的檔案名稱
    fname = './vessel_record/check_date_{time}.txt'.format(time=restore_time)

    with open(fname, 'a') as fp:
        number = 1
        for name in empty_dict:
            fp.write("\n\n")
            fp.write(name)
            fp.write("\n")
            for detail in empty_dict[name]:
                if number == 0:
                    fp.write(detail)
                    fp.write(',')
                    fp.write(" ")
                    number +=1
                elif detail == 'NO Data':
                    fp.write(detail)
                    fp.write(',')
                    fp.write(" ")
                    number = 1
                elif empty_dict[name].index(detail) == len(empty_dict[name]) - 1:
                    fp.write(detail)
                    number = 1
                elif number % 8 == 0:
                    fp.write(detail)
                    fp.write(',')
                    fp.write("\n")
                    number +=1
                else:
                    fp.write(detail)
                    fp.write(',')
                    fp.write(" ")
                    number +=1