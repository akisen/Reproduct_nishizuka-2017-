import sunpy.map
import pandas as pd
import glob
from tqdm import tqdm
import sys 
from datetime import datetime as dt
import datetime
import numpy as np 
import pickle
import os
def extract_sharp_features(SHARP_Path):
    feature_list = ["harpnum","totusjh","totusjz","absnjzh","savncpp","usflux","area_acr","meangam","meangbt","meangbz","meangbh","meanjzh","meanjzd","latdtmin","latdtmax","londtmin","londtmax"]
    if(os.path.exists("physical_feature/sharp_dfs.pickle")):
        sharp_dfs=pickle_load("physical_feature/sharp_dfs.pickle")
    else:
        sharp_dfs={}
    sharp_list = sorted(glob.glob(SHARP_Path))
    ar_time_dic={} #同じHARP番号のファイルを格納する辞書
    for path in sharp_list:
        ar_num = path.split(".")[2]
        record_time = path.split(".")[3]
        record_time=dt.strptime(record_time.replace("_TAI",""),"%Y%m%d_%H%M%S")#比較しやすいように時間型に変換
        ar_time_dic.setdefault(ar_num,[]).append(record_time) #HARP番号をキーとして記録時間の一覧をリストで格納
    for rec_time_list in ar_time_dic.values():
        rec_time_list.sort() #観測時間のリストを初期化することによって最初に初めて観測した時間、最後に観測し終わった時間が来るように
    for ar_num,rec_time_list in ar_time_dic.items():
        
        rec_time =rec_time_list[0]
        time_list =[rec_time]
        while (rec_time!=rec_time_list[-1]): #初観測時間から最終観測時間までのリストを作成
            rec_time = rec_time+datetime.timedelta(hours=1) #ケイデンスによって調整の必要あり
            time_list.append(rec_time)
        sharp_df = pd.DataFrame(0,index = time_list,columns=feature_list) #データフレームの初期化(0埋め)
        if (int(ar_num) in sharp_dfs.keys()):
            sharp_dfs[int(ar_num)]=sharp_dfs[int(ar_num)].append(sharp_df)
        else:
            sharp_dfs[int(ar_num)]=sharp_df #HARP番号をキーにした辞書を作成し、1ARにつきひとつのDataFrameを紐づける
    
    for path in tqdm(sharp_list):
        map = sunpy.map.Map(path)
        ar_num_key=map.meta["harpnum"]
        ar_num_path = int(path.split(".")[2])
        record_time = path.split(".")[3]
        record_time=dt.strptime(record_time.replace("_TAI",""),"%Y%m%d_%H%M%S")#比較しやすいように時間型に変換
        for feature in feature_list:
            sharp_dfs[ar_num_path][feature][record_time]=str(map.meta[feature])
    return sharp_dfs
def extract_cgem_features(CGEM_Path):
    feature_list=["harpnum","t_rec","totbsq","totfz","epsz","totfy","totfx","epsy","epsx"]
    if(os.path.exists("physical_feature/cgem_dfs.pickle")):
        cgem_dfs=pickle_load("physical_feature/cgem_dfs.pickle")
    else:
        cgem_dfs={}
    cgem_list = sorted(glob.glob(CGEM_Path))
    ar_time_dic={} #同じHARP番号のファイルを格納する辞書
    for path in cgem_list:
        ar_num = path.split(".")[3]
        record_time = path.split(".")[4]
        record_time=dt.strptime(record_time.replace("_TAI",""),"%Y%m%d_%H%M%S")#比較しやすいように時間型に変換
        ar_time_dic.setdefault(ar_num,[]).append(record_time) #HARP番号をキーとして記録時間の一覧をリストで格納
    for rec_time_list in ar_time_dic.values():
        rec_time_list.sort() #観測時間のリストを初期化することによって最初に初めて観測した時間、最後に観測し終わった時間が来るように
    for ar_num,rec_time_list in ar_time_dic.items():
        rec_time =rec_time_list[0]
        time_list =[rec_time]
        while (rec_time!=rec_time_list[-1]): #初観測時間から最終観測時間までのリストを作成
            rec_time = rec_time+datetime.timedelta(hours=1) #ケイデンスによって調整の必要あり
            time_list.append(rec_time)
        cgem_df = pd.DataFrame(0,index = time_list,columns=feature_list) #データフレームの初期化(0埋め)
        if(int(ar_num) in cgem_dfs.keys()):
            cgem_dfs[int(ar_num)]=cgem_dfs[int(ar_num)].append(cgem_df)
        else:
            cgem_dfs[int(ar_num)]=cgem_df #HARP番号をキーにした辞書を作成し、1ARにつきひとつのDataFrameを紐づける
    # print(cgem_dfs)
    for path in tqdm(cgem_list):
        map = sunpy.map.Map(path)
        ar_num_key=map.meta["harpnum"]
        ar_num_path = int(path.split(".")[3])
        record_time = path.split(".")[4]
        record_time=dt.strptime(record_time.replace("_TAI",""),"%Y%m%d_%H%M%S")#比較しやすいように時間型に変換
        for feature in feature_list:
            cgem_dfs[ar_num_path][feature][record_time]=str(map.meta[feature])
    # print(cgem_dfs)
    return cgem_dfs
def merge_df(sharp_dfs,cgem_dfs):
    merged_dfs={}
    for key,value in sharp_dfs.items():
        if(key in cgem_dfs.keys()):
            merged_dfs[key]=pd.concat([sharp_dfs[key],cgem_dfs[key]],axis=1)
        else:
            print(str(key)+" unmatched")
    print(merged_dfs)
    return merged_dfs
def pickle_dump(obj, path):
    with open(path, mode='wb') as f:
        pickle.dump(obj,f)
def pickle_load(path):
    with open(path, mode='rb') as f:
        data = pickle.load(f)
        return data
def save_as_pickle(sharp_dfs,cgem_dfs,merged_dfs):
    pickle_dump(sharp_dfs,"physical_feature/sharp_dfs.pickle")
    pickle_dump(cgem_dfs,"physical_feature/cgem_dfs.pickle")
    pickle_dump(merged_dfs,"physical_feature/merged_dfs.pickle")
def main():
    args = sys.argv
    SHARP_Path = args[1]
    CGEM_Path = args[2]
    CSV_Path = args[3]
    sharp_dfs =extract_sharp_features(SHARP_Path)
    cgem_dfs = extract_cgem_features(CGEM_Path)
    merged_dfs = merge_df(sharp_dfs,cgem_dfs)
    save_as_pickle(sharp_dfs,cgem_dfs,merged_dfs)
    # merged_df.to_csv(CSV_Path)
if __name__ == "__main__":
    main()
