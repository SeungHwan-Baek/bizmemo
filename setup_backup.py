'''
Created on 2016. 10. 28.

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
        self.name = "BizMemo Backup"

target = Target(description = "BizMemo Backup", script = "backup.py", dest_base = "backup")

setup(
    options = {'py2exe': {'bundle_files': 1,
                          'compressed'  : True,
                          'includes':['urllib'],
                          'excludes':['_ssl']
                          #'excludes':['_ssl','pyreadline','difflib','doctest','optparse','pickle','calendar'],
                          #'dll_excludes':['msvcr71.dll']
                          }},
    console = [target],
    zipfile = None,
)
