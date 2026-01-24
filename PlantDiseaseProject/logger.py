import datetime as dt 

class Logger:
    def __init__(self,logfile_path,evaulate_path,history,model,test_data):
        self.logfile_path = logfile_path
        self.evaulate_path = evaulate_path 
        self.history = history
        self.model = model
        self.test_data = test_data
        self.date,self.hour = dt.datetime.now().date(),dt.datetime.now().strftime('%H:%M:%S')
    
    def writeLog(self):
        if isinstance(self.logfile_path,str) and isinstance(self.evaulate_path,str):
            with open(self.logfile_path,'a') as logfile:
                logfile.write(f'Tarih/Saat: {self.date}/{self.hour}\n')

                for key,item in self.history.history.items():
                    logfile.write(f'{key}: {item}\n')
            
            with open(self.evaulate_path,'a') as elogfile:
                test_loss,test_acc = self.model.evaluate(self.test_data)
                
                elogfile.write(f'Tarih/Saat: {self.date}/{self.hour}')
                elogfile.write(f'\ntest loss; {test_loss}, test accuracy: {test_acc}\n')
        
        else:
            print('log dosyaları belirtilmemiş')
