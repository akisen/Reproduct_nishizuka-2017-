import time
import pandas as pd
import numpy as np
from tqdm import tqdm
flare_database_name = "Huge_Flare_database.csv"
flare_df =pd.read_csv(flare_database_name)
flare_df = flare_df.drop_duplicates()
flare_df["Start"]=pd.to_datetime(flare_df["Start"])
flare_df["Derived Position"] = flare_df["Derived Position"].str.replace(" ","")
# print(flare_df["Start"])
def initialize_coordinate (flare_df):
    flare_df["flare_24h"] = 0
    flare_df["longitude"] = 0
    for i in tqdm(range (len(flare_df))):
        if(flare_df["GOES Class"][i][0]=="A" or flare_df["GOES Class"][i][0]=="B" or flare_df["GOES Class"][i][0]=="C"):

            flare_df=flare_df.drop(i,axis=0)
    flare_df.to_csv("Huge_Flare_database.csv")        
initialize_coordinate(flare_df)

