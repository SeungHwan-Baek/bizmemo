# -*- coding: utf-8 -*-
'''
Created on 2016. 5. 3.

@author: P005271
'''
from urllib import parse, request
import re
import datetime as dt

from memo import Memo
from sqlite_adapter import SqliteAdapter
from configure import Configure
from setting import bizmemo_config

system_noti_users = ('ITRM관리자', '모델변경현황')

box_id = ''
search_url = 'http://imwas.sk.com/Memo/SearchBoxMemo'
read_url = 'http://imwas.sk.com/Memo/Read'

def backup_bizmemo(box_flag):
	if box_flag == 'S':
		box_id = '-10'
	elif box_flag == 'R':
		box_id = '0'
	else:
		return False
    
	conf = bizmemo_config('setting.ini')
        
	daily_max_cnt = int(conf.daily_max_cnt)  # 일일 최대 백업량(200)
	expire_period = int(conf.expire_period)  # 쪽지 삭제 기한(3주)
	backup_period = int(conf.backup_period)  # 한번에 백업할 기간 (7일)
    
	db_file_name     = conf.id                  # sqlite 파일명
	system_noti_skip = conf.system_noti_skip    # 시스템쪽지 스킵여부
    
	cmn, ticket, skt_emp_id = conf.cmn, conf.ticket, conf.id
	
	print(conf)
	print(backup_period)

	adapter = SqliteAdapter(db_file_name)
	adapter.connect()
	adapter.create_table(box_flag)

	headers = {
		'User-Agent' : 'TMsgBox/3.5.0.0',
		'Cache-Control' : 'no-cache',
		'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
		'Accept-Charset' : 'UTF-8'
	}
    
	param_list = {}
	param_list['max_num'] = daily_max_cnt
	param_list['box_id']  = box_id
	param_list['cmn']     = cmn
	param_list['ticket']  = ticket
	param_list['id']      = skt_emp_id
    
	# 백업시작일은 삭제되기 하루전인 데이터
	start_date = dt.date.today() - dt.timedelta(days=expire_period)
    
	# backup_period 값에 설정된 기간만큼 백업(기본값 = 7)
	for d in range(backup_period):
		target_date = start_date + dt.timedelta(days=d) # d일만큼 더하기 (0 ~ 4)
		
		param_list['start_date']  = '%d-%02d-%02d' % (target_date.year, target_date.month, target_date.day)
		param_list['end_date']    = param_list['start_date']
		
		# 1차 : 쪽지 목록 조회
		req = request.Request(search_url, parse.urlencode(param_list).encode('ascii'), headers=headers)
		u = request.urlopen(req)
		
		memos = []
		memo_seq_list = re.findall('memo_seq=(\d{9,10})&', u.read().decode('utf-8')) # 데이터 전체에서 memo_seq 값만 뽑아온다
		
		# 2차 : 쪽지 내용 조회
		for memo_seq in memo_seq_list:
			each_param_list = {}
			
			each_param_list['memo_info'] = '%s|%s|%s' % (box_id, memo_seq, box_flag)
			each_param_list['ticket'] = ticket
			each_param_list['cmn'] = cmn
			each_param_list['id'] = skt_emp_id

			req = request.Request(read_url, parse.urlencode(each_param_list).encode('ascii'), headers=headers)
			u = request.urlopen(req)
			
			memo = Memo(u.readlines()[1].decode('utf-8'))   # 역시 1번째 라인은 응답코드이므로 무시
			
			# 정상적으로 parsing된 쪽지가 아니면 SKIP
			if memo.memo_seq == '':
				continue
			# 시스템계정 발신쪽지일 경우 백업 제외
			elif system_noti_skip == 'Y' and memo.sender_name in system_noti_users:
				continue

			memos.append(memo)
			
		skip_count = adapter.insert_memos(memos, box_flag)
		print('# [%4d/%02d/%02d] Memo Count : %4d (%4d skipped)' % (target_date.year, target_date.month, target_date.day, len(memo_seq_list), skip_count))
		
	adapter.disconnect()
        
if __name__ == '__main__':
    print('보낸 쪽지함 백업 시작')
    backup_bizmemo('S')
    
    print('받은 쪽지함 백업 시작')
    backup_bizmemo('R')
    