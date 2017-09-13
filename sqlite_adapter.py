# -*- coding: utf-8 -*-
'''
Created on 2016. 10. 25.

@author: P005271
'''
import sqlite3
from memo import Memo
from condition import Condition

class SqliteAdapter:
    filename = ''
    conn = ''
    
    def __init__(self, filename):
        print('init in...', filename)
        self.filename = filename + '.db'
        
    def connect(self):
        self.conn = sqlite3.connect(self.filename)
        self.conn.text_factory = str 
        print('db file open success')
    
    def disconnect(self):
        self.conn.close()
        print('db file close success')


    # db파일에 테이블을 생성
    def create_table(self, box_flag='A'):
        self.c = self.conn.cursor()
        
        # 1. 받은 쪽지함 테이블 생성
        if box_flag in ('R', 'A'):
            try:
                # print('tb_recv_box table create')
                self.c.execute('''CREATE TABLE tb_recv_box ( memo_seq        unique
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
            # 테이블이 이미 존재할 경우 skip
            except sqlite3.OperationalError:
                print('tb_recv_box table already exists')
        
        # 2. 보낸 쪽지함 테이블 생성
        if box_flag in ('S', 'A'):
            try:
                # print('tb_sent_box table create')
                self.c.execute('''CREATE TABLE tb_sent_box ( memo_seq        unique
                                                           , receivers       text
                                                           , sender_name     text
                                                           , sender_id       text
                                                           , sender_division text
                                                           , send_date       text
                                                           , content_size    integer
                                                           , recv_display    text
                                                           , contents        text
                                                           , subject         text
                                                           , backup_date     date )''')
            # 테이블이 이미 존재할 경우 skip
            except sqlite3.OperationalError:
                print('tb_sent_box table already exists')
        
        self.conn.commit()
        
    # 쪽지를 DB에 insert
    def insert_memos(self, memos, box_flag):
        skip_count = 0
        
        if box_flag == 'R':
            table_name = 'tb_recv_box'
        elif box_flag == 'S':
            table_name = 'tb_sent_box'
        else:
            return False
        
        self.c = self.conn.cursor()
        
        for memo in memos:
            try:
                sql_string = "insert into " + table_name + '''( memo_seq
                                                              , receivers
                                                              , sender_name
                                                              , sender_id
                                                              , sender_division
                                                              , send_date
                                                              , content_size
                                                              , recv_display
                                                              , contents
                                                              , subject
                                                              , backup_date ) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now', 'localtime'))'''

                self.c.execute(sql_string, ( memo.memo_seq
                                           , memo.receivers
                                           , memo.sender_name
                                           , memo.sender_id
                                           , memo.sender_division
                                           , memo.send_date
                                           , memo.content_size
                                           , memo.recv_display
                                           , memo.contents
                                           , memo.subject))
                
                # print(memo['memo_seq'] + ' insert ok!!')
                
            # 이미 백업한 쪽지일 경우 skip
            except sqlite3.IntegrityError:
                # print('memo_seq[%d] already exists...skip!!' % memo['memo_seq'])
                skip_count = skip_count + 1
                pass
            
        self.conn.commit()
        return skip_count
    
	
    # 쪽지 리스트 조회(N건)
    def select_memo_list(self, cond):
        
        memo_list = []
        
        # 1. select
        if cond.box_flag == 'S':
            select_string = "select memo_seq, recv_display, subject, send_date, content_size"
        elif cond.box_flag == 'R':
            select_string = "select memo_seq, sender_name, subject, send_date, content_size"
        
        # 2. from
        if cond.box_flag == 'S':
            from_string = 'from tb_sent_box'
        elif cond.box_flag == 'R':
            from_string = 'from tb_recv_box'
        
        # 3. where (기본적으로 내용이 있는 데이터만 조회)
        where_string = 'where contents is not null '
        
        #  3-1. 보낸/받은 사람
        if len(str(cond.send_recv_user).strip()) > 0:
            if cond.send_recv_cl == 'S':
                where_string = where_string + "and sender_name like '%" + str(cond.send_recv_user) + "%' "
            elif cond.send_recv_cl == 'R':
                where_string = where_string + "and recv_display like '%" + str(cond.send_recv_user) + "%' "
        
        #  3-2. 키워드
        if len(str(cond.keyword).strip()):
            where_string = where_string + "and contents like '%" + str(cond.keyword) + "%' "
            
        #  3-3. 기간
        if cond.period_flag:
            start_dt = str(cond.period_start_dt) + '000000'
            end_dt = str(cond.period_end_dt) + '235959'
            
            where_string = where_string + "and send_date between '" + start_dt + "' and '" + end_dt + "'"
        
        # 4.order by
        order_string = 'order by send_date desc limit 100'
            
        # 5. final sql string
        sql_string = ' '.join((select_string, from_string, where_string, order_string))
        
        print('sql_string : ' + sql_string)
        
        try:
            self.c = self.conn.cursor()
            self.c.execute(sql_string)
            
            cur = self.c.fetchall()
            
            for row in cur:
                memo_seq = str(row[0])
                sender_name = str(row[1])
                subject = str(row[2])
                send_date = str(row[3])
                content_size = str(row[4])
                
                memo = Memo()
                memo.set_properties(memo_seq, sender_name, subject, send_date, content_size)
                memo_list.append(memo)
                
            return memo_list[:]
        except Exception as e:
            print(e)
            return []
    

    # 쪽지 내용 조회(1건)
    def get_memo(self, cond, memo_seq):
        if cond.box_flag == 'S':
            table_name = 'tb_sent_box'
        elif cond.box_flag == 'R':
            table_name = 'tb_recv_box'
        
        sql_string = "select sender_name, send_date, recv_display, contents from " + table_name + " where memo_seq ='" + memo_seq + "'"
        
        self.c = self.conn.cursor()
        self.c.execute(sql_string)
        
        cur = self.c.fetchone()
        
        sender_name = str(cur[0])
        send_date = str(cur[1])
        recv_display = str(cur[2])
        contents = str(cur[3])
        
        memo = Memo()
        memo.set_properties(memo_seq, sender_name, '', send_date, '', contents, recv_display)
        
        return memo
        
    # 쪽지 삭제 (실제로는 내용만 삭제)
    def delete_memo(self, cond, memo_seq):
        
        if cond.box_flag == 'S':
            table_name = 'tb_sent_box'
        elif cond.box_flag == 'R':
            table_name = 'tb_recv_box'
        
        sql_string = "update " + table_name + " set contents = null where memo_seq ='" + memo_seq + "'"
        
        self.c = self.conn.cursor()
        self.c.execute(sql_string)        
        self.conn.commit()
    
# 테스트 코드    
if __name__ == '__main__':
    adapter = SqliteAdapter('test.db')
    adapter.connect()
    