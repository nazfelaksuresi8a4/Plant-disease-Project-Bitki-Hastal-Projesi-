import numpy as np 
import matplotlib.pyplot as plt 

logfile_path = r"logs\SigmoidModelLogs\datas.txt"

class Plotter:
    def plotter(self,logfile_path):
        dct = {}
        dct_arr = []
        with open(logfile_path,mode='r') as logfile:
            logs = logfile.read().split('\n')

            for log in logs:
                log = log.split(':')

                if len(log) == 2:
                    array = [float(x.strip()) for x in log[1].replace('[','').replace(']','').split(',')]
                    dct[log[0]] = array
                    dct_arr.append(dct.copy())
            
                    dct.clear()
                
                else:
                    print('xf')

        for dc in dct_arr:
            print(dc)

        nrow,ncol = 0,0
        fig,ax = plt.subplots(nrows=3,ncols=3 - 1,figsize=(8,8))

        for dct in dct_arr:
            if nrow <= 1:
                if ncol == len(ax) - 1:
                    nrow += 1
                    ncol = 0

                key,data = list(dct.items()).copy()[0]
                print(nrow,ncol,key)

                yield (nrow,ncol,dct,key)
                ncol += 1
            
            else:
                nrow,ncol = 0,0
                key,data = list(dct.items()).copy()[0]
                yield (nrow,ncol,dct,key)
                
                ncol += 1

        else:
            nrow,ncol = 0,0

#Plotter().plotter(logfile_path)

