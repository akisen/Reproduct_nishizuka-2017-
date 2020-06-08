"""
NOAAのデータベースから太陽フレアのデータをダウンロードするためのスクリプト
"""
from bs4 import BeautifulSoup
from urllib import request
import requests
import re
import csv
from tqdm import tqdm
url = "https://www.lmsal.com/solarsoft/latest_events_archive.html"
r = requests.get(url)
soup = BeautifulSoup(r.text,"html.parser")
elems = soup.find_all(href=re.compile("ssw/last_events"))
rows=["Events","EName","Start","Stop","peak","GOES Class","Derived Position"]
    
with tqdm(total = len(elems)) as pbar:
    for elem in elems[0:10]:
        pbar.update(1)
        # print(elem.attrs["href"])
        res = requests.get("https://www.lmsal.com/solarsoft/"+str(elem.attrs["href"]))
        # print(res)
        soup =BeautifulSoup(res.text,"html.parser")
        table = soup.find_all("table")
        try:
            table
            data=table[-1].find_all("td")
        except NameError:
            continue
        row =[column.text for column in data]
        for i in range(len(row)//7):
            
            r=row[i*7:(i*7+6)]
            rows.append(r)
            # print(r)
    
with open("flare_database.csv","w") as f:
    writer =csv.writer(f)
    writer.writerows(rows)