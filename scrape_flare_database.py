"""
NOAAのデータベースから太陽フレアのデータをダウンロードするためのスクリプト
URL=https://www.lmsal.com/solarsoft/latest_events_archive.html
"""
from bs4 import BeautifulSoup
from urllib import request
import requests
import re
import csv
from tqdm import tqdm
import sys
args =sys.argv
url = "https://www.lmsal.com/solarsoft/latest_events_archive.html"
r = requests.get(url)
soup = BeautifulSoup(r.text,"html.parser")
elems = soup.find_all(href=re.compile("ssw/last_events"))
rows=[["Events","EName","Start","Stop","peak","GOES Class","Derived Position"]]
number=int(args[1])*100
with tqdm(total = 100) as pbar:
    for elem in elems[number:number+100]:
        pbar.update(1)
        # print(elem.attrs["href"])
        res = requests.get("https://www.lmsal.com/solarsoft/"+str(elem.attrs["href"]))
        # print(res)
        soup =BeautifulSoup(res.text,"html.parser")
        table = soup.find_all("table")
        if(table!=[]):
            data=table[-1].find_all("td")
        else:
            continue
        row =[column.text for column in data]
        for i in range(len(row)//7):
            
            r=row[i*7:(i*7+7)]
            rows.append(r)
            # print(r)
csvfile="flare_database/flare_database"+args[1].zfill(2)+".csv"
with open(csvfile,"w") as f:
    writer =csv.writer(f)
    writer.writerows(rows)