import numpy as np
import matplotlib.pyplot as plt

class LoggPlotterEvaulate:
    def __init__(self,lfpath):
        self.lfpath = lfpath
        self.loss_arr = []
        self.acc_arr = []

    def plotLog(self):
        val_loss,val_acc = None,None

        with open(self.lfpath,'r') as logfile:
            splitted = logfile.read().split('\n')
            for logX in splitted:
                splittedX = logX.split(';')

                if len(splittedX) == 4:
                    self.loss_arr.append(splittedX[1].split(';')[0].split(','))
                    self.acc_arr.append(splittedX[3].split(';')[0].split(','))

            copy_loss = self.loss_arr.copy()
            copy_acc = self.acc_arr.copy()

            self.loss_arr.clear()
            self.acc_arr.clear()

            for vecX,vecY in zip(copy_loss,copy_acc):
                for argX,argY in zip(vecX,vecY):
                    self.loss_arr.append(argX)
                    self.acc_arr.append(argY)

            self.loss_arr = [float(x) for x in self.loss_arr]
            self.acc_arr = [float(x) for x in self.acc_arr]

            return (self.loss_arr,self.acc_arr,['Loss','Accuracy'])


#LoggPlotterEvaulate(r"C:\Users\alper\Desktop\Plant Disease Project\logs\SigmoidModelLogs\evaulates.txt").plotLog()


