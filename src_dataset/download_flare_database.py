import subprocess
import time
i=0
while(1):
    command =["python3","scrape_flare_database.py",str(i)]
    print(command)
    if(i>=50):
        break
    if(subprocess.call(command)==0):
        i+=1
        continue
    else:
        time.sleep(60)
        continue