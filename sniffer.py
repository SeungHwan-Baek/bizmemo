#-*- coding: utf-8 -*-
'''
Created on 2016. 10. 20.

@author: P005271
'''

import socket
import re

if __name__ == '__main__':
    host = socket.gethostbyname(socket.gethostname())
    print('당신의 IP :', host)
    
    p = re.compile('cmn=(\d{6})&ticket=(.{240})&id=(skt\.p\d{6}?@partner\.sk\.com)')
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
            
        s.bind((host, 0))
        s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 3)
        s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        
        setting_file = open('param.conf', 'w')
        
        print("패킷을 기다리고 있습니다. 쪽지함을 왔다갔다 하세요.")
        
        while True:
            data = s.recvfrom(10000)
            
            # data[1][0]은 source이므로, 곧 나가는 패킷만 가로채겠다는 의미
            if data[1][0] == host:
                try:
                    segment = data[0][40:].decode('utf-8')   
                    match_obj = p.search(segment)       
                    
                    if match_obj:
                        cmn, ticket, user_id = match_obj.group(1,2,3)
                        
                        #print ('cmn :', cmn)
                        #print ('ticket :', ticket)
                        #print ('id :', user_id)
                        
                        setting_file.write('cmn=' + cmn + '\n')
                        setting_file.write('ticket=' + ticket + '\n')
                        setting_file.write('id=' + user_id + '\n')
                        
                        print("설정값을 성공적으로 획득했습니다. 프로그램을 종료합니다.")
                        
                        break
                except:
                    pass            
    
        setting_file.close()
        
    except socket.error:
        print('socket error!!')
        print(socket.error)
