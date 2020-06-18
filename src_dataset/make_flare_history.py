"""
フレアデータベースをもとにデータセットを作成するスクリプト
第1引数: 作成するデータの種類 0→全部のデータからM以上を抽出 2→M以上のデータから学習に使用する用のデータを作成

"""

import time
import pandas as pd
import numpy as np
from tqdm import tqdm
import sys
import sunpy.map
import glob
from tqdm import tqdm
def make_huge_flare_database (flare_df):
    """
    M,Xクラスのみのフレアデータ(csv)を作成する関数
    """
    flare_df["flare_24h"] = 0
    flare_df["longitude"] = 0
    for i in tqdm(range (len(flare_df))):
        if(flare_df["GOES Class"][i][0]=="A" or flare_df["GOES Class"][i][0]=="B" or flare_df["GOES Class"][i][0]=="C"):

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
def make_flare_history(ar_coordinate_list,flare_list):
    return 

def main():
    args = sys.argv
    flare_database_name = "../Huge_Flare_database.csv"
    if args[1]=="0":
        flare_df = flare_df.drop_duplicates()
        flare_df["Start"]=pd.to_datetime(flare_df["Start"])
        flare_df["Derived Position"] = flare_df["Derived Position"].str.replace(" ","")
        make_huge_flare_database(flare_df).to_csv("flare_database/Huge_Flare_database.csv")
    elif args[1]=="1":
        make_flare_csv()).to_csv
    elif args[1]=="2":
        (make_ar_csv(args[2]).sort_values(0)).to_csv("ar_coordinate_list.csv", index=False)
if __name__ == "__main__":
    main()

