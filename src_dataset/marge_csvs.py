"""
ダウンロード制限等の関係でバラバラになっているCSVファイルを一つに結合するプログラム
→注意:pathを正規表現で与えて結合する際に順番がめちゃくちゃにならないようにZero Paddingを忘れないようにする
第1引数:結合したいファイルのパス(連番でできるように正規表現で入力)
第2引数:出力ファイルの名前
"""
import sys
import time
import glob
import pandas as pd
args=sys.argv
path_str = args[1]
path_obj = sorted(glob.glob(path_str))
df = pd.DataFrame([])
for path in path_obj:
    df = df.append(pd.read_csv(path))
df = df.drop_duplicates()
df.to_csv(args[2])
