# -*- coding: utf-8 -*-
'''
Created on 2016. 10. 25.

@author: P005271
'''
class Configure:
    properties = {}
    
    def __init__(self):
        with open('setting.conf', 'r') as f:
            conf_list = f.readlines()
            
            for conf_string in conf_list:
                conf_key, conf_value = conf_string.split('=')
                self.properties[conf_key] = conf_value.strip()
                
        with open('param.conf', 'r') as f:
            conf_list = f.readlines()
            
            for conf_string in conf_list:
                conf_key, conf_value = conf_string.split('=')
                self.properties[conf_key] = conf_value.strip()
                
        # default setting
        if not self.properties['daily_max_cnt']:
            self.properties['daily_max_cnt'] = 200
            
        if not self.properties['expire_period']:
            self.properties['expire_period'] = 21
            
        if not self.properties['backup_period']:
            self.properties['backup_period'] = 7
            
        if not self.properties['system_noti_skip']:
            self.properties['system_noti_skip'] = 'Y'
        
        #print(self.properties)
         
    def __getitem__(self, conf_key):
        return self.properties[conf_key]
    
if __name__ == '__main__':
    conf = Configure()
    #print(conf.properties)
