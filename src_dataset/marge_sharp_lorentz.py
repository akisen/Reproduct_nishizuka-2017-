import sunpy.map
import pandas as pd
import glob
from tqdm import tqdm
import sys 
from datetime import datetime as dt
def extract_sharp_features(SHARP_Path):
    sharp_df=[]
    sharp_list = sorted(glob.glob(SHARP_Path))
    ar_dic={} #同じHARP番号のファイルを格納する辞書
    for path in sharp_list:
        ar_num = path.split(".")[2]
        record_time = path.split(".")[3]
        record_time=dt.strptime(record_time.replace("_TAI",""),"%Y%m%d_%H%M%S")#比較しやすいように時間型に変換
        ar_dic.setdefault(ar_num,[]).append(record_time) #HARP番号をキーとして記録時間の一覧をリストで格納
    for rec_time_list in ar_dic.values():
        rec_time_list.sort() #観測時間のリストを初期化することによって最初に初めて観測した時間、最後に観測し終わった時間が来るように
        print(rec_time_list)
    # for rec_time_list in ar_dic.values():
        
        
    print(ar_dic)
        
    return sharp_df

def extract_cgem_features(CGEM_Path):
    cgem_df=[]
    cgem_list = sorted(glob.glob(CGEM_Path))
    # print([path for path in cgem_list])
    return cgem_df
def marge_df(sharp_df,cgem_df):
    marged_df=pd.concat([sharp_df, cgem_df],axis=1)
    
    return marged_df

def main():
    args = sys.argv
    SHARP_Path = args[1]
    CGEM_Path = args[2]
    CSV_Path = args[3]
    sharp_df =extract_sharp_features(SHARP_Path)
    cgem_df = extract_cgem_features(CGEM_Path)
    # marged_df=
    marged_df =pd.DataFrame([])
    marged_df.to_csv(CSV_Path)
if __name__ == "__main__":
    main()
