import time
import glob
import pandas as pd
path_str = "flare_database/flare_database*.csv"
path_obj = sorted(glob.glob(path_str))
df = pd.DataFrame([])
for path in path_obj:
    df = df.append(pd.read_csv(path))
df = df.drop_duplicates()
df.to_csv("Flare_database.csv")
