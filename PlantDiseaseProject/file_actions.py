import os as o
import sys as s

from numpy.f2py.auxfuncs import isintent_in


class FileActions:
    def __init__(self,mode,external_path,internal_path):
        self.mode = mode
        self.internal_path = internal_path
        self.external_path = external_path

    def fileAction(self):
        if self.mode == 'artifical_intelligence':
            try:
                internal_dirs = o.listdir(self.internal_path)
                external_dirs = o.listdir(self.external_path)
                return  (internal_dirs,external_dirs)
            except:
                print(self.internal_path,self.external_path)
        else:
            return ('Mode exception',self.mode)
