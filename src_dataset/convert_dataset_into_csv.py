"""
SHARP,Cgem.lorentzのデータセットから必要なデータを抽出する関数
データセットを入力してメタデータからCSVファイルを生成する
第一引数:SHARPのデータセットがあるディレクトリのパス
第二引数:cgem.Lorentzのデータセットが格納してあるディレクトリのパス
第三引数:CSVファイルのパス
ex)python3 convert_dataset_into_csv.py "/media/akito/Data/Dataset/SHARP(CEA)/2010/201005/*Bp.fits" "/media/akito/Data/Dataset/Cgem.Lorentz/2010/201005/*.Fx.fits" "physical201005.csv"
"""
import csv  
import sunpy.map
import glob
import sys
import pandas as pd
import os
from tqdm import tqdm
def reading_dataset(SHARP_Path,CGEM_Path):
    sharp_keys = ["harpnum","t_rec","totusjh","totusjz","absnjzh","savncpp","usflux","area_acr","meangam","meangbt","meangbz","meangbh","meanjzh","meanjzd","latdtmin","latdtmax","londtmin","londtmax"]
    cgem_keys = ["harpnum","t_rec","totbsq","totfz","epsz","totfy","totfx","epsy","epsx"]
    sharp_path_obj = sorted(glob.glob(SHARP_Path))
    cgem_path_obj =sorted(glob.glob(CGEM_Path))
    sharp_datas =pd.DataFrame([sharp_keys])
    cgem_datas = pd.DataFrame([cgem_keys])
    size_of_data=len(sharp_path_obj)+len(cgem_path_obj)
    print(len(sharp_path_obj))
    print(len(cgem_path_obj))
    with tqdm(total = size_of_data) as pbar:
        for sharp_data in sharp_path_obj:
            print("sharp")
            pbar.update(1)
            sharp_map =sunpy.map.Map(sharp_data)
            sharp_row=[]
            for key in sharp_keys:
                # print(str(key)+str(map.meta[key]))
                sharp_row.append(str(sharp_map.meta[key]))
            if(set(sharp_row[2:14])!={'0.0'} or (set(sharp_row[2:14])=={'0.0', '-nan'})):# すべての要素が0の行を弾く
                sharp_datas=sharp_datas.append([sharp_row])
        for cgem_data in cgem_path_obj:
            pbar.update(1)
            cgem_map =sunpy.map.Map(cgem_data)
            cgem_row=[]
            # print(set(row[2:14])=={'0.0', '-nan'})
            for key in cgem_keys:
                cgem_row.append(str(cgem_map.meta[key]))
            # if (sharp_map.meta["t_rec"]!=cgem_map.meta["t_rec"]):
            #     print(row)
            #     exit()
            print("cgem")
            cgem_datas=cgem_datas.append([cgem_row])
        merged_datas = pd.concat([sharp_datas,cgem_datas],axis=1)
    return merged_datas

def main():
    args = sys.argv
    SHARP_Path = args[1]
    CGEM_Path = args[2]
    CSV_Path = args[3]
    # print(reading_dataset(SHARP_Path,CGEM_Path))
    reading_dataset(SHARP_Path,CGEM_Path).to_csv(CSV_Path,index=False,header=False) 
if __name__ == "__main__":
    main()