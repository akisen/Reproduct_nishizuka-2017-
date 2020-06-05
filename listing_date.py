"""
fitsファイルの中の撮影日を出力するスクリプト。
データセットをNASに上げる前に漏れがないか確認するようにする
ex)python3 listing_date.py "/media/akito/Data/Dataset/SHARP(CEA)/2010*/*000000*Bp.fits" >2010.txt
注意:活動が余り活発な時期でないときには途中のデータが抜けている場合もある→普通に期間で取り出していれば
"""
import sys
import glob
import sunpy.map

args=sys.argv
paths=sorted(glob.glob(args[1]))
dates=[]
for path in paths:
    map=sunpy.map.Map(path)
    date=(str(map.meta["t_rec"])).replace("_00:00:00_TAI","")
    if (date not in dates):
        dates.append(date)
[print(date) for date in sorted(dates)]
