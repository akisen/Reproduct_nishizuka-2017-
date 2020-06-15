"""
フレアデータベースをもとにデータセットを作成するスクリプト
第一引数: 作成するデータの種類 0→全部のデータからM以上を抽出 1→M以上のデータから学習に使用する用のデータを作成
第2引数: 作成するデータの年(Start)
第3引数: 作成するデータの月(Start)
第4引数: 作成するデータの年(End)
第5引数: 作成するデータの月(End)
"""

import time
import pandas as pd
import numpy as np
from tqdm import tqdm
import sys
def make_huge_flare_database (flare_df):
    flare_df["flare_24h"] = 0
    flare_df["longitude"] = 0
    for i in tqdm(range (len(flare_df))):
        if(flare_df["GOES Class"][i][0]=="A" or flare_df["GOES Class"][i][0]=="B" or flare_df["GOES Class"][i][0]=="C"):

            flare_df=flare_df.drop(i,axis=0)
    return flare_df
def make_flare_csv (flare_df, start_year, start_month, end_year, end_month):
    flare_history_df = pd.DataFrame(["his"])
    return flare_history_df

def main():
    args = sys.argv
    flare_database_name = "Huge_Flare_database.csv"
    flare_df =pd.read_csv(flare_database_name)
    if args[1]==0:
        flare_df = flare_df.drop_duplicates()
        flare_df["Start"]=pd.to_datetime(flare_df["Start"])
        flare_df["Derived Position"] = flare_df["Derived Position"].str.replace(" ","")
        make_huge_flare_database(flare_df).to_csv("flare_database/Huge_Flare_database.csv")
    elif args[1]==1:
        make_flare_csv(flare_df,args[2],args[3],args[4],args[5]).to_csv
if __name__ == "__main__":
    main()

