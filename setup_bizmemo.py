'''
Created on 2016. 10. 27.

@author: P005271
'''
from distutils.core import setup
import py2exe
import sys
import os

sys.argv.append('py2exe')
sys.argv.append('-q')

class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        self.version = "0.1"
        self.company_name = "SK C&C"
        self.copyright = "Dr.Strange"
        self.name = "BizMemo Viewer"

target = Target(description = "BizMemo Viewer", script = "bizmemo.py", dest_base = "viewer")

setup(
    options = {'py2exe': {'bundle_files': 1,
                          'compressed'  : True,
                          'includes':['sip'],
                          'excludes':['_ssl'],
                          'dll_excludes':['msvcr71.dll', 'w9xpopen.exe'],
                          'optimize':2
                          }},
    windows = [target],
    zipfile = None,
)
