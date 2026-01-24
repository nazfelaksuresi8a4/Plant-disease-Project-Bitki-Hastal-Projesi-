import numpy as np 
import matplotlib.pyplot as plt 

logfile_path = r"logs\datas.txt"

dct = {}
with open(logfile_path,mode='r') as logfile:
    logs = logfile.read().split('\n')

    for log in logs:
        log = log.split(':')
        if len(log) == 2:
            array = [float(x.strip()) for x in log[1].replace('[','').replace(']','').split(',')]
            print(array)
            dct[log[0]] = array

nrow,ncol = 0,0

fig,ax = plt.subplots(nrows=3,ncols=3 - 1,figsize=(8,8))
ax[len(ax) - 1,len(ax) - 2].axis(False)

for axX,key in enumerate(dct):
    if ncol == len(ax) - 1:
        nrow += 1
        ncol = 0

    ax[nrow,ncol].plot(np.array(dct[key]),label=str(key))
    ax[nrow,ncol].legend()
    ncol += 1 

plt.show()