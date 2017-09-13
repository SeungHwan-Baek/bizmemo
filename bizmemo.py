# -*- coding: utf-8 -*-
'''
Created on 2016. 10. 25.

@author: P005271
'''

import sys
import math

from datetime import datetime
from memo import Memo
from condition import Condition
from sqlite_adapter import SqliteAdapter
from setting import bizmemo_config

from PyQt4 import QtGui, uic
from PyQt4.QtCore import * 
from PyQt4.Qt import QFileDialog, QMessageBox

class BizMemoDialog(QtGui.QDialog):
    conf = ''
    adapter = ''
    
    def __init__(self):
        self.conf = bizmemo_config('setting.ini')
        self.adapter = SqliteAdapter(self.conf.id)
        self.adapter.connect()
        
        QtGui.QDialog.__init__(self)        
        self.ui = uic.loadUi('main.ui', self)
        
        # 최소/최대화 버튼 활성화
        #self.setWindowFlags(self.windowFlags() | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint)
        self.setWindowFlags(self.windowFlags() | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint)
        
        # 콤보값
        self.cmbSndRcvCl.addItem('보낸 사람', 'S')
        self.cmbSndRcvCl.addItem('받은 사람', 'R')
        
        # 기간은 기본으로 비활성화
        self.chkPeriod.setChecked(False)
        
        # 메인 그리드
        self.tableWidget.setColumnWidth(0, 80)     # memo_seq
        self.tableWidget.setColumnWidth(1, 100)    # 보낸/받은 사람
        self.tableWidget.setColumnWidth(2, 600)    # 제목
        self.tableWidget.setColumnWidth(3, 150)    # 보낸/받은 일시
        self.tableWidget.setColumnWidth(4, 50)     # 크기
        
        # 아무 조건없이 조회
        self.search()
        
        # signal/slot 연결   
        self.radio_recv_box.clicked.connect(self.box_radio_clicked) # 쪽지함 변경시          
        self.radio_sent_box.clicked.connect(self.box_radio_clicked) # 쪽지함 변경시
        self.search_button.clicked.connect(self.search)  # 검색 버튼 클릭시        
        self.tableWidget.itemClicked.connect(self.table_item_clicked)   # 그리드 항목 클릭시
    
    # 쪽지함 변경
    def box_radio_clicked(self):
        try:
            self.clear_condition()
            self.search()
        except Exception as e:
            print(e)
    
    # 그리드 항목 클릭
    def table_item_clicked(self):
        try:
            selected_item = self.tableWidget.selectedItems()
            
            if selected_item:
                memo_seq = str(selected_item[0].text())
                #print('선택된 memo_seq :' + memo_seq)
                self.read(memo_seq)
        except Exception as e:
            print(e)
    
    # 쪽지 검색
    def search(self):    
        try:
            # 조건으로 쪽지 리스트 조회
            cond = self.get_condtition()
            memo_list = self.adapter.select_memo_list(cond)
            
            table_widget = self.tableWidget
            table_widget.setRowCount(len(memo_list))
            
            for i, memo in enumerate(memo_list):     
                memo_seq = memo.memo_seq
                
                if cond.box_flag == 'R':
                    sender_name = memo.sender_name
                elif cond.box_flag == 'S':
                    sender_name = self.recv_display_convert(memo.sender_name)[0]
                    
                subject = memo.subject
                send_date = memo.send_date
                content_size = memo.content_size
                
                # text formatting
                send_date = datetime.strptime(send_date, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
                content_size = str(math.trunc(int(content_size) / 1000)) + ' KB' 
                
                # item
                item0 = QtGui.QTableWidgetItem(memo_seq)
                item1 = QtGui.QTableWidgetItem(sender_name)
                item2 = QtGui.QTableWidgetItem(subject)
                item3 = QtGui.QTableWidgetItem(send_date)
                item4 = QtGui.QTableWidgetItem(content_size)
                
                # cell align
                item0.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
                item3.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
                item4.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                
                # set to grid
                table_widget.setItem(i, 0, item0)
                table_widget.setItem(i, 1, item1)
                table_widget.setItem(i, 2, item2)
                table_widget.setItem(i, 3, item3)
                table_widget.setItem(i, 4, item4)
           
            self.ui.show()
            
        except Exception as e:
            print(e)
            
    # 쪽지 1건 읽기
    def read(self, memo_seq):
        memo = self.adapter.get_memo(self.get_condtition(), memo_seq)
        
        sender_name = memo.sender_name
        recv_display = memo.recv_display
        contents = memo.contents
        
        rcv_name, ref_name = self.recv_display_convert(recv_display)
        
        self.edt_sender_name.setText(sender_name)
        self.edt_recv_display.setText(rcv_name)
        self.edt_recv_display2.setText(ref_name)
        self.webView.setHtml(contents)
    
    # 조회조건을 클리어한다
    def clear_condition(self):
        if self.radio_recv_box.isChecked():
            self.cmbSndRcvCl.setCurrentIndex(self.cmbSndRcvCl.findText('보낸 사람'))
        else:
            self.cmbSndRcvCl.setCurrentIndex(self.cmbSndRcvCl.findText('받은 사람'))
            
        self.editUserNm.clear()
        self.editKeyword.clear()
        
    # 화면에서 조회조건 읽어서 condition객체 생성&리턴
    def get_condtition(self):
        box_flag        = 'R' if self.radio_recv_box.isChecked() else 'S' 
        send_recv_cl    = self.cmbSndRcvCl.itemData(self.cmbSndRcvCl.currentIndex())
        send_recv_user  = str(self.editUserNm.text())
        keyword         = str(self.editKeyword.text())
        period_flag     = self.chkPeriod.isChecked()
        period_start_dt = str(self.dtPeriodStart.date().toString('yyyyMMdd'))
        period_end_dt   = str(self.dtPeriodStart.date().toString('yyyyMMdd'))
        
        return Condition(box_flag, send_recv_cl, send_recv_user, keyword, period_flag, period_start_dt, period_end_dt)

    # input  : R;배정호/대리/고객상품팀 <baezzang@sk.com>; 이송호/오더 <skt.p069495@partner.sk.com>;
    # output : 배정호/대리/고객상품팀; 이송호/오더
    def recv_display_convert(self, recv_display_text):
        split_text_list = recv_display_text.split('\n') 
        
        rcv_user_text = ', '.join([user[0:user.index('<')].strip() for user in split_text_list[0].split(';')[1:-1]])
        ref_user_text = ''
        
        # 참조가 있으면 추가로 parsing
        if len(split_text_list) == 2:
            ref_user_text = ', '.join([user[0:user.index('<')].strip() for user in split_text_list[1].split(';')[1:-1]])
                    
        return rcv_user_text, ref_user_text
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = BizMemoDialog()
    
    # print(QtGui.QStyleFactory.keys()) 
    # ['Windows', 'WindowsXP', 'WindowsVista', 'Fusion']
    
    sys.exit(app.exec_())
    