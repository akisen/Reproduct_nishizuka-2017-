import time
import pandas as pd
flare_database_name = "flare_database/flare_database0.csv"
flare_df =pd.read_csv(flare_database_name)
flare_df = flare_df.drop_duplicates()
flare_df["Start"]=pd.to_datetime(flare_df["Start"])
print(flare_df["Start"])
with 