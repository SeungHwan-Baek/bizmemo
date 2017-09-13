# -*- coding: utf-8 -*-
'''
Created on 2016. 10. 26.

@author: P005271
'''

class Condition:
    box_flag = ''
    send_recv_cl = ''
    send_recv_user = ''
    keyword = ''
    period_flag = False
    period_start_dt = ''
    period_end_dt = ''
    
    def __init__(self, box_flag='R', send_recv_cl='', send_recv_user='', keyword='', period_flag=False, period_start_dt='', period_end_dt=''):
        self.box_flag = box_flag
        self.send_recv_cl = send_recv_cl
        self.send_recv_user = send_recv_user
        self.keyword = keyword
        self.period_flag = period_flag
        self.period_start_dt = period_start_dt
        self.period_end_dt = period_end_dt
        
    def show(self):
        print('box_flag :', self.box_flag)
        print('send_recv_cl :', self.send_recv_cl)
        print('send_recv_user :', self.send_recv_user)
        print('keyword :', self.keyword)
        print('period_flag :', self.period_flag)
        print('period_start_dt :', self.period_start_dt)
        print('period_end_dt :', self.period_end_dt)