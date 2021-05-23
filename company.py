import sys
import threading
import pickle
from datetime import date
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication

from PyQt5 import QtGui
from PyQt5 import uic
import time
from find_pwC import *
from signupC import *
form_class = uic.loadUiType("company2.ui")[0]
# x=['음식명','음식갯수','총가격','음식명','음식갯수','총가격']
# y=['년','월','일','분','시','주문자','주소','가게명','배달대행','배달완료']

class CompanyApp(QMainWindow, form_class):
    import BM_business_rc
    # btns_names = [self.btn_......]
    # for i, name in enumerate(store_name):
    #     if search_word in name:
    #
    #
    #
    #
    # store_join="".join(store_name)
    # print(store_join)
    b=0
    q=0
    z=0
    store_name = ['뽀식이네 감자탕', '우람한 국밥', '애기선훈반점', '동국반점', '성환미쯔야', '선스시오', '상준이반마리치킨',
                  'bybyQ치킨', '영완피자', '돌리노피자', '이루오드리오분식', '광인분식', '상동버거', '맥두리아']



    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.initUI()
        self.store_list = []
        self.store_dict3 = {'이루오드리오분식': self.luo_btn, '광인분식': self.kwang_btn, '우람한 국밥': self.wooram_btn,
                           '애기선훈반점': self.by_sh_btn, '동국반점': self.dong_btn, '성환미쯔야': self.ksh_btn,
                           '선스시오': self.sun_btn,
                           '상준이반마리치킨': self.sj_btn, 'bybyq치킨': self.bybyq_btn1, '영완피자': self.yw_btn,
                           '돌리노피자': self.dol_btn, '상동버거': self.sang_btn,
                           '맥두리아': self.mac_btn,'뽀식이네 감자탕':self.bbosik_btn1}

        with open('delivery.pickle', 'rb') as r:
            self.x = pickle.load(r)

        self.u=[]
        self.k = 0

        self.btn_company_search.clicked.connect(self.search_store)
        self.btn_search_clear.clicked.connect(self.clear_btn)
        self.stackedWidget.setCurrentIndex(1)
        #서치해서 나온 가게들이 해당가게 페이지로 보내주는 시그널
        self.bbosik_btn2.clicked.connect(lambda:self.stack_index(3,self.bbosik_btn2))
        self.wooram_btn_2.clicked.connect(lambda:self.stack_index(3,self.wooram_btn_2))
        self.by_sh_btn_2.clicked.connect(lambda: self.stack_index(3,self.by_sh_btn_2))
        self.dong_btn_2.clicked.connect(lambda:self.stack_index(3,self.dong_btn_2))
        self.sun_btn2.clicked.connect(lambda:self.stack_index(3,self.sun_btn2))
        self.sj_btn_2.clicked.connect(lambda:self.stack_index(3,self.sj_btn_2))
        self.bybyq_btn_2.clicked.connect(lambda:self.stack_index(3,self.bybyq_btn_2))
        self.dol_btn_2.clicked.connect(lambda:self.stack_index(3,self.dol_btn_2))
        self.luo_btn_2.clicked.connect(lambda:self.stack_index(3,self.luo_btn_2))
        self.kwang_btn_2.clicked.connect(lambda:self.stack_index(3,self.kwang_btn_2))
        self.sang_btn_2.clicked.connect(lambda:self.stack_index(3,self.sang_btn_2))
        self.mac_btn_2.clicked.connect(lambda:self.stack_index(3,self.mac_btn_2))
        self.ksh_btn_2.clicked.connect(lambda:self.stack_index(3,self.ksh_btn_2))
        self.yw_btn_2.clicked.connect(lambda:self.stack_index(3,self.yw_btn_2))

        self.bbosik_btn_3.clicked.connect(lambda:self.stack_index(3,self.bbosik_btn_3))
        self.wooram_btn_3.clicked.connect(lambda:self.stack_index(3,self.wooram_btn_3))
        self.by_sh_btn_3.clicked.connect(lambda: self.stack_index(3,self.by_sh_btn_3))
        self.dong_btn_3.clicked.connect(lambda:self.stack_index(3,self.dong_btn_3))
        self.sun_btn_3.clicked.connect(lambda:self.stack_index(3,self.sun_btn_3))
        self.sj_btn_3.clicked.connect(lambda:self.stack_index(3,self.sj_btn_3))
        self.bybyq_btn_3.clicked.connect(lambda:self.stack_index(3,self.bybyq_btn_3))
        self.dol_btn_3.clicked.connect(lambda:self.stack_index(3,self.dol_btn_3))
        self.luo_btn_3.clicked.connect(lambda:self.stack_index(3,self.luo_btn_3))
        self.kwang_btn_3.clicked.connect(lambda:self.stack_index(3,self.kwang_btn_3))
        self.sang_btn_3.clicked.connect(lambda:self.stack_index(3,self.sang_btn_3))
        self.mac_btn_3.clicked.connect(lambda:self.stack_index(3,self.mac_btn_3))
        self.ksh_btn_3.clicked.connect(lambda:self.stack_index(3,self.ksh_btn_3))
        self.yw_btn_3.clicked.connect(lambda:self.stack_index(3,self.yw_btn_3))

        # #서치메인에있는 작은버튼들 해당가게 페이지로 보내주는 시그널
        # self.bbosik_btn_3.clicked.connect(lambda: self.stack_index(3,self.bbosik_btn_3))
        # self.wooram_btn_3.clicked.connect(lambda: self.stack_index(4,self.wooram_btn_3))
        # self.by_sh_btn_3.clicked.connect(lambda: self.stack_index(5))
        # self.dong_btn_3.clicked.connect(lambda: self.stack_index(6))
        # self.sun_btn_3.clicked.connect(lambda: self.stack_index(7))
        # self.sj_btn_3.clicked.connect(lambda: self.stack_index(8))
        # self.bybyq_btn_3.clicked.connect(lambda: self.stack_index(9))
        # self.dol_btn_3.clicked.connect(lambda: self.stack_index(10))
        # self.luo_btn_3.clicked.connect(lambda: self.stack_index(11))
        # self.kwang_btn_3.clicked.connect(lambda: self.stack_index(12))
        # self.sang_btn_3.clicked.connect(lambda: self.stack_index(13))
        # self.mac_btn_3.clicked.connect(lambda: self.stack_index(14))
        # self.ksh_btn_3.clicked.connect(lambda: self.stack_index(15))
        # self.yw_btn_3.clicked.connect(lambda: self.stack_index(16))


        #뒤로가기 버튼을 눌렀을경우 서치목록으로 보내는 함수
        self.bbosik_back.clicked.connect(lambda: self.stack_index2(2))
        self.calendarWidget.setSelectedDate(QDate.currentDate())
        self.calendarWidget.selectionChanged.connect(self.set_text)
        self.calendarWidget.selectionChanged.connect(self.set_month)



        # self.choicelogin_button_cp.clicked.connect()


        # x=concurrentdate.toString
        # print(x)
        # x = self.calendarWidget.selectedDate().toString('Md')
        # print(x)

    #
    #
    # def cal(self):
    #
    #

    # def
    #
    #
    #
    # def label(self):
    #     self.label1.setText(date.toString("dd"))

    # x = [['5', '09', '주문시간', '주문음식', '수량', '단가', '주문자', '베송주소', '배달대행', '배달완료', '뽀식이네 감자탕'],
    #      ['월', '일', '주문시간', '주문음식', '수량', '단가', '주문자', '베송주소', '배달대행', '배달완료', '현식 감자탕']]

    def set_text(self):
        print(self.x)
        y = 0
        self.tableWidget.setRowCount(y)
        self.k = 0
        for i in range(len(self.x)):
            if self.label.text()==self.x[i][-1]:
                if  self.calendarWidget.selectedDate().toString('d')==self.x[i][1] and str(self.calendarWidget.monthShown())==self.x[i][0]:
                    y += 1
                    self.k += int(self.x[i][5])
                    self.label_2.setText(f'금일총매출 :{self.k}')
                    self.q+=self.k
                    self.tableWidget.setRowCount(y)
                    for j in range(7):
                        self.tableWidget.setItem(y - 1, j, QTableWidgetItem(self.x[i][j + 2]))
                        self.u.append(self.x[i][0])
        if self.k==0:
            self.label_2.clear()




    def set_month(self):
        z = 0
        c=''
        for i in range(len(self.x)):
            if self.label.text() == self.x[i][-1]:
                if str(self.calendarWidget.monthShown()) == self.x[i][0] and self.calendarWidget.selectedDate().toString('d')==self.x[i][1]:
                    z += int(self.x[i][5])
                    self.label_3.setText(f"{self.calendarWidget.monthShown()}월 매출:{z}")
                    self.u.append(self.x[i][0])
















    # def table_seTtext(self):
    #
    #
    #




    #해당 가게를 찾아서 버튼을 띄어주는 함수
    def search_store(self):
        for i in self.store_name:
            if self.company_searchbar.text() in i:
                self.store_list.append(i)
                print(self.store_list)
        for j in self.store_list:
            if len(self.company_searchbar.text())==0:
                self.store_list.clear()
                self.search_msg()
            elif j in self.store_dict3.keys():
                self.verticalLayout_search.addWidget(self.store_dict3[j])


    #서치목록초기화 시켜주는 함수
    def clear_btn(self):
        for i in self.store_list:
            if i in self.store_list:
                self.verticalLayout_hide.addWidget(self.store_dict3[i])

        self.store_list.clear()
        self.company_searchbar.clear()


    #해당인덱스로 보내는 함수
    def stack_index(self,a,b):

        self.stackedWidget.setCurrentIndex(a-1)
        self.label.setText(b.text())
        self.set_month()
        print(self.label.text())
        self.set_text()

    def stack_index2(self,a):
        self.stackedWidget.setCurrentIndex(a - 1)
        self.tableWidget.clear()


    #검색어를 입력하지 않을시 검색이안됨
    def search_msg(self):
        self.msg = QMessageBox()
        self.msg.setWindowTitle("check")
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.setText("""
검색어를 입력해주세요!""")
        self.msg.show()
    #검색버튼에서 엔터키누를시 작동
    def keyPressEvent(self, e):
        if e.key() == 16777220:
            if len(self.company_searchbar.text()) >= 1:
                self.search_store()



    # def sign_up(self):
    #
    #
    #
    #
    #










        # 좌측 상단 날짜를 오늘 날짜로 표시
        # self.label_title_date.setText(date.today().isoformat())
        #
        # 프로그램 구동되면 첫 화면: 로그인화면 설정
        # self.stackedWidget.setCurrentIndex(0)

        ## 사이드버튼 스택위젯 연결
        # self.go_sw(0)
        # self.go_sw(1)
        # self.go_sw(2)
        # self.go_sw(3)
        # self.go_sw(4)

        ## 로그인 관련
        self.Login_info = Login_info()
        self.pw_search = Pw_search()
        # self.login_status = False
        self.choicelogin_button_cp.clicked.connect(self.Login_info.show)  # 회원가입
        self.main_pw_search_btn_cp.clicked.connect(self.pw_search.show)  # 비밀번호 찾기
        self.login_button.clicked.connect(self.companyapp)  # 로그인화면

        ### 좌측하단 로그인/로그아웃/회원가입 버튼 연결
        self.btn_login.clicked.connect(self.login_)
        self.btn_logout.clicked.connect(self.logout_)
        self.btn_signup.clicked.connect(self.signup_)

    # 모니터 중앙에 어플배치
    def initUI(self):
        self.setWindowTitle('B달의 민족_본사용')
        self.resize(1103, 674)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # # 사이드 버튼 클릭시 해당 위젯으로 이동 함수
    # def go_sw(self, index):
    #     self.sidebtns = [self.btn_new_order, self.btn_order_status, self.btn_delivery_status,
    #                      self.btn_daily_sales, self.btn_monthly_sales]
    #     self.sidebtns[index].clicked.connect(lambda: self.show_sw(index+1))
    #
    # def show_sw(self, index):
    #     return self.stackedWidget.setCurrentIndex(index)

    # # 로그인 눌렀을시 함수
    # def companyapp(self):
    #     if self.id_main_2.text() in self.Login_info.login_c.keys():
    #         if self.pw_main_2.text() == self.Login_info.login_c[self.id_main_2.text()][0]:
    #             # 로그인 성공시
    #             self.current_id = self.id_main_2.text()
    #
    #             self.stackedWidget.setCurrentIndex(1)  ## 홈화면가기
    #             # self.login_status = True
    #         else:
    #             self.statusbar_2.setText("비번이 맞지않습니다.")
    #     else:
    #         self.statusbar_2.setText("입력하신 ID로 가입된 정보가 없습니다.")
    #
    # # 좌측하단 로그인 클릭시; 로그아웃상태에서만 로그인 버튼 활성화
    # def login_(self):
    #     if not self.login_status:
    #         self.stackedWidget.setCurrentIndex(0)
    #     else:
    #         pass
    #
    # def logout_(self):
    #     if self.login_status:
    #         self.stackedWidget.setCurrentIndex(0)
    #         self.id_main_2.clear()
    #         self.pw_main_2.clear()
    #         self.statusbar_2.setText("로그아웃 되었습니다.")
    #         # self.login_status = False
    #     else:
    #         pass
    #
    # def signup_(self):
    #     if not self.login_status:
    #         self.Login_info.show()
    #     else:
    #         pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = CompanyApp()
    form.show()
    exit(app.exec_())