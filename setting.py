# -*- coding: utf-8 -*-
'''
Created on 2016. 12. 31.

@author: P005271
'''
from configparser import ConfigParser

class bizmemo_config:
	cfg = ''
	
	def __init__(self, filename):
		self.cfg = ConfigParser()
		self.cfg.read(filename)

		self.cmn = self.cfg.get('network', 'cmn')
		self.ticket = self.cfg.get('network', 'ticket')	
		self.id = self.cfg.get('network', 'id')

		self.daily_max_cnt = self.cfg.get('parameters', 'daily_max_cnt')
		self.expire_period = self.cfg.get('parameters', 'expire_period')
		self.backup_period = self.cfg.get('parameters', 'backup_period')
		self.system_noti_skip = self.cfg.get('parameters', 'system_noti_skip')

	def __repr__(self):
		rval = ''

		for sec in self.cfg.sections():
			rval = rval + '=' * 30 + '\n'
			rval = rval + sec + '\n'
			rval = rval + '=' * 30 + '\n'

			for name, value in self.cfg.items(sec):
				rval = rval + name + ' : ' + value + '\n'
			
		return rval

if __name__ == '__main__':
	bcfg = bizmemo_config('setting.ini')
	print(bcfg)
	