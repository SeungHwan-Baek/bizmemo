# -*- coding: utf-8 -*-
'''
Created on 2016. 10. 25.

@author: P005271
'''
from urllib import parse
import re

p1 = re.compile('<span.*?>', re.IGNORECASE)			# span open tag 제거
p2 = re.compile('</span>', re.IGNORECASE)			# span close tag 제거
p3 = re.compile('<font.*?>', re.IGNORECASE)			# font open tag 제거
p4 = re.compile('</font>', re.IGNORECASE)			# font close tag 제거
p5 = re.compile('\sstyle=".*?"', re.IGNORECASE)		# style 속성 제거
p6 = re.compile('\sclass=\w*', re.IGNORECASE)		# css class 속성 제거

p_list = [p1, p2, p3, p4, p5, p6]

def refine_contents(contents):
	for p in p_list:
		contents = re.sub(p, '', contents)

	return contents

class Memo():
    
    memo_seq = ''
    sender_name = ''
    subject = ''
    send_date = ''
    content_size = ''
    contents = ''
    recv_display = ''
    receivers = ''
    sender_id = ''
    sender_division = ''
    
    def __init__(self, memo_string=False):
        
        if memo_string:
            split_string_list = memo_string.split('&')
            
            key, value = '', ''
            
            for split_string_elem in split_string_list:
                try:
                    key, value = split_string_elem.split('=')
                    
                    if key == 'contents':
                        self.contents = parse.unquote(parse.unquote(value)).strip()
                        
                        tag_idx = self.contents.find('<TITLE>')
                        self.contents = refine_contents(self.contents[0:tag_idx] + '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">' + self.contents[tag_idx:])
                          
                    elif len(key) > 0:
                        parsed_string = parse.unquote(parse.unquote(value)).strip()
                        
                        if key == 'memo_seq':
                            self.memo_seq = parsed_string
                        elif key == 'sender_name':
                            self.sender_name = parsed_string
                        elif key == 'subject':
                            self.subject = parsed_string
                        elif key == 'send_date':  
                            self.send_date = parsed_string
                        elif key == 'sender_name':  
                            self.sender_name = parsed_string
                        elif key == 'content_size':  
                            self.content_size = parsed_string
                        elif key == 'recv_display':  
                            self.recv_display = parsed_string
                        elif key == 'receivers':
                            self.receivers = parsed_string
                        elif key == 'sender_id':
                            self.sender_id = parsed_string
                        elif key == 'sender_division':
                            self.sender_division = parsed_string
                except:
                    pass
                    
    def set_properties(self, memo_seq, sender_name, subject, send_date, content_size, contents='', recv_display=''):
        self.memo_seq = memo_seq
        self.sender_name = sender_name
        self.subject = subject
        self.send_date = send_date
        self.content_size = content_size
        self.contents = refine_contents(contents)
        self.recv_display = recv_display
