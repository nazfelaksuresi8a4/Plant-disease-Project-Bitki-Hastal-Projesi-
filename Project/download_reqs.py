import subprocess as sbp
import os as _o

class installPythonPackages:
    def __init__(self):
        self.state = bool(0)
        self.proces_out = None 
    
    def installPKGS(self):
        try:
            self.proces_out = sbp.Popen(['pip'])
            self.state = 1

        except Exception as e0fx:
            self.state = 0
            print(1,e0fx)
        
        finally:
            try:
                if self.state == 1:
                    self.proces_out = sbp.Popen(['pip','install','-r','reqs.txt'],
                                                               stdout=sbp.PIPE,
                                                               stderr=sbp.STDOUT,
                                                               text=True)
                    
                    if self.proces_out is not None:
                        if isinstance(self.proces_out,list):
                            self.state = 1
                        
                        else:
                            print('proces in not list')
                    
                    else:
                        print('process is none')
                    
                
                else:
                    self.proces_out = sbp.Popen(['python.exe','-m','pip','install','-r','reqs.txt'],
                                                               stdout=sbp.PIPE,
                                                               stderr=sbp.STDOUT,
                                                               text=True)
                    
                    if self.proces_out is not None:
                        if isinstance(self.proces_out,list):
                            self.state = 1
                        
                        else:
                            print('proces in not list')
                    
                    else:
                        print('process is none')
            
            except Exception as e0fx1:
                print('Modüller kurulamıyor lütfen daha sonra tekrar deneyiniz hata: ' + str(e0fx1))
                self.state = 0
                self.proces_out = None
            
