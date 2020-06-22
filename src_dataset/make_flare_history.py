"""
フレアデータベースをもとにデータセットを作成するスクリプト
第1引数: 作成するデータの種類 0→全部のデータからM以上を抽出 →M以上のデータから学習に使用する用のデータを作成

"""

import time
import pandas as pd
import numpy as np
from tqdm import tqdm
import sys
import sunpy.map
import glob
from tqdm import tqdm
import datetime
from datetime import timedelta
def make_huge_flare_database (flare_df):
    """
    M,Xクラスのみのフレアデータ(csv)を作成する関数
    """
    flare_df["flare_24h"] = 0
    flare_df["longitude"] = 0
    for i in tqdm(range (len(flare_df))):
        if(flare_df["GOES Class"][i][0]=="A" or flare_df["GOES Class"][i][0]=="B"):

            flare_df=flare_df.drop(i,axis=0)
    return flare_df
def make_ar_csv(fits_path):
    print("Make Active Region list from fits files.")
    indexs=["harpnum","t_rec","noaa_ars","latdtmin","londtmin","latdtmax","londtmax"]
    ar_csv=pd.DataFrame(columns=indexs)
    sorted_path = sorted(glob.glob(fits_path))
    for path in tqdm(sorted_path):
        row=[]
        map=sunpy.map.Map(path)
        for index in indexs:
            if index =="harpnum":
                row.append(str(map.meta[index]).zfill(4))
            else:
                row.append(map.meta[index])
        ar_csv=ar_csv.append([row])
    return ar_csv
def make_flare_history(ar_coordinate_df,flare_df,flare_history_df):
    flare_df = flare_df.drop("Events",axis=1)
    flare_df = flare_df.drop_duplicates()
    flare_df = flare_df.reset_index(drop=True)
    # sharp,lorentzのデータから抽出したメタデータのデータフレームを取りだし、観測時刻を演算可能なDatetime型に変換する
    for i in range(len(flare_history_df)-1):
        rec_time_str = flare_history_df["1"][i+1]
        flare_history_df["1"][i+1] = datetime.datetime(int(rec_time_str[0:4]),int(rec_time_str[5:7]),int(rec_time_str[8:10]),int(rec_time_str[11:13]),int(rec_time_str[14:16]),int(rec_time_str[17:19]))
        flare_history_df["Mflare_flag"]=0 #フレア発生のフラグを初期化
        flare_history_df["Xflare_flag"]=0
    print(flare_history_df[1:2])
    # ARの座標データから抽出したメタデータのデータフレームを取りだし、観測時刻を演算可能なDatetime型に変換する
    for i in range(len(ar_coordinate_df)):
        ar_time_str = ar_coordinate_df["t_rec"][i]
        ar_coordinate_df["t_rec"][i] = datetime.datetime(int(ar_time_str[0:4]),int(ar_time_str[5:7]),int(ar_time_str[8:10]),int(ar_time_str[11:13]),int(ar_time_str[14:16]),int(ar_time_str[17:19]))
    # print(ar_coordinate_df.sort_values("harp_num").sort_values("t_rec")[0:1])
    for i in range(len(flare_df)):
        flare_df["Start"][i] = datetime.datetime.strptime(flare_df["Start"][i],"%Y-%m-%d %H:%M:%S")
    # print(datetime.datetime.strptime(flare_df["Start"][0],"%Y/%m/%d %H:%M:%S"))
    """
    以下の条件文ではフレアが発生している日時を取り出し、座標をもとにどこのARでフレアが発生したか判断する。
    Index="flare_flug"にはフレアが発生した場合Event番号が、そうでない場合0が入る
    """
    # print([index for index in flare_df.index.values])
    print(len(flare_df.index.values))
    indexs = set(flare_df.index.values)
    print(len(flare_df))
    for i in indexs:
        # print(flare_df["Derived Position"][i])
        if((flare_df["Derived Position"][i][1:3])!="**"):
            # print(flare_df["Derived Position"][i][0])
            lat = (int(flare_df["Derived Position"][i][1:3]) if flare_df["Derived Position"][i][0]=="N" else -1*int(flare_df["Derived Position"][i][1:3]))
            # print(flare_df["Derived Position"][i][3])
            lon = (int(flare_df["Derived Position"][i][4:6]) if flare_df["Derived Position"][i][3]=="W" else -1*int(flare_df["Derived Position"][i][4:6]))
        else:
            flare_df=flare_df.drop(i)
        # print("lat:"+str(lat)+"lon:"+str(lon))
        
        # print(indexs)
    flare_df = flare_df.reset_index(drop=True)
    indexs = set(flare_df.index.values)
    for i in tqdm(indexs):
        # print(flare_df["Start"][i])
        for k in range(len(flare_history_df)-1):
            if((flare_history_df["1"][k+1] <= flare_df["Start"][i]<(flare_history_df["1"][k+1]+timedelta(hours=1)))and (float(flare_history_df["16"][k+1])<=lon<float(flare_history_df["17"][k+1]))):
                if(flare_df["GOES Class"][i][0]=="M"):
                    if(flare_history_df["Mflare_flag"][k+1] == int("0")):
                        flare_history_df["Mflare_flag"][k+1]=flare_df["EName"][i]
                        print(flare_history_df["Mflare_flag"][k+1])
                    else:
                        flare_history_df["Mflare_flag"][k+1]=flare_history_df["Mflare_flag"][i+1]+","+flare_df["EName"][i]
                        print(flare_history_df["Mflare_flag"][k+1])
                elif(flare_df["GOES Class"][i][0]=="X"):
                    if(flare_history_df["Xflare_flag"][k+1] == int("0")):
                        flare_history_df["Xflare_flag"][k+1]=flare_df["EName"][i]
                        print(flare_history_df["Xflare_flag"][k+1])
                    else:
                        flare_history_df["Xflare_flag"][k+1]=flare_history_df["Xflare_flag"][i]+","+flare_df["EName"][i]
                        print(flare_history_df["Xflare_flag"][k+1])
                else:
                    print("Unexpected data")
    print([index for index in flare_df.index.values])
    return flare_history_df

def main():
    args = sys.argv
    flare_database_path = args[2]
    flare_df =pd.read_csv(flare_database_path)
    ar_coordinate_path = args[3]
    ar_coordinate_df = pd.read_csv(ar_coordinate_path)
    ar_phisical_features_path = args[4]
    ar_phisical_features_df = pd.read_csv(ar_phisical_features_path)
    if args[1]=="0":
        flare_df = flare_df.drop_duplicates()
        flare_df["Start"]=pd.to_datetime(flare_df["Start"])
        flare_df["Derived Position"] = flare_df["Derived Position"].str.replace(" ","")
        make_huge_flare_database(flare_df).to_csv("C_Flare_database.csv")
    elif args[1]=="1":
        make_flare_history(ar_coordinate_df,flare_df,ar_phisical_features_df).to_csv("sharp_test201005.csv")
    elif args[1]=="2":
        ((make_ar_csv(args[2]).sort_values(1)).sort_values(0)).to_csv("ar_coordinate_list.csv", header=False,index=False)
if __name__ == "__main__":
    main()

