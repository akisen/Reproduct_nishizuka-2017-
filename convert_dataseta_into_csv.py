"""
SHARP,Cgem.lorentzのデータセットから必要なデータを抽出する関数
データセットを入力してメタデータからCSVファイルを生成する
第一引数:SHARPのデータセットがあるディレクトリのパス
第二引数:cgem.Lorentzのデータセットが格納してあるディレクトリのパス
第三引数:CSVファイルのパス
"""
import csv 
import sunpy.map
import glob
import sys
import pandas as pd
import os
def reading_sharp(SHARP_Path):
    keys = ["t_rec","totusjh","totusjz","absnjzh","savncpp","usflux","area_acr","meangam","meangbt","meangbz","meangbh","meanjzh","meanjzd"]
    sharp_path_obj = sorted(glob.glob(SHARP_Path))
    sharp_datas =pd.DataFrame([keys])
    for index,data in enumerate(sharp_path_obj):
        map =sunpy.map.Map(data)
        row=[]
        for key in keys:
            # print(str(key)+str(map.meta[key]))

            row.append(str(map.meta[key]))
        sharp_datas=sharp_datas.append([row])
    return sharp_datas


def main():
    args = sys.argv
    SHARP_Path = args[1]
    # CGEM_Path = args[2]
    CSV_Path = args[2]
    reading_sharp(SHARP_Path).to_csv(CSV_Path) 
if __name__ == "__main__":
    main()