import subprocess as sbp
import time as tx

class main:
    def getPython(self,bcount,px1,px2):
        cprocess = 0xf2

        try:
            if bcount == 64:
                print('running')
                cprocess = sbp.run(px2)
            
            else:
                if bcount == 32:
                    print('running')
                    cprocess = sbp.run(px1)

        except Exception as e0fx:
            print(e0fx)
        
        finally:
            flag = True

            while flag:
                if cprocess is not None:
                    flag = False
                    return ('completed',24)
                
                else:
                    pass

    def startSetup(self,state):
        if state == 1:
            pass

        else:
            print(f'state is : {state} setup failed. Please try again later....')


class mixinClass(main):
    def __init__(self,bcountz,px1z,px2z):
        super().__init__()
        try:
            out = self.getPython(bcountz,px1z,px2z)

        except Exception as e0fx:
            print(e0fx)
        
        finally:
            try:
                print(out)
            
            except UnboundLocalError:
                print('out variable is not defined')
    
    