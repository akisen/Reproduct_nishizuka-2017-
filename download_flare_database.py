import subprocess
i=0
while(1):
    command ="python3 scrape_flare_database.py" + str(i)
    if(subprocess.call(command)):
        i+=1
        continue
    else:
        continue