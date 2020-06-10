import subprocess
import time
i=3
while(1):
    command =["python3","scrape_flare_database.py",str(i)]
    print(command)
    if(subprocess.call(command)==0):
        i+=1
        continue
    else:
        wait(3600)
        continue