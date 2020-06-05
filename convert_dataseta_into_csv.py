"""
SHARP,Cgem.lorentzのデータセットから必要なデータを抽出する関数
データセットを入力してメタデータからCSVファイルを生成する
第一引数:SHARPのデータセットがあるディレクトリのパス
第二引数:cgem.Lorentzのデータセットが格納してあるディレクトリのパス
第三引数:CSVファイルのパス
ex)
"""
import csv 
import sunpy.map
import glob
import sys
import pandas as pd
import os
from tqdm import tqdm
def reading_dataset(SHARP_Path,CGEM_Path):
    sharp_keys = ["t_rec","totusjh","totusjz","absnjzh","savncpp","usflux","area_acr","meangam","meangbt","meangbz","meangbh","meanjzh","meanjzd"]
    cgem_keys = ["totbsq","totfz","epsz","totfy","totfx","epsy","epsx"]
    sharp_path_obj = sorted(glob.glob(SHARP_Path))
    cgem_path_obj =sorted(glob.glob(CGEM_Path))
    datas =pd.DataFrame([sharp_keys+cgem_keys])
    size_of_data=len(sharp_path_obj)
    with tqdm(total = size_of_data) as pbar:
        for sharp_data,cgem_data in zip(sharp_path_obj,cgem_path_obj):
            pbar.update(1)
            sharp_map =sunpy.map.Map(sharp_data)
            cgem_map =sunpy.map.Map(cgem_data)
            row=[]
            for key in sharp_keys:
                # print(str(key)+str(map.meta[key]))
                row.append(str(sharp_map.meta[key]))
            for key in cgem_keys:
                row.append(str(cgem_map.meta[key]))
            datas=datas.append([row])
    return datas


def main():
    args = sys.argv
    SHARP_Path = args[1]
    CGEM_Path = args[2]
    CSV_Path = args[3]
    reading_dataset(SHARP_Path,CGEM_Path).to_csv(CSV_Path) 
if __name__ == "__main__":
    main()