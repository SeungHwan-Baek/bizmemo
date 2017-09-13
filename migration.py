# -*- coding: utf-8 -*-
'''
Created on 2016. 10. 25.

@author: P005271
'''
import sqlite3
import re
import logging

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

def refine_table(table_name):
	conn = sqlite3.connect('skt.p005271@partner.sk.com.db')
	conn.text_factory = str

	memo_list = []
	
	select_sql = "select memo_seq, receivers, sender_name, sender_id, sender_division, send_date, content_size, recv_display, contents, subject, backup_date from " + table_name
		
	c1 = conn.cursor()
	c1.execute(select_sql)
	
	cur = c1.fetchall()
	
	row_count = len(cur)
	
	for idx, row in enumerate(cur):
		memo_list.append(row)
		
		if (idx+1) % 100 == 0:
			print("{}/{} 읽기 완료".format(idx+1, row_count))
			
	conn.close()
	
	# #############################################################
	# 여기서부터 새 파일에 쓰기
	# #############################################################
	conn = sqlite3.connect('new.db')
	conn.text_factory = str
	c2 = conn.cursor()
	
	if table_name == 'tb_recv_box':
		c2.execute('''CREATE TABLE tb_recv_box ( memo_seq        unique
											   , receivers       text
											   , sender_name     text
											   , sender_id       text
											   , sender_division text
											   , send_date       text
											   , content_size    integer
											   , recv_display    text
											   , contents        text
											   , subject         text
											   , backup_date     text )''')
	elif table_name == 'tb_sent_box':
		c2.execute('''CREATE TABLE tb_sent_box ( memo_seq        unique
											   , receivers       text
											   , sender_name     text
											   , sender_id       text
											   , sender_division text
											   , send_date       text
											   , content_size    integer
											   , recv_display    text
											   , contents        text
											   , subject         text
											   , backup_date     text )''')
											   
	conn.commit()
	
	for idx, memo in enumerate(memo_list):
		memo_seq		= memo[0]
		receivers		= memo[1]
		sender_name		= memo[2]
		sender_id		= memo[3]
		sender_division	= memo[4]
		send_date		= memo[5]
		content_size	= memo[6]
		recv_display	= memo[7]
		contents		= memo[8]
		subject			= memo[9]
		backup_date		= memo[10]
		
		insert_sql = "insert into " + table_name + '''( memo_seq
													  , receivers
													  , sender_name
													  , sender_id
													  , sender_division
													  , send_date
													  , content_size
													  , recv_display
													  , contents
													  , subject
													  , backup_date ) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

		c2.execute(insert_sql, ( memo_seq
							   , receivers
							   , sender_name
							   , sender_id
							   , sender_division
							   , send_date
							   , content_size
							   , recv_display
							   , refine_contents(contents)
							   , subject
							   , backup_date))
		
		conn.commit()
		
		if (idx+1) % 100 == 0:
			print("{}/{} 쓰기 완료".format(idx+1, row_count))
	
	conn.close()
	print("{} complete!!".format(table_name))


if __name__ == '__main__':
	refine_table('tb_sent_box')
	refine_table('tb_recv_box')
		