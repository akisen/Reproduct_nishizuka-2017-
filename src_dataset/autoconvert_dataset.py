import subprocess
import os
years=[i+2010 for i in range(4)]
months = [i+1 for i in range(12)]
for year in years:
    for month in months:
        if(year==2010 and month<=4):
            continue
        else:
            command = 'python3 merge_sharp_lorentz.py "/media/akito/Data/Dataset/SHARP(CEA)/'+str(year)+"/"+str(year)+str(month).zfill(2)+'/*Bp.fits" "/media/akito/Data/Dataset/Cgem.Lorentz/'+str(year)+"/"+str(year)+str(month).zfill(2)+'/*.Fx.fits" "../physical_feature/physical'+str(year)+str(month).zfill(2)+'.csv"'
            print(command)
            subprocess.call(command,shell=True)