import sys
import threading
import pickle
from datetime import date
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication

from PyQt5 import QtGui
from PyQt5 import uic
import time
from find_pw import *
from signup import *

form_class = uic.loadUiType("cust_2.8.ui")[0]

class CustApp(QMainWindow, form_class):
    import BaeMin_rc

    #가게 이름
    store_name=['뽀식이네 감자탕','우람한 국밥','애기선훈반점','동국반점','성환미쯔야','선스시오','상준이반마리치킨',
                'bybyQ','영완피자','돌리노피자','이루오드리오분식','광인분식','상동버거','맥두리아']

    #가게 정보와 가격
    all_dict = {
        "한식": {"우람한 국밥": {"정보": ["4.7", "02-720-2748", "2000", "10000"], "순대국밥": 6000, "소머리국밥": 7000, "굴국밥": 11000,
                "설렁탕": 8000},
            "뽀식이네 감자탕": {"정보": ["4.3", "02-736-0828", "3000", "15000"], "감자탕": 13000, "우거지해장국": 6500, "소머리국밥": 8000,
                "설렁탕": 8500}},
        "일식": {"성환미쯔야": {"정보": ["4.8", "02-275-1475", "3000", "15000"], "돈코츠라멘": 7500, "미소라멘": 7500, "돈까스": 6000,
                         "초밥12p": 7500},
               "선스시오": {"정보": ["4.0", "02-920-8576", "1500", "25000"], "초밥12p": 7000, "돈까스": 6500, "초밥20p": 9000,
                        "광어회": 18000}},
        "중식": {"애기선훈반점": {"정보": ["4.7", "02-355-1197", "2000", "12000"], "짜장면": 2500, "짬뽕": 6000, "볶음밥": 6000,
                          "탕수육": 12000},
               "동국반점": {"정보": ["3.8", "02-804-4902", "3000", "18000"], "짜장면": 4000, "짬뽕": 5500, "팔보채": 18000,
                        "양장피": 21000}},
        "분식": {
            "이루오드리오분식": {"정보": ["5.0", "02-976-3753", "1000", "8000"], "김밥": 1500, "떡볶이": 3000, "순대": 2000,
                         "모듬튀김": 2000},
            "광인분식": {"정보": ["4.3", "02-376-4975", "2000", "12000"], "김밥": 2000, "라면": 2500, "떡볶이": 1500, "제육덮밥": 6500}},
        "치킨": {"상준이 반마리치킨": {"정보": ["4.3", "02-736-0828", "2000", "16000"], "후라이드": 12000, "양념치킨": 13000, "간장치킨": 13000,
                             "치즈볼": 4000},
               "bybyq치킨": {"정보": ["4.0", "02-250-2694", "4000", "15000"], "후라이드": 8000, "양념치킨": 12000, "스노윙치킨": 16000,
                           "치즈스틱": 4000}},
        "피자": {"영완피자": {"정보": ["4.5", "02-837-3319", "1500", "22000"], "불고기피자": 8000, "콤비네이션피자": 8500, "쉬림프피자": 9000,
                        "하와이안피자": 10000},
               "돌리노피자": {"정보": ["4.9", "02-250-2694", "2000", "18000"], "불고기피자": 9000, "콤비네이션피자": 11000, "쉬림프피자": 9500,
                         "하와이안피자": 11000}},
        "패스트푸드": {"상동버거": {"정보": ["3.7", "02-720-2748", "3000", "15000"], "불고기버거": 2500, "상하이버거": 3200, "치즈버거": 3200,
                           "치킨버거": 1200},
                  "맥두리아": {"정보": ["4.6", "02-537-8828", "3000", "15000"], "불고기버거": 2200, "치즈버거": 2400, "슈맥버거": 2500,
                           "새우버거": 1700}}}

    pay_atonce_save=[]          #바로 결제 저장 리스트
    all_price = 0  # 가격 합산용
    basket = list()  # 한가게에서 구매한 품목
    basket_2 = {}       # 추후 추가된 장바구니???
    all_basket = []  # 주문한 전체 품목
    search_name_list = []  # 검색했을때 나오는 가게명을 넣어주는 리스트
    search_name_list2 = []  # 검색했을때 바로결제에 나오는 리스트
    history_btn = []  # 주문내역 버튼 비교용

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

        self.stackedWidget.setCurrentIndex(10)
        self.stackedWidget_5.setCurrentIndex(0)
        self.stackedWidget_profile.setCurrentIndex(0)

        self.nickname_show.setText('더귀한분, ')

        # 검색목록에 버튼을 보내기위한 딕트
        self.store_dict = {'이루오드리오분식': self.luo_hide_2, '광인분식': self.kwang_hide_2, '우람한 국밥': self.wooram_hide_2,
                           '애기선훈반점': self.by_sh_hide_2, '동국반점': self.dong_hide_2, '성환미쯔야': self.ksh_hide_2,
                           '선스시오': self.sun_hide_2,
                           '상준이 반마리치킨': self.sj_hide_2, 'bybyq치킨': self.byq_hide_2, '영완피자': self.wy_hide_2,
                           '돌리노피자': self.dol_hide_2, '상동버거': self.sang_hide_2,
                           '맥두리아': self.mac_hide_2}

        # 바로주문에 버튼을 보내기위한 딕트
        self.store_dict2 = {'이루오드리오분식': self.luo_hide_3, '광인분식': self.kwang_hide_3, '우람한 국밥': self.wooram_hide_3,
                            '애기선훈반점': self.by_sh_hide_3, '동국반점': self.dong_hide_3, '성환미쯔야': self.ksh_hide_3,
                            '선스시오': self.sun_hide_3,
                            '상준이 반마리치킨': self.sj_hide_3, 'bybyq치킨': self.byq_hide_3, '영완피자': self.wy_hide_3,
                            '돌리노피자': self.dol_hide_3, '상동버거': self.sang_hide_3,
                            '맥두리아': self.mac_hide_3}

        self.stackedWidget.setCurrentIndex(10)
        self.stackedWidget_5.setCurrentIndex(0)

        # 첫 실행시 로그인 / 회원가입 / 비번찾기
        self.Login_info = Login_info()
        self.pw_search = Pw_search()

        self.choicelogin_button_2.clicked.connect(self.Login_info.show)  # 회원가입
        self.main_pw_search_btn_2.clicked.connect(self.pw_search.show)  # 비밀번호 찾기
        self.login_button.clicked.connect(self.custapp)  # 로그인화면

        # 하단 버튼
        self.btn_home.clicked.connect(lambda: self.under_bar(5))
        self.btn_search.clicked.connect(lambda: self.under_bar(6))
        self.btn_like.clicked.connect(lambda: self.under_bar(7))
        self.btn_history.clicked.connect(lambda: self.under_bar(8))
        self.btn_myinfo.clicked.connect(lambda: self.under_bar(9))
        self.btn_top_search_4.clicked.connect(lambda: self.under_bar(6))

        self.notification_4.clicked.connect(lambda: self.goindex(4))
        self.btn_back.clicked.connect(lambda: self.goindex(5))

        self.lineEdit_addr_4.setText("이곳은 사용자 주소")

        self.btn_cen_delivery.clicked.connect(lambda: self.goindex_home(1))
        self.btn_cen_takeout.clicked.connect(lambda: self.goindex_home(2))

        self.currentIndex = 0
        self.btn_right.clicked.connect(lambda: self.display_ad(direction="right"))
        self.btn_left.clicked.connect(lambda: self.display_ad(direction="left"))

        self.rest_stackedWidget_3.setCurrentIndex(6)

        #홈화면에서 클릭시 해당메뉴쪽으로 넘어가는 시그널
        self.btn_fastfood.clicked.connect(lambda: self.gorestuarants(6))
        self.btn_china.clicked.connect(lambda: self.gorestuarants(1))
        self.btn_japan.clicked.connect(lambda: self.gorestuarants(2))
        self.btn_korean.clicked.connect(lambda: self.gorestuarants(0))
        self.btn_pizza.clicked.connect(lambda: self.gorestuarants(4))
        self.btn_chicken.clicked.connect(lambda: self.gorestuarants(3))
        self.btn_bunsik.clicked.connect(lambda: self.gorestuarants(5))

        #홈화면 방문포장에서 클릭시 해당메뉴쪽으로 넘어가는 시그널
        self.btn_fastfood_t.clicked.connect(lambda: self.gorestuarants(6))
        self.btn_china_t.clicked.connect(lambda: self.gorestuarants(1))
        self.btn_japan_t.clicked.connect(lambda: self.gorestuarants(2))
        self.btn_korean_t.clicked.connect(lambda: self.gorestuarants(0))
        self.btn_pizza_t.clicked.connect(lambda: self.gorestuarants(4))
        self.btn_chicken_t.clicked.connect(lambda: self.gorestuarants(3))
        self.btn_bunsik_t.clicked.connect(lambda: self.gorestuarants(5))

        #메뉴창에서 센터프레임 위쪽에 작은 아이콘들 입력시 해당메뉴로 넘어가는 시그널
        self.rest_btn_fastfood.clicked.connect(lambda: self.gorestuarants(6))
        self.rest_btn_china.clicked.connect(lambda: self.gorestuarants(1))
        self.rest_btn_japan.clicked.connect(lambda: self.gorestuarants(2))
        self.rest_btn_korea.clicked.connect(lambda: self.gorestuarants(0))
        self.rest_btn_pizza.clicked.connect(lambda: self.gorestuarants(4))
        self.rest_btn_chicken.clicked.connect(lambda: self.gorestuarants(3))
        self.rest_btn_bunsik.clicked.connect(lambda: self.gorestuarants(5))
        self.rest_btn_back.clicked.connect(lambda: self.goindex(5))

        #메뉴창에서 뽀식가게로 들어가지는 시그널
        self.bbocik_btn_1.clicked.connect(lambda: self.gorestuarants_2(0))
        self.bbocik_btn_2.clicked.connect(lambda: self.gorestuarants_2(0))
        self.bbocik_btn_3.clicked.connect(lambda: self.gorestuarants_2(0))
        self.bbocik_btn_4.clicked.connect(lambda: self.gorestuarants_2(0))

        #메뉴창에서 우람한국밥집으로 들어가지는 시그널

        self.wooram_btn_1.clicked.connect(lambda: self.gorestuarants_2(1))
        self.wooram_btn_2.clicked.connect(lambda: self.gorestuarants_2(1))
        self.wooram_btn_3.clicked.connect(lambda: self.gorestuarants_2(1))
        self.wooram_btn_4.clicked.connect(lambda: self.gorestuarants_2(1))

        #메뉴창에서  해당 중국집으로 들어가는 시그널
        self.sh_btn.clicked.connect(lambda: self.gorestuarants_2(2))
        self.sh_btn_2.clicked.connect(lambda: self.gorestuarants_2(2))
        self.sh_btn_3.clicked.connect(lambda: self.gorestuarants_2(2))
        self.sh_btn_4.clicked.connect(lambda: self.gorestuarants_2(2))
        self.dong_btn.clicked.connect(lambda: self.gorestuarants_2(3))
        self.dong_btn_2.clicked.connect(lambda: self.gorestuarants_2(3))
        self.dong_btn_3.clicked.connect(lambda: self.gorestuarants_2(3))
        self.dong_btn_4.clicked.connect(lambda: self.gorestuarants_2(3))

        # 메뉴창에서  해당 일식집으로 들어가는 시그널

        self.ksh_btn_2.clicked.connect(lambda: self.gorestuarants_2(4))
        self.ksh_btn.clicked.connect(lambda: self.gorestuarants_2(4))
        self.ksh_btn_3.clicked.connect(lambda: self.gorestuarants_2(4))
        self.ksh_btn_4.clicked.connect(lambda: self.gorestuarants_2(4))
        self.sun_btn.clicked.connect(lambda: self.gorestuarants_2(5))
        self.sun_btn_2.clicked.connect(lambda: self.gorestuarants_2(5))
        self.sun_btn_3.clicked.connect(lambda: self.gorestuarants_2(5))
        self.sun_btn_4.clicked.connect(lambda: self.gorestuarants_2(5))

        # 메뉴창에서  해당 치킨집으로 들어가는 시그널
        self.sj_btn.clicked.connect(lambda: self.gorestuarants_2(6))
        self.sj_btn_2.clicked.connect(lambda: self.gorestuarants_2(6))
        self.sj_btn_3.clicked.connect(lambda: self.gorestuarants_2(6))
        self.sj_btn_4.clicked.connect(lambda: self.gorestuarants_2(6))
        self.byq_btn.clicked.connect(lambda: self.gorestuarants_2(7))
        self.byq_btn_2.clicked.connect(lambda: self.gorestuarants_2(7))
        self.byq_btn_3.clicked.connect(lambda: self.gorestuarants_2(7))
        self.byq_btn_4.clicked.connect(lambda: self.gorestuarants_2(7))

        # 메뉴창에서  해당 피자집으로 들어가는 시그널
        self.wy_btn1.clicked.connect(lambda: self.gorestuarants_2(8))
        self.wy_btn2.clicked.connect(lambda: self.gorestuarants_2(8))
        self.wy_btn3.clicked.connect(lambda: self.gorestuarants_2(8))
        self.wy_btn4.clicked.connect(lambda: self.gorestuarants_2(8))
        self.dol_btn1.clicked.connect(lambda: self.gorestuarants_2(9))
        self.dol_btn2.clicked.connect(lambda: self.gorestuarants_2(9))
        self.dol_btn3.clicked.connect(lambda: self.gorestuarants_2(9))
        self.dol_btn4.clicked.connect(lambda: self.gorestuarants_2(9))

        # 메뉴창에서  해당 분식집으로 들어가는 시그널
        self.luo_btn_1.clicked.connect(lambda: self.gorestuarants_2(10))
        self.luo_btn_2.clicked.connect(lambda: self.gorestuarants_2(10))
        self.luo_btn_3.clicked.connect(lambda: self.gorestuarants_2(10))
        self.luo_btn_4.clicked.connect(lambda: self.gorestuarants_2(10))
        self.kwang_btn_1.clicked.connect(lambda: self.gorestuarants_2(11))
        self.kwang_btn_2.clicked.connect(lambda: self.gorestuarants_2(11))
        self.kwang_btn_3.clicked.connect(lambda: self.gorestuarants_2(11))
        self.kwang_btn_4.clicked.connect(lambda: self.gorestuarants_2(11))

        # 메뉴창에서  해당 버거집으로 들어가는 시그널
        self.sang_burger_btn.clicked.connect(lambda: self.gorestuarants_2(12))
        self.sang_burger_btn_2.clicked.connect(lambda: self.gorestuarants_2(12))
        self.sang_burger_btn_3.clicked.connect(lambda: self.gorestuarants_2(12))
        self.sang_burger_btn_4.clicked.connect(lambda: self.gorestuarants_2(12))
        self.mac_burger_btn.clicked.connect(lambda: self.gorestuarants_2(13))
        self.mac_burger_btn_2.clicked.connect(lambda: self.gorestuarants_2(13))
        self.mac_burger_btn_3.clicked.connect(lambda: self.gorestuarants_2(13))
        self.mac_burger_btn_4.clicked.connect(lambda: self.gorestuarants_2(13))

        #가게에서 빽버튼 입력시 뒤로가는 시그널
        self.BBOsick_btn_back.clicked.connect(lambda: self.close_shop(0))
        self.wooram_btn_back.clicked.connect(lambda: self.close_shop(0))
        self.baby_sh_btn_back.clicked.connect(lambda: self.close_shop(1))
        self.dong_btn_back.clicked.connect(lambda: self.close_shop(1))
        self.ksh_btn_back.clicked.connect(lambda: self.close_shop(2))
        self.sun_btn_back.clicked.connect(lambda: self.close_shop(2))
        self.jun_btn_back.clicked.connect(lambda: self.close_shop(3))
        self.by_btn_back.clicked.connect(lambda: self.close_shop(3))
        self.yw_btn_back.clicked.connect(lambda: self.close_shop(4))
        self.dol_btn_back.clicked.connect(lambda: self.close_shop(4))
        self.luo_btn_back.clicked.connect(lambda: self.close_shop(5))
        self.kwang_btn_back.clicked.connect(lambda: self.close_shop(5))
        self.sang_btn_back.clicked.connect(lambda: self.close_shop(6))
        self.mac_btn_back.clicked.connect(lambda: self.close_shop(6))

        #가게에서 돋보기 버튼을 눌렀을때 검색창으로 넘어가는 시그널
        self.BBOsick_btn_search.clicked.connect(lambda: self.goindex(6))
        self.wooram_btn_search.clicked.connect(lambda: self.goindex(6))
        self.baby_sh_btn_search.clicked.connect(lambda: self.goindex(6))
        self.dong_btn_search.clicked.connect(lambda: self.goindex(6))
        self.ksh_btn_search.clicked.connect(lambda: self.goindex(6))
        self.sun_btn_search.clicked.connect(lambda: self.goindex(6))
        self.jun_btn_search.clicked.connect(lambda: self.goindex(6))
        self.by_btn_search.clicked.connect(lambda: self.goindex(6))
        self.yw_btn_search.clicked.connect(lambda: self.goindex(6))
        self.dol_btn_search.clicked.connect(lambda: self.goindex(6))
        self.kwang_btn_search.clicked.connect(lambda: self.goindex(6))
        self.sang_btn_search.clicked.connect(lambda: self.goindex(6))
        self.mac_btn_search.clicked.connect(lambda: self.goindex(6))
        self.luo_btn_search.clicked.connect(lambda: self.goindex(6))

        # 가게내에 방문포장과 배달주문 시그널
        self.BBOsick_btn_deliv.clicked.connect(lambda: self.custUi(0, 1))
        self.BBOsick_btn_self.clicked.connect(lambda: self.custUi(0, 0))
        self.wooram_btn_deliv.clicked.connect(lambda: self.custUi2(1, 0))
        self.wooram_btn_self.clicked.connect(lambda: self.custUi2(1, 1))
        self.baby_sh_btn_deliv.clicked.connect(lambda: self.custUi3(2, 1))
        self.baby_sh_btn_self.clicked.connect(lambda: self.custUi3(2, 0))
        self.dong_btn_deliv.clicked.connect(lambda: self.custUi4(3, 1))
        self.dong_btn_self.clicked.connect(lambda: self.custUi4(3, 0))
        self.ksh_btn_deliv.clicked.connect(lambda: self.custUi5(4, 1))
        self.ksh_btn_self.clicked.connect(lambda: self.custUi5(4, 0))
        self.sun_btn_deliv.clicked.connect(lambda: self.custUi6(5, 1))
        self.sun_btn_self.clicked.connect(lambda: self.custUi6(5, 0))
        self.jun_btn_deliv.clicked.connect(lambda: self.custUi7(6, 1))
        self.jun_btn_self.clicked.connect(lambda: self.custUi7(6, 0))
        self.by_btn_deliv.clicked.connect(lambda: self.custUi8(7, 1))
        self.by_btn_self.clicked.connect(lambda: self.custUi8(7, 0))
        self.yw_btn_deliv.clicked.connect(lambda: self.custUi9(8, 1))
        self.yw_btn_self.clicked.connect(lambda: self.custUi9(8, 0))
        self.dol_btn_deliv.clicked.connect(lambda: self.custUi10(9, 1))
        self.dol_btn_self.clicked.connect(lambda: self.custUi10(9, 0))
        self.luo_btn_deliv.clicked.connect(lambda: self.custUi11(10, 1))
        self.luo_btn_self.clicked.connect(lambda: self.custUi11(10, 0))
        self.kwang_btn_deliv.clicked.connect(lambda: self.custUi12(11, 1))
        self.kwang_btn_self.clicked.connect(lambda: self.custUi12(11, 0))
        self.sang_btn_deliv.clicked.connect(lambda: self.custUi13(12, 1))
        self.sang_btn_self.clicked.connect(lambda: self.custUi13(12, 0))
        self.mac_btn_deliv.clicked.connect(lambda: self.custUi14(13, 1))
        self.mac_btn_self.clicked.connect(lambda: self.custUi14(13, 0))

        self.BBOsick_btn_menu.clicked.connect(lambda: self.custUi_2(0, 0))
        self.BBOsick_btn_info.clicked.connect(lambda: self.custUi_2(0, 1))
        self.BBOsick_btn_review.clicked.connect(lambda: self.custUi_2(0, 2))
        self.wooram_btn_menu.clicked.connect(lambda: self.custUi_2_1(1, 0))
        self.wooram_btn_info.clicked.connect(lambda: self.custUi_2_1(1, 1))
        self.wooram_btn_review.clicked.connect(lambda: self.custUi_2_1(1, 2))
        self.baby_sh_btn_menu.clicked.connect(lambda: self.custUi_2_2(2, 0))
        self.baby_sh_btn_info.clicked.connect(lambda: self.custUi_2_2(2, 1))
        self.baby_sh_btn_review.clicked.connect(lambda: self.custUi_2_2(2, 2))
        self.dong_btn_menu.clicked.connect(lambda: self.custUi_2_3(3, 0))
        self.dong_btn_info.clicked.connect(lambda: self.custUi_2_3(3, 1))
        self.dong_btn_review.clicked.connect(lambda: self.custUi_2_3(3, 2))
        self.ksh_btn_menu.clicked.connect(lambda: self.custUi_2_4(4, 0))
        self.ksh_btn_info.clicked.connect(lambda: self.custUi_2_4(4, 1))
        self.ksh_btn_review.clicked.connect(lambda: self.custUi_2_4(4, 2))
        self.sun_btn_menu.clicked.connect(lambda: self.custUi_2_5(5, 0))
        self.sun_btn_info.clicked.connect(lambda: self.custUi_2_5(5, 1))
        self.sun_btn_review.clicked.connect(lambda: self.custUi_2_5(5, 2))
        self.jun_btn_menu.clicked.connect(lambda: self.custUi_2_6(6, 0))
        self.jun_btn_info.clicked.connect(lambda: self.custUi_2_6(6, 1))
        self.jun_btn_review.clicked.connect(lambda: self.custUi_2_6(6, 2))
        self.by_btn_menu.clicked.connect(lambda: self.custUi_2_7(7, 0))
        self.by_btn_info.clicked.connect(lambda: self.custUi_2_7(7, 1))
        self.by_btn_review.clicked.connect(lambda: self.custUi_2_7(7, 2))
        self.yw_btn_menu.clicked.connect(lambda: self.custUi_2_8(8, 0))
        self.yw_btn_info.clicked.connect(lambda: self.custUi_2_8(8, 1))
        self.yw_btn_review.clicked.connect(lambda: self.custUi_2_8(8, 2))
        self.dol_btn_menu.clicked.connect(lambda: self.custUi_2_9(9, 0))
        self.dol_btn_info.clicked.connect(lambda: self.custUi_2_9(9, 1))
        self.dol_btn_review.clicked.connect(lambda: self.custUi_2_9(9, 2))
        self.luo_btn_menu.clicked.connect(lambda: self.custUi_2_10(10, 0))
        self.luo_btn_info.clicked.connect(lambda: self.custUi_2_10(10, 1))
        self.luo_btn_review.clicked.connect(lambda: self.custUi_2_10(10, 2))
        self.kwang_btn_menu.clicked.connect(lambda: self.custUi_2_11(11, 0))
        self.kwang_btn_info.clicked.connect(lambda: self.custUi_2_11(11, 1))
        self.kwang_btn_review.clicked.connect(lambda: self.custUi_2_11(11, 2))
        self.sang_btn_menu.clicked.connect(lambda: self.custUi_2_12(12, 0))
        self.sang_btn_info.clicked.connect(lambda: self.custUi_2_12(12, 1))
        self.sang_btn_review.clicked.connect(lambda: self.custUi_2_12(12, 2))
        self.mac_btn_menu.clicked.connect(lambda: self.custUi_2_13(13, 0))
        self.mac_btn_info.clicked.connect(lambda: self.custUi_2_13(13, 1))
        self.mac_btn_review.clicked.connect(lambda: self.custUi_2_13(13, 2))

        self.like_btn.clicked.connect(lambda: self.SJ_likewidget(1))  # 찜한가게
        self.pay_atonce_btn.clicked.connect(lambda: self.SJ_likewidget(2))  # 바로결제
        self.paybycall_btn.clicked.connect(lambda: self.SJ_likewidget(3))  # 전화주문
        self.like_btn.setCheckable(True)                    #마우스 클릭 고정
        self.pay_atonce_btn.setCheckable(True)              #마우스 클릭 고정
        self.paybycall_btn.setCheckable(True)               #마우스 클릭 고정



        #좋아요 눌럿을때 찜한가게에 추가되는 시그널
        self.BBOsick_btn_like.clicked.connect(lambda: self.like_copy(self.bbosik_hide))
        self.wooram_btn_like.clicked.connect(lambda: self.like_copy(self.wooram_hide))
        self.baby_sh_btn_like.clicked.connect(lambda: self.like_copy(self.by_sh_hide))
        self.dong_btn_like.clicked.connect(lambda: self.like_copy(self.dong_hide))
        self.ksh_btn_like.clicked.connect(lambda: self.like_copy(self.ksh_hide))
        self.sun_btn_like.clicked.connect(lambda: self.like_copy(self.sun_hide))
        self.jun_btn_like.clicked.connect(lambda: self.like_copy(self.sj_hide))
        self.by_btn_like.clicked.connect(lambda: self.like_copy(self.byq_hide))
        self.yw_btn_like.clicked.connect(lambda: self.like_copy(self.wy_hide))
        self.dol_btn_like.clicked.connect(lambda: self.like_copy(self.dol_hide))
        self.luo_btn_like.clicked.connect(lambda: self.like_copy(self.luo_hide))
        self.kwang_btn_like.clicked.connect(lambda: self.like_copy(self.kwang_hide))
        self.sang_btn_like.clicked.connect(lambda: self.like_copy(self.sang_hide))
        self.mac_btn_like.clicked.connect(lambda: self.like_copy(self.mac_hide))


        #좋아요 눌렀을때 메시지박스 나오는 시그널
        self.BBOsick_btn_like.clicked.connect(self.like_msg)
        self.wooram_btn_like.clicked.connect(self.like_msg)
        self.baby_sh_btn_like.clicked.connect(self.like_msg)
        self.dong_btn_like.clicked.connect(self.like_msg)
        self.ksh_btn_like.clicked.connect(self.like_msg)
        self.sun_btn_like.clicked.connect(self.like_msg)
        self.jun_btn_like.clicked.connect(self.like_msg)
        self.by_btn_like.clicked.connect(self.like_msg)
        self.yw_btn_like.clicked.connect(self.like_msg)
        self.dol_btn_like.clicked.connect(self.like_msg)
        self.luo_btn_like.clicked.connect(self.like_msg)
        self.kwang_btn_like.clicked.connect(self.like_msg)
        self.sang_btn_like.clicked.connect(self.like_msg)
        self.mac_btn_like.clicked.connect(self.like_msg)

        # 찜가게에서 해당가게로 보내주는 시그널
        self.hide_btn1.clicked.connect((lambda: self.gorestuarants_2(0)))
        self.hide_btn2.clicked.connect((lambda: self.gorestuarants_2(0)))
        self.hide_btn3.clicked.connect((lambda: self.gorestuarants_2(0)))
        self.hide_btn4.clicked.connect((lambda: self.gorestuarants_2(0)))

        self.hide_btn_1.clicked.connect((lambda: self.gorestuarants_2(1)))
        self.hide_btn_2.clicked.connect((lambda: self.gorestuarants_2(1)))
        self.hide_btn_3.clicked.connect((lambda: self.gorestuarants_2(1)))
        self.hide_btn_4.clicked.connect((lambda: self.gorestuarants_2(1)))

        self.hide_btn_9.clicked.connect((lambda: self.gorestuarants_2(2)))
        self.hide_btn_10.clicked.connect((lambda: self.gorestuarants_2(2)))
        self.hide_btn_11.clicked.connect((lambda: self.gorestuarants_2(2)))
        self.hide_btn_12.clicked.connect((lambda: self.gorestuarants_2(2)))

        self.hide_btn_13.clicked.connect((lambda: self.gorestuarants_2(3)))
        self.hide_btn_14.clicked.connect((lambda: self.gorestuarants_2(3)))
        self.hide_btn_15.clicked.connect((lambda: self.gorestuarants_2(3)))
        self.hide_btn_16.clicked.connect((lambda: self.gorestuarants_2(3)))

        self.hide_btn_17.clicked.connect((lambda: self.gorestuarants_2(4)))
        self.hide_btn_18.clicked.connect((lambda: self.gorestuarants_2(4)))
        self.hide_btn_19.clicked.connect((lambda: self.gorestuarants_2(4)))
        self.hide_btn_20.clicked.connect((lambda: self.gorestuarants_2(4)))

        self.hide_btn_21.clicked.connect((lambda: self.gorestuarants_2(5)))
        self.hide_btn_22.clicked.connect((lambda: self.gorestuarants_2(5)))
        self.hide_btn_23.clicked.connect((lambda: self.gorestuarants_2(5)))
        self.hide_btn_24.clicked.connect((lambda: self.gorestuarants_2(5)))

        self.hide_btn_25.clicked.connect((lambda: self.gorestuarants_2(6)))
        self.hide_btn_26.clicked.connect((lambda: self.gorestuarants_2(6)))
        self.hide_btn_27.clicked.connect((lambda: self.gorestuarants_2(6)))
        self.hide_btn_28.clicked.connect((lambda: self.gorestuarants_2(6)))

        self.hide_btn_29.clicked.connect((lambda: self.gorestuarants_2(7)))
        self.hide_btn_30.clicked.connect((lambda: self.gorestuarants_2(7)))
        self.hide_btn_31.clicked.connect((lambda: self.gorestuarants_2(7)))
        self.hide_btn_32.clicked.connect((lambda: self.gorestuarants_2(7)))

        self.hide_btn_33.clicked.connect((lambda: self.gorestuarants_2(8)))
        self.hide_btn_34.clicked.connect((lambda: self.gorestuarants_2(8)))
        self.hide_btn_35.clicked.connect((lambda: self.gorestuarants_2(8)))
        self.hide_btn_36.clicked.connect((lambda: self.gorestuarants_2(8)))

        self.hide_btn_37.clicked.connect((lambda: self.gorestuarants_2(9)))
        self.hide_btn_38.clicked.connect((lambda: self.gorestuarants_2(9)))
        self.hide_btn_39.clicked.connect((lambda: self.gorestuarants_2(9)))
        self.hide_btn_40.clicked.connect((lambda: self.gorestuarants_2(9)))

        self.hide_btn_41.clicked.connect((lambda: self.gorestuarants_2(10)))
        self.hide_btn_42.clicked.connect((lambda: self.gorestuarants_2(10)))
        self.hide_btn_43.clicked.connect((lambda: self.gorestuarants_2(10)))
        self.hide_btn_44.clicked.connect((lambda: self.gorestuarants_2(10)))

        self.hide_btn_45.clicked.connect((lambda: self.gorestuarants_2(11)))
        self.hide_btn_46.clicked.connect((lambda: self.gorestuarants_2(11)))
        self.hide_btn_47.clicked.connect((lambda: self.gorestuarants_2(11)))
        self.hide_btn_48.clicked.connect((lambda: self.gorestuarants_2(11)))

        self.hide_btn_49.clicked.connect((lambda: self.gorestuarants_2(12)))
        self.hide_btn_50.clicked.connect((lambda: self.gorestuarants_2(12)))
        self.hide_btn_51.clicked.connect((lambda: self.gorestuarants_2(12)))
        self.hide_btn_52.clicked.connect((lambda: self.gorestuarants_2(12)))

        self.hide_btn_53.clicked.connect((lambda: self.gorestuarants_2(13)))
        self.hide_btn_54.clicked.connect((lambda: self.gorestuarants_2(13)))
        self.hide_btn_55.clicked.connect((lambda: self.gorestuarants_2(13)))
        self.hide_btn_56.clicked.connect((lambda: self.gorestuarants_2(13)))

        # 바로결제에서 해당가게로 넘어가는 시그널
        # 뽀식이네 감자탕
        self.hide_btn_1_1_1.clicked.connect((lambda: self.gorestuarants_2(0)))
        self.hide_btn_1_1_2.clicked.connect((lambda: self.gorestuarants_2(0)))
        self.hide_btn_1_1_3.clicked.connect((lambda: self.gorestuarants_2(0)))
        self.hide_btn_1_1_4.clicked.connect((lambda: self.gorestuarants_2(0)))
        # 우람한 국밥
        self.hide_btn_1_1_5.clicked.connect((lambda: self.gorestuarants_2(1)))
        self.hide_btn_1_1_6.clicked.connect((lambda: self.gorestuarants_2(1)))
        self.hide_btn_1_1_7.clicked.connect((lambda: self.gorestuarants_2(1)))
        self.hide_btn_1_1_8.clicked.connect((lambda: self.gorestuarants_2(1)))
        # 애기선훈반점
        self.hide_btn_1_1_9.clicked.connect((lambda: self.gorestuarants_2(2)))
        self.hide_btn_1_1_10.clicked.connect((lambda: self.gorestuarants_2(2)))
        self.hide_btn_1_1_11.clicked.connect((lambda: self.gorestuarants_2(2)))
        self.hide_btn_1_1_12.clicked.connect((lambda: self.gorestuarants_2(2)))
        # 동국반점
        self.hide_btn_1_1_13.clicked.connect((lambda: self.gorestuarants_2(3)))
        self.hide_btn_1_1_14.clicked.connect((lambda: self.gorestuarants_2(3)))
        self.hide_btn_1_1_15.clicked.connect((lambda: self.gorestuarants_2(3)))
        self.hide_btn_1_1_16.clicked.connect((lambda: self.gorestuarants_2(3)))
        # 성환미쯔야
        self.hide_btn_1_1_17.clicked.connect((lambda: self.gorestuarants_2(4)))
        self.hide_btn_1_1_18.clicked.connect((lambda: self.gorestuarants_2(4)))
        self.hide_btn_1_1_19.clicked.connect((lambda: self.gorestuarants_2(4)))
        self.hide_btn_1_1_20.clicked.connect((lambda: self.gorestuarants_2(4)))
        # 선스시오
        self.hide_btn_1_1_21.clicked.connect((lambda: self.gorestuarants_2(5)))
        self.hide_btn_1_1_22.clicked.connect((lambda: self.gorestuarants_2(5)))
        self.hide_btn_1_1_23.clicked.connect((lambda: self.gorestuarants_2(5)))
        self.hide_btn_1_1_24.clicked.connect((lambda: self.gorestuarants_2(5)))
        # 상준이반마리치킨
        self.hide_btn_1_1_25.clicked.connect((lambda: self.gorestuarants_2(6)))
        self.hide_btn_1_1_26.clicked.connect((lambda: self.gorestuarants_2(6)))
        self.hide_btn_1_1_27.clicked.connect((lambda: self.gorestuarants_2(6)))
        self.hide_btn_1_1_28.clicked.connect((lambda: self.gorestuarants_2(6)))
        # bybyQ
        self.hide_btn_1_1_29.clicked.connect((lambda: self.gorestuarants_2(7)))
        self.hide_btn_1_1_30.clicked.connect((lambda: self.gorestuarants_2(7)))
        self.hide_btn_1_1_31.clicked.connect((lambda: self.gorestuarants_2(7)))
        self.hide_btn_1_1_32.clicked.connect((lambda: self.gorestuarants_2(7)))
        # 영완피자
        self.hide_btn_1_1_33.clicked.connect((lambda: self.gorestuarants_2(8)))
        self.hide_btn_1_1_34.clicked.connect((lambda: self.gorestuarants_2(8)))
        self.hide_btn_1_1_35.clicked.connect((lambda: self.gorestuarants_2(8)))
        self.hide_btn_1_1_36.clicked.connect((lambda: self.gorestuarants_2(8)))
        # 돌리노피자
        self.hide_btn_1_1_37.clicked.connect((lambda: self.gorestuarants_2(9)))
        self.hide_btn_1_1_38.clicked.connect((lambda: self.gorestuarants_2(9)))
        self.hide_btn_1_1_39.clicked.connect((lambda: self.gorestuarants_2(9)))
        self.hide_btn_1_1_40.clicked.connect((lambda: self.gorestuarants_2(9)))
        # 이루오드리오
        self.hide_btn_1_1_41.clicked.connect((lambda: self.gorestuarants_2(10)))
        self.hide_btn_1_1_42.clicked.connect((lambda: self.gorestuarants_2(10)))
        self.hide_btn_1_1_43.clicked.connect((lambda: self.gorestuarants_2(10)))
        self.hide_btn_1_1_44.clicked.connect((lambda: self.gorestuarants_2(10)))
        # 광인분식
        self.hide_btn_1_1_45.clicked.connect((lambda: self.gorestuarants_2(11)))
        self.hide_btn_1_1_46.clicked.connect((lambda: self.gorestuarants_2(11)))
        self.hide_btn_1_1_47.clicked.connect((lambda: self.gorestuarants_2(11)))
        self.hide_btn_1_1_48.clicked.connect((lambda: self.gorestuarants_2(11)))
        # 상동버거
        self.hide_btn_1_1_49.clicked.connect((lambda: self.gorestuarants_2(12)))
        self.hide_btn_1_1_50.clicked.connect((lambda: self.gorestuarants_2(12)))
        self.hide_btn_1_1_51.clicked.connect((lambda: self.gorestuarants_2(12)))
        self.hide_btn_1_1_52.clicked.connect((lambda: self.gorestuarants_2(12)))
        # 맥두리아
        self.hide_btn_1_1_53.clicked.connect((lambda: self.gorestuarants_2(13)))
        self.hide_btn_1_1_54.clicked.connect((lambda: self.gorestuarants_2(13)))
        self.hide_btn_1_1_55.clicked.connect((lambda: self.gorestuarants_2(13)))
        self.hide_btn_1_1_56.clicked.connect((lambda: self.gorestuarants_2(13)))



        # 찜가게에서 해당가게로 보내주는 시그널
        #뽀식이네 감자탕
        self.hide_btn_1_1.clicked.connect((lambda: self.gorestuarants_2(0)))
        self.hide_btn_1_2.clicked.connect((lambda: self.gorestuarants_2(0)))
        self.hide_btn_1_3.clicked.connect((lambda: self.gorestuarants_2(0)))
        self.hide_btn_1_4.clicked.connect((lambda: self.gorestuarants_2(0)))
        #우람한 국밥
        self.hide_btn_1_5.clicked.connect((lambda: self.gorestuarants_2(1)))
        self.hide_btn_1_6.clicked.connect((lambda: self.gorestuarants_2(1)))
        self.hide_btn_1_7.clicked.connect((lambda: self.gorestuarants_2(1)))
        self.hide_btn_1_8.clicked.connect((lambda: self.gorestuarants_2(1)))
        #애기선훈반점
        self.hide_btn_1_9.clicked.connect((lambda: self.gorestuarants_2(2)))
        self.hide_btn_1_10.clicked.connect((lambda: self.gorestuarants_2(2)))
        self.hide_btn_1_11.clicked.connect((lambda: self.gorestuarants_2(2)))
        self.hide_btn_1_12.clicked.connect((lambda: self.gorestuarants_2(2)))
        #동국반점
        self.hide_btn_1_13.clicked.connect((lambda: self.gorestuarants_2(3)))
        self.hide_btn_1_14.clicked.connect((lambda: self.gorestuarants_2(3)))
        self.hide_btn_1_15.clicked.connect((lambda: self.gorestuarants_2(3)))
        self.hide_btn_1_16.clicked.connect((lambda: self.gorestuarants_2(3)))
        #성환미쯔야
        self.hide_btn_1_17.clicked.connect((lambda: self.gorestuarants_2(4)))
        self.hide_btn_1_18.clicked.connect((lambda: self.gorestuarants_2(4)))
        self.hide_btn_1_19.clicked.connect((lambda: self.gorestuarants_2(4)))
        self.hide_btn_1_20.clicked.connect((lambda: self.gorestuarants_2(4)))
        #선스시오
        self.hide_btn_1_21.clicked.connect((lambda: self.gorestuarants_2(5)))
        self.hide_btn_1_22.clicked.connect((lambda: self.gorestuarants_2(5)))
        self.hide_btn_1_23.clicked.connect((lambda: self.gorestuarants_2(5)))
        self.hide_btn_1_24.clicked.connect((lambda: self.gorestuarants_2(5)))
        #상준이반마리치킨
        self.hide_btn_1_25.clicked.connect((lambda: self.gorestuarants_2(6)))
        self.hide_btn_1_26.clicked.connect((lambda: self.gorestuarants_2(6)))
        self.hide_btn_1_27.clicked.connect((lambda: self.gorestuarants_2(6)))
        self.hide_btn_1_28.clicked.connect((lambda: self.gorestuarants_2(6)))
        #bybyQ
        self.hide_btn_1_29.clicked.connect((lambda: self.gorestuarants_2(7)))
        self.hide_btn_1_30.clicked.connect((lambda: self.gorestuarants_2(7)))
        self.hide_btn_1_31.clicked.connect((lambda: self.gorestuarants_2(7)))
        self.hide_btn_1_32.clicked.connect((lambda: self.gorestuarants_2(7)))
        #영완피자
        self.hide_btn_1_33.clicked.connect((lambda: self.gorestuarants_2(8)))
        self.hide_btn_1_34.clicked.connect((lambda: self.gorestuarants_2(8)))
        self.hide_btn_1_35.clicked.connect((lambda: self.gorestuarants_2(8)))
        self.hide_btn_1_36.clicked.connect((lambda: self.gorestuarants_2(8)))
        #돌리노피자
        self.hide_btn_1_37.clicked.connect((lambda: self.gorestuarants_2(9)))
        self.hide_btn_1_38.clicked.connect((lambda: self.gorestuarants_2(9)))
        self.hide_btn_1_39.clicked.connect((lambda: self.gorestuarants_2(9)))
        self.hide_btn_1_40.clicked.connect((lambda: self.gorestuarants_2(9)))
        #이루오드리오
        self.hide_btn_1_41.clicked.connect((lambda: self.gorestuarants_2(10)))
        self.hide_btn_1_42.clicked.connect((lambda: self.gorestuarants_2(10)))
        self.hide_btn_1_43.clicked.connect((lambda: self.gorestuarants_2(10)))
        self.hide_btn_1_44.clicked.connect((lambda: self.gorestuarants_2(10)))
        #광인분식
        self.hide_btn_1_45.clicked.connect((lambda: self.gorestuarants_2(11)))
        self.hide_btn_1_46.clicked.connect((lambda: self.gorestuarants_2(11)))
        self.hide_btn_1_47.clicked.connect((lambda: self.gorestuarants_2(11)))
        self.hide_btn_1_48.clicked.connect((lambda: self.gorestuarants_2(11)))
        #상동버거
        self.hide_btn_1_49.clicked.connect((lambda: self.gorestuarants_2(12)))
        self.hide_btn_1_50.clicked.connect((lambda: self.gorestuarants_2(12)))
        self.hide_btn_1_51.clicked.connect((lambda: self.gorestuarants_2(12)))
        self.hide_btn_1_52.clicked.connect((lambda: self.gorestuarants_2(12)))
        #맥두리아
        self.hide_btn_1_53.clicked.connect((lambda: self.gorestuarants_2(13)))
        self.hide_btn_1_54.clicked.connect((lambda: self.gorestuarants_2(13)))
        self.hide_btn_1_55.clicked.connect((lambda: self.gorestuarants_2(13)))
        self.hide_btn_1_56.clicked.connect((lambda: self.gorestuarants_2(13)))

        self.btn_user_select_search.clicked.connect(self.search_dish)
        self.btn_user_select_search.clicked.connect(self.search_store_button)  # 검색버튼을 눌렀을때 해당가게 버튼이 검색목록에 나오게하는 시그널

        self.btn_search_clear.clicked.connect(self.search_clear)   #지워 버튼을 눌렀을때 목록들을 지워주는 시그널

        self.btn_user_select_search.clicked.connect(self.pay_atonce_button) #검색버튼을 눌렀을때 해당가게 버튼이 바로결제 목록에 나오는 시그널


        #전화결제에서 전화버튼누르면 나오는 메시지박스

        self.bunsik_call.clicked.connect(self.call1)
        self.chicken_call.clicked.connect(self.call2)
        self.china_call.clicked.connect(self.call3)
        self.korean_call.clicked.connect(self.call4)
        self.burger_call.clicked.connect(self.call5)
        self.japan_call.clicked.connect(self.call6)
        self.pizza_call.clicked.connect(self.call7)

        # 가게에서 전화버튼누르면 나오는 메시지박스
        self.BBOsick_btn_call.clicked.connect(self.bbosik_num)
        self.wooram_btn_call.clicked.connect(self.wooram_num)
        self.baby_sh_btn_call.clicked.connect(self.by_sh_num)
        self.dong_btn_call.clicked.connect(self.dong_num)
        self.ksh_btn_call.clicked.connect(self.ksh_num)
        self.sun_btn_call.clicked.connect(self.sun_num)
        self.jun_btn_call.clicked.connect(self.jun_num)
        self.by_btn_call.clicked.connect(self.byq_num)
        self.yw_btn_call.clicked.connect(self.yw_num)
        self.dol_btn_call.clicked.connect(self.dol_num)
        self.luo_btn_call.clicked.connect(self.luo_num)
        self.kwang_btn_call.clicked.connect(self.kwang_num)
        self.sang_btn_call.clicked.connect(self.sang_num)
        self.mac_btn_call.clicked.connect(self.mac_num)

        # 식당 스핀박스
        self.spinBox_amount.valueChanged.connect(self.spin)

        # 식당 담기버튼
        self.btn_pay.clicked.connect(self.last_order)
        # 식당 결제버튼
        self.btn_pay_2.clicked.connect(self.payment)

        # 뽀식이네 감자탕집에서 주문   이름이 적힌 버튼이 딕셔너리의 키값과 일치해야합니다
        self.btn_dish1_9.clicked.connect(
            lambda a, kind="한식", shop="뽀식이네 감자탕", menu="감자탕": self.order(a, kind, shop, menu))
        self.btn_dish1_10.clicked.connect(
            lambda a, kind="한식", shop="뽀식이네 감자탕", menu="우거지해장국": self.order(a, kind, shop, menu))
        self.btn_dish1_11.clicked.connect(
            lambda a, kind="한식", shop="뽀식이네 감자탕", menu="소머리국밥": self.order(a, kind, shop, menu))
        self.btn_dish1_12.clicked.connect(
            lambda a, kind="한식", shop="뽀식이네 감자탕", menu="설렁탕": self.order(a, kind, shop, menu))
        # 우람한 국밥 주문
        self.btn_dish1.clicked.connect(
            lambda a, kind="한식", shop="우람한 국밥", menu="순대국밥": self.order(a, kind, shop, menu))
        self.btn_dish1_2.clicked.connect(
            lambda a, kind="한식", shop="우람한 국밥", menu="소머리국밥": self.order(a, kind, shop, menu))
        self.btn_dish1_3.clicked.connect(
            lambda a, kind="한식", shop="우람한 국밥", menu="굴국밥": self.order(a, kind, shop, menu))
        self.btn_dish1_4.clicked.connect(
            lambda a, kind="한식", shop="우람한 국밥", menu="설렁탕": self.order(a, kind, shop, menu))

        # 애기선훈반점
        self.btn_dish1_5.clicked.connect(
            lambda a, kind="중식", shop="애기선훈반점", menu="짜장면": self.order(a, kind, shop, menu))
        self.btn_dish1_6.clicked.connect(
            lambda a, kind="중식", shop="애기선훈반점", menu="짬뽕": self.order(a, kind, shop, menu))
        self.btn_dish1_7.clicked.connect(
            lambda a, kind="중식", shop="애기선훈반점", menu="볶음밥": self.order(a, kind, shop, menu))
        self.btn_dish1_8.clicked.connect(
            lambda a, kind="중식", shop="애기선훈반점", menu="탕수육": self.order(a, kind, shop, menu))

        # 동국반점
        self.btn_dish1_17.clicked.connect(
            lambda a, kind="중식", shop="동국반점", menu="짜장면": self.order(a, kind, shop, menu))
        self.btn_dish1_18.clicked.connect(
            lambda a, kind="중식", shop="동국반점", menu="짬뽕": self.order(a, kind, shop, menu))
        self.btn_dish1_19.clicked.connect(
            lambda a, kind="중식", shop="동국반점", menu="팔보채": self.order(a, kind, shop, menu))
        self.btn_dish1_20.clicked.connect(
            lambda a, kind="중식", shop="동국반점", menu="양장피": self.order(a, kind, shop, menu))

        # 성환미쯔야
        self.btn_dish1_33.clicked.connect(
            lambda a, kind="일식", shop="성환미쯔야", menu="돈코츠라멘": self.order(a, kind, shop, menu))
        self.btn_dish1_34.clicked.connect(
            lambda a, kind="일식", shop="성환미쯔야", menu="미소라멘": self.order(a, kind, shop, menu))
        self.btn_dish1_35.clicked.connect(
            lambda a, kind="일식", shop="성환미쯔야", menu="돈까스": self.order(a, kind, shop, menu))
        self.btn_dish1_36.clicked.connect(
            lambda a, kind="일식", shop="성환미쯔야", menu="초밥12p": self.order(a, kind, shop, menu))

        # 선스시오
        self.btn_dish1_29.clicked.connect(
            lambda a, kind="일식", shop="선스시오", menu="초밥12p": self.order(a, kind, shop, menu))
        self.btn_dish1_30.clicked.connect(
            lambda a, kind="일식", shop="선스시오", menu="돈까스": self.order(a, kind, shop, menu))
        self.btn_dish1_31.clicked.connect(
            lambda a, kind="일식", shop="선스시오", menu="초밥20p": self.order(a, kind, shop, menu))
        self.btn_dish1_32.clicked.connect(
            lambda a, kind="일식", shop="선스시오", menu="광어회": self.order(a, kind, shop, menu))


        # 상준이 반마리 치킨
        self.btn_dish1_13.clicked.connect(
            lambda a, kind="치킨", shop="상준이 반마리치킨", menu="후라이드": self.order(a, kind, shop, menu))
        self.btn_dish1_14.clicked.connect(
            lambda a, kind="치킨", shop="상준이 반마리치킨", menu="양념치킨": self.order(a, kind, shop, menu))
        self.btn_dish1_15.clicked.connect(
            lambda a, kind="치킨", shop="상준이 반마리치킨", menu="간장치킨": self.order(a, kind, shop, menu))
        self.btn_dish1_16.clicked.connect(
            lambda a, kind="치킨", shop="상준이 반마리치킨", menu="치즈볼": self.order(a, kind, shop, menu))

        # bybyq치킨
        self.btn_dish1_37.clicked.connect(
            lambda a, kind="치킨", shop="bybyq치킨", menu="후라이드": self.order(a, kind, shop, menu))
        self.btn_dish1_38.clicked.connect(
            lambda a, kind="치킨", shop="bybyq치킨", menu="양념치킨": self.order(a, kind, shop, menu))
        self.btn_dish1_39.clicked.connect(
            lambda a, kind="치킨", shop="bybyq치킨", menu="스노윙치킨": self.order(a, kind, shop, menu))
        self.btn_dish1_40.clicked.connect(
            lambda a, kind="치킨", shop="bybyq치킨", menu="치즈스틱": self.order(a, kind, shop, menu))

        # 영완피자
        self.btn_dish1_41.clicked.connect(
            lambda a, kind="피자", shop="영완피자", menu="불고기피자": self.order(a, kind, shop, menu))
        self.btn_dish1_42.clicked.connect(
            lambda a, kind="피자", shop="영완피자", menu="콤비네이션피자": self.order(a, kind, shop, menu))
        self.btn_dish1_43.clicked.connect(
            lambda a, kind="피자", shop="영완피자", menu="쉬림프피자": self.order(a, kind, shop, menu))
        self.btn_dish1_44.clicked.connect(
            lambda a, kind="피자", shop="영완피자", menu="하와이안피자": self.order(a, kind, shop, menu))


        # 돌리노피자
        self.btn_dish1_45.clicked.connect(
            lambda a, kind="피자", shop="돌리노피자", menu="불고기피자": self.order(a, kind, shop, menu))
        self.btn_dish1_46.clicked.connect(
            lambda a, kind="피자", shop="돌리노피자", menu="콤비네이션피자": self.order(a, kind, shop, menu))
        self.btn_dish1_47.clicked.connect(
            lambda a, kind="피자", shop="돌리노피자", menu="쉬림프피자": self.order(a, kind, shop, menu))
        self.btn_dish1_48.clicked.connect(
            lambda a, kind="피자", shop="돌리노피자", menu="하와이안피자": self.order(a, kind, shop, menu))


        # 이루오드리오분식
        self.btn_dish1_49.clicked.connect(
            lambda a, kind="분식", shop="이루오드리오분식", menu="김밥": self.order(a, kind, shop, menu))
        self.btn_dish1_50.clicked.connect(
            lambda a, kind="분식", shop="이루오드리오분식", menu="떡볶이": self.order(a, kind, shop, menu))
        self.btn_dish1_51.clicked.connect(
            lambda a, kind="분식", shop="이루오드리오분식", menu="순대": self.order(a, kind, shop, menu))
        self.btn_dish1_52.clicked.connect(
            lambda a, kind="분식", shop="이루오드리오분식", menu="모듬튀김": self.order(a, kind, shop, menu))

        # 광인분식
        self.btn_dish1_53.clicked.connect(
            lambda a, kind="분식", shop="광인분식", menu="김밥": self.order(a, kind, shop, menu))
        self.btn_dish1_54.clicked.connect(
            lambda a, kind="분식", shop="광인분식", menu="라면": self.order(a, kind, shop, menu))
        self.btn_dish1_55.clicked.connect(
            lambda a, kind="분식", shop="광인분식", menu="떡볶이": self.order(a, kind, shop, menu))
        self.btn_dish1_56.clicked.connect(
            lambda a, kind="분식", shop="광인분식", menu="제육덮밥": self.order(a, kind, shop, menu))

        # 상동버거
        self.btn_dish1_57.clicked.connect(
            lambda a, kind="패스트푸드", shop="상동버거", menu="불고기버거": self.order(a, kind, shop, menu))
        self.btn_dish1_58.clicked.connect(
            lambda a, kind="패스트푸드", shop="상동버거", menu="상하이버거": self.order(a, kind, shop, menu))
        self.btn_dish1_59.clicked.connect(
            lambda a, kind="패스트푸드", shop="상동버거", menu="치즈버거": self.order(a, kind, shop, menu))
        self.btn_dish1_60.clicked.connect(
            lambda a, kind="패스트푸드", shop="상동버거", menu="치킨버거": self.order(a, kind, shop, menu))

        # 맥두리아
        self.btn_dish1_61.clicked.connect(
            lambda a, kind="패스트푸드", shop="맥두리아", menu="불고기버거": self.order(a, kind, shop, menu))
        self.btn_dish1_62.clicked.connect(
            lambda a, kind="패스트푸드", shop="맥두리아", menu="치즈버거": self.order(a, kind, shop, menu))
        self.btn_dish1_63.clicked.connect(
            lambda a, kind="패스트푸드", shop="맥두리아", menu="슈맥버거": self.order(a, kind, shop, menu))
        self.btn_dish1_64.clicked.connect(
            lambda a, kind="패스트푸드", shop="맥두리아", menu="새우버거": self.order(a, kind, shop, menu))

        # 결재확인 버튼
        self.system_btn1.clicked.connect(self.pay)
        self.system_btn2.clicked.connect(self._back)
        self.system_btn3.clicked.connect(self.no_show)

        # My배민버튼 btn_Myinfo (내정보)버튼, btn_Myinfo_edit (내 정보 수정)버튼
        self.btn_Myinfo.clicked.connect(self.Mybaemin_MYINFO)
        self.btn_Myinfo_edit.clicked.connect(self.Mybaemin_MYINFO_AMEND)

        # 닉네임, 이름, 아이디, 전화번호, 주소 변경 버튼
        self.btn_edit_2.clicked.connect((lambda: self.Myinfo_edit_name(1)))  # 이름
        self.btn_edit_1.clicked.connect((lambda: self.Myinfo_edit_name(4)))  # 닉네임
        self.btn_edit_4.clicked.connect((lambda: self.Myinfo_edit_name(3)))  # 전화번호
        self.btn_edit_5.clicked.connect((lambda: self.Myinfo_edit_name(2)))  # 주소

        self.btn_login.clicked.connect(self.login_)
        self.btn_logout.clicked.connect(self.logout)
        self.btn_signup.clicked.connect(self.signup_)

        self.login_status = False

        # 주문 내역 버튼 이름변수 뒤 붙게 될 수
        self.frame_no = 1
        self.btn_start_no = 1
        self.btn_end_no = 3
        self.label_start_no = 1
        self.label_end_no = 3

        self.index = 0

        self.listWidget_2.setItemAlignment(Qt.AlignLeft)

    def initUI(self):
        self.setWindowTitle('B달의 민족')
        self.resize(500, 350)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def login_(self):
        if not self.login_status:
            self.stackedWidget.setCurrentIndex(10)
        else:
            pass

    def signup_(self):
        if not self.login_status:
            self.Login_info.show()
        else:
            pass

    def logout(self):
        if self.login_status:
            self.stackedWidget.setCurrentIndex(10)
            self.basket = []
            user_info_vars = [self.user_name, self.user_phone, self.user_id, self.user_addr,
                              self.user_nickname_2, self.user_name_2, self.user_phone_2, self.user_id_2, self.user_addr_2]
            for user_info_var in user_info_vars:
                user_info_var.clear()
            self.current_id = None
            self.nickname_show.setText('더귀한분, ')
            self.lineEdit_addr_4.setText('로그인을 먼저 해주세요.')
        else:
            pass

    def nickname_show_(self):
        self.current_id = self.id_main_2.text()
        self.user_infos = self.Login_info.login
        if len(self.user_infos[self.current_id]) > 4:
            nick_name = self.user_infos[self.current_id][-1]
            self.nickname_show.setText('더귀한분, {}'.format(str(nick_name)))
            print(nick_name)
        else:
            self.nickname_show.setText('더귀한분, ')
            print("nada")

    # 로그인 눌렀을시 함수
    def custapp(self):
        if self.id_main_2.text() in self.Login_info.login.keys():
            if self.pw_main_2.text() == self.Login_info.login[self.id_main_2.text()][0]:
                # 로그인 성공시
                self.current_id = self.id_main_2.text()
                self.show_userinfo()
                self.nickname_show_()
                self.stackedWidget.setCurrentIndex(4)  ## 홈화면가기
                self.login_status = True
                self.pw_main_2.setText('')
            else:
                self.statusbar.setText("비번이 맞지않습니다.")
        else:
            self.statusbar.setText("입력하신 ID로 가입된 정보가 없습니다.")

    # 로그인하면 해당 아이디의 사용자 정보를 보여줌
    def show_userinfo(self):
        self.current_id = self.id_main_2.text()
        self.user_infos = self.Login_info.login
        print(self.current_id)
        print(self.user_infos)
        if self.current_id:
            # My배민 페이지에서 (내정보) 이름/아이디/전화번호/주소를 현 로그인한 사용자 정보로 보여주기
            self.user_name.setText(self.user_infos[self.current_id][1])  ##이름
            self.user_id.setText(self.current_id)  ##아이디
            self.user_phone.setText(self.user_infos[self.current_id][3])  ##폰번호
            self.user_addr.setText(self.user_infos[self.current_id][2])  ##주소
            self.lineEdit_addr_4.setText(self.user_infos[self.current_id][2])  ##메인화면 상단 사용자 주소

            # My배민 페이지에서 (내정보수정) 이름/아이디/전화번호/주소를 현 로그인한 사용자 정보로 보여주기
            self.user_name_2.setText(self.user_infos[self.current_id][1])  ##이름
            self.user_id_2.setText(self.current_id)  ##아이디
            self.user_addr_2.setText(self.user_infos[self.current_id][2])  ##주소
            self.user_phone_2.setText(self.user_infos[self.current_id][3])  ##폰번호
            try:
                self.user_nickname_2.setText(self.user_infos[self.current_id][4])       ##닉네임
            except IndexError:
                pass

    # 내 정보 수정
    def Myinfo_edit_name(self, x):
        self.current_id = self.id_main_2.text()
        self.user_infos = self.Login_info.login
        print(self.current_id)
        msg = "정보를 변경하시겠습니까?"
        info_question = QMessageBox.question(self, '변경하시겠습니까?', msg, QMessageBox.Yes | QMessageBox.No)
        try:
            if info_question == QMessageBox.Yes:
                QMessageBox.about(self, "저장", "입력하신 정보로 저장되었습니다.")
                if x == 1:
                    self.user_infos[self.current_id][x] = self.user_name_2.text()  # 이름
                elif x == 2:
                    self.user_infos[self.current_id][x] = self.user_addr_2.toPlainText()  # 주소
                elif x == 3:
                    self.user_infos[self.current_id][x] = self.user_phone_2.text()  # 전화번호
                    # self.Login_info.login[self.current_id] = self.user_id_2.text()            # 아이디
                elif x == 4:
                    new_nickname = self.user_nickname_2.text()
                    if len(self.user_infos[self.current_id]) >= x+1:  # 닉네임
                        self.user_infos[self.current_id][x] = new_nickname
                        print(self.user_infos)
                    else:
                        self.user_infos[self.current_id].append(new_nickname)
                        print(self.user_infos)
                    self.nickname_show.setText('더귀한분, '+ new_nickname)
            elif info_question == QMessageBox.No:
                pass
                # 바뀐 정보 저장
            with open("log.pickle", 'wb')as f:
                pickle.dump(self.user_infos, f)
        except KeyError:
            print("로그인을 먼저 해주세요!")
            self.stackedWidget.setCurrentIndex(10)
            self.statusbar.setText("로그인을 먼저 해주세요!")

    def Mybaemin_MYINFO(self):
        self.stackedWidget_profile.setCurrentIndex(0)

    def Mybaemin_MYINFO_AMEND(self):
        self.stackedWidget_profile.setCurrentIndex(1)

    def like_copy(self,k):
        self.verticalLayout1.addWidget(k)

    def goindex(self, index_no):
        self.stackedWidget.setCurrentIndex(index_no-1)


    def goindex_home(self, index_no):
        self.stackedWidget_5.setCurrentIndex(index_no-1)

    def gorestuarants(self, index_no):
        self.stackedWidget.setCurrentIndex(2)
        self.rest_stackedWidget_3.setCurrentIndex(index_no)

    def gorestuarants_2(self, index_no):
        self.basket_price = 0
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_no)

    def custUi(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_7.setCurrentIndex(index_no)

    def custUi2(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_12.setCurrentIndex(index_no)

    def custUi3(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_14.setCurrentIndex(index_no)

    def custUi4(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_16.setCurrentIndex(index_no)

    def custUi5(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_18.setCurrentIndex(index_no)

    def custUi6(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_20.setCurrentIndex(index_no)

    def custUi7(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_22.setCurrentIndex(index_no)

    def custUi8(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_24.setCurrentIndex(index_no)

    def custUi9(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_26.setCurrentIndex(index_no)

    def custUi10(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_28.setCurrentIndex(index_no)

    def custUi11(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_30.setCurrentIndex(index_no)

    def custUi12(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_32.setCurrentIndex(index_no)

    def custUi13(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_34.setCurrentIndex(index_no)

    def custUi14(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_36.setCurrentIndex(index_no)

    def custUi_2(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_8.setCurrentIndex(index_no)

    def custUi_2_1(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_13.setCurrentIndex(index_no)

    def custUi_2_2(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_15.setCurrentIndex(index_no)

    def custUi_2_3(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_17.setCurrentIndex(index_no)

    def custUi_2_4(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_19.setCurrentIndex(index_no)

    def custUi_2_5(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_21.setCurrentIndex(index_no)

    def custUi_2_6(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_23.setCurrentIndex(index_no)

    def custUi_2_7(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_25.setCurrentIndex(index_no)

    def custUi_2_8(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_27.setCurrentIndex(index_no)

    def custUi_2_9(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_29.setCurrentIndex(index_no)

    def custUi_2_10(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_31.setCurrentIndex(index_no)

    def custUi_2_11(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_33.setCurrentIndex(index_no)

    def custUi_2_12(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_35.setCurrentIndex(index_no)

    def custUi_2_13(self, index_non, index_no):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_4.setCurrentIndex(index_non)
        self.stackedWidget_37.setCurrentIndex(index_no)

    def display_ad(self, direction=None):
        len_ads = 16
        if direction == 'right':
            self.currentIndex += 1
        elif direction == 'left':
            self.currentIndex -= 1
        if self.currentIndex > len_ads:
            self.currentIndex = 0
        elif self.currentIndex < 0:
            self.currentIndex = len_ads
        self.stackedWidget_2.setCurrentIndex(self.currentIndex)
        print(self.currentIndex)



    def SJ_likewidget(self,index_no):  #찜한가게 바로결제 전화주문으로 넘어가는 함수
        self.likedwidget.setCurrentIndex(index_no-1)

    def search_dish(self):
        ## new_all_dict = {가게이름: [가게이름, 가게메뉴(하나의 str으로 join처리됨)]
        ## 위 형태의 새로운 딕셔너리 전처리 과정
        cuisines = list(self.all_dict.keys())
        business_names = []
        business_infos = []
        for i, cuisine in enumerate(cuisines):
            globals()['business_{}'.format(i + 1)] = list(self.all_dict[cuisine].keys())
            globals()['business_info_{}'.format(i + 1)] = list(self.all_dict[cuisine].values())
            business_names.append(globals()['business_{}'.format(i + 1)])
            business_infos.append(globals()['business_info_{}'.format(i + 1)])
        business_infos = sum(business_infos, [])
        business_names = sum(business_names, [])
        new_all_dict = {}
        for i in range(len(business_infos)):
            new_all_dict[business_names[i]] = [business_names[i], ' '.join(business_infos[i].keys())[3:]]

        self.search_result_status = False
        ## 검색어를 매칭해서 가게이름과 가게정보를 끌어오는 코드
        search_word = self.user_searchbar.text()
        for name, dishes in list(new_all_dict.values()):
            if search_word in dishes:
                self.search_result_status = True
                for cuisine, v in self.all_dict.items():
                    try:
                        ### 검색성공시 결과
                        ##### 이 부분에 실제 보여지는 버튼을 연결하는 코드 작성하면 끝! #####
                        print(name, v[name])
                        print(name)

                        self.search_name_list.append(name)
                        self.search_name_list2.append(name)
                        print(self.search_name_list)

                        # self.search_stores.addItem("{}\n{}".format(name, v[name]))
                    except KeyError:
                        pass
        if self.search_result_status:
            self.search_result_status = False
            if len(search_word) == 0:
                self.search_name_list.clear()
                self.search_name_list2.clear()
                self.search_msg_box2()
        elif self.search_result_status == False:
            self.search_msg_box()


   # 검색하면 검색목록에 버튼을 보여주는함수

    def search_store_button(self):
        for i in self.search_name_list:
            if i in self.store_dict.keys():
                self.verticalLayout_search.addWidget(self.store_dict[i])

    # 검색하면 바로결제 목록에 버튼을 띄어주는 함수
    def pay_atonce_button(self):
        for i in self.search_name_list2:
            if i in self.store_dict.keys():
                self.verticalLayout_pay_atonce.addWidget(self.store_dict2[i])


    # 클리어시 버튼을 돌려보내는 함수

    def search_clear(self):
        for i in self.search_name_list:
            if i in self.store_dict.keys():
                self.verticalLayout_hide.addWidget(self.store_dict[i])
        self.search_name_list.clear()
        self.user_searchbar.clear()

    # 가게 위젯에서 주문해주는 함수입니다
    def order(self, a, kind, shop, menu):
        self.spinBox_amount.setValue(0)
        price = self.all_dict[kind][shop][menu]
        self.price = str(price)
        self.name = menu
        self.now_kind = kind
        self.now_shop = shop
        self.count = 0
        self.now_price = int(self.price) * int(self.count)
        self.now_price = str(self.now_price)
        self.menu_show_pay.setText(f"{self.name}\t{self.count}\t{self.now_price}")
        self.price_show_pay.setText("")

    # 스핀위젯으로 갯수조정할수 있는 함수입니다
    def spin(self):
        try:
            self.count = self.spinBox_amount.value()
            cow = "0"
            if int(cow) < int(self.count):
                self.now_price = int(self.price) * int(self.count)
                self.now_price = str(self.now_price)
                cow = self.count
                self.menu_show_pay.setText(f"{self.name} / {self.count}개 / {self.now_price}원")
            elif int(cow) > int(self.count):
                self.now_price = int(self.price) * int(self.count)
                self.now_price = str(self.now_price)
                cow = self.count
                self.menu_show_pay.setText(f"{self.name} / {self.count}개 / {self.now_price}원")
        except:
            self.system_msg = QMessageBox()
            self.system_msg.setWindowTitle("system")
            self.system_msg.setStandardButtons(QMessageBox.Ok)
            self.system_msg.setText("메뉴를 선택해주세요")
            self.system_msg.show()
            self.spinBox_amount.setValue(0)

    # 한가게에서 주문한 목록을 쌓아둠
    def last_order(self):
        try:
            if self.count == 0:
                self.system_msg = QMessageBox()
                self.system_msg.setWindowTitle("system")
                self.system_msg.setStandardButtons(QMessageBox.Ok)
                self.system_msg.setText("수량을 선택해 주세요")
                self.system_msg.show()
            elif int(self.count) > 0:
                self.system_msg1 = QMessageBox()
                self.system_msg1.setWindowTitle("system")
                self.system_msg1.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                self.system_msg1.setText("장바구니에 추가하시겠습니까?")
                self.system_msg1.show()
                retval = self.system_msg1.exec_()
                if retval == QMessageBox.Yes:
                    if len(self.basket) == 0:
                        a = self.menu_show_pay.text()
                        self.listWidget_2.addItem(a)
                        self.basket.append([self.name, self.count, self.now_price])
                        basket_price = self.basket_price + int(self.now_price)
                        self.basket_price = basket_price
                        self.price_show_pay.setText(f"{self.name},{self.count}개 장바구니 담기 완료")
                        self.menu_show_pay.setText("")
                        self.spinBox_amount.setValue(0)
                        print(self.basket)

                    elif len(self.basket) > 0:
                        transposed_basket = list(map(list, zip(*self.basket)))
                        if self.name not in transposed_basket[0]:
                            a = self.menu_show_pay.text()
                            self.listWidget_2.addItem(a)
                            self.basket.append([self.name, self.count, self.now_price])
                            self.basket_price += int(self.now_price)
                            self.price_show_pay.setText(f"{self.name},{self.count}개 장바구니 담기 완료")
                            self.menu_show_pay.setText("")
                            self.spinBox_amount.setValue(0)
                            print(self.basket)
                        else:
                            a = self.menu_show_pay.text()
                            self.listWidget_2.addItem(a)
                            dup_index = transposed_basket[0].index(self.name)
                            transposed_basket[1][dup_index] += self.count
                            transposed_basket[2][dup_index] = str(int(transposed_basket[2][dup_index]) + int(self.now_price))
                            self.basket = list(map(list, zip(*transposed_basket)))
                            self.basket_price += int(self.now_price)
                            self.price_show_pay.setText(f"{self.name},{self.count}개 장바구니에 추가")
                            self.menu_show_pay.setText("")
                            self.spinBox_amount.setValue(0)
                            print(self.basket)
                else:
                    pass
        except:
            self.system_msg = QMessageBox()
            self.system_msg.setWindowTitle("system")
            self.system_msg.setStandardButtons(QMessageBox.Ok)
            self.system_msg.setText("메뉴를 선택해 주세요")
            self.system_msg.show()
            pass

    # 그 가게에서 주문을 마치고 나감
    def close_shop(self, index_no=0):
        # 아무것도 결제하지 않았을때 그냥나감
        if len(self.basket) == 0:
            self.stackedWidget.setCurrentIndex(2)
            self.stackedWidget_4.setCurrentIndex(index_no)
        # 결제를 했을때 확인창이 뜸
        elif len(self.basket) > 0:
            self.system_msg = QMessageBox()
            self.system_msg.setWindowTitle("system")
            self.system_msg.setStandardButtons(QMessageBox.Ok)
            self.system_msg.setText(f"미결제 상품이 있습니다")
            self.system_msg.show()
            self.deliv = self.all_dict[self.now_kind][self.now_shop]["정보"][2]
            self.lineEdit_system_shop.setText(self.now_shop)
            a = int(self.basket_price) + int(self.deliv)
            self.lineEdit_system.setText(f" 배달료: {self.deliv}원\t\t총결제 금액: {str(a)}원")
            self.stackedWidget.setCurrentIndex(0)
            self.stackedWidget_9.setCurrentIndex(0)

    def under_bar(self, index_no):
        # 아무것도 결제하지 않았을때 그냥나감
        if len(self.basket) == 0:
            self.stackedWidget.setCurrentIndex(index_no - 1)
            if index_no == 9:
                self.stackedWidget_profile.setCurrentIndex(0)
        # 결제를 했을때 확인창이 뜸
        elif len(self.basket) > 0:
            return self.close_shop()

    def payment(self):
        if len(self.basket) == 0:
            self.system_msg = QMessageBox()
            self.system_msg.setWindowTitle("system")
            self.system_msg.setStandardButtons(QMessageBox.Ok)
            self.system_msg.setText(f"장바구니에 상품이 없습니다")
            self.system_msg.show()

        elif len(self.basket) > 0:
            self.deliv = self.all_dict[self.now_kind][self.now_shop]["정보"][2]
            self.lineEdit_system_shop.setText(self.now_shop)
            a = int(self.basket_price) + int(self.deliv)
            self.lineEdit_system.setText(f" 배달료: {self.deliv}원\t\t총결제 금액: {str(a)}원")
            self.stackedWidget.setCurrentIndex(0)
            self.stackedWidget_9.setCurrentIndex(0)

    def pay(self):
        if self.login_status:
            low_price = self.all_dict[self.now_kind][self.now_shop]["정보"][3]
            if self.basket_price < int(low_price):
                self.system_msg = QMessageBox()
                self.system_msg.setWindowTitle("system")
                self.system_msg.setStandardButtons(QMessageBox.Ok)
                self.system_msg.setText(f"최소주문 금액은 {low_price}원입니다")
                self.system_msg.show()
            else:
                self.system_msg1 = QMessageBox()
                self.system_msg1.setWindowTitle("system")
                self.system_msg1.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                self.system_msg1.setText("결재 하시겠습니까?")
                self.system_msg1.show()
                retval = self.system_msg1.exec_()
                if retval == QMessageBox.Yes:
                    tm = time.localtime()
                    self.order_time = [tm.tm_year, tm.tm_mon, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec,
                                       self.user_infos[self.current_id][1], self.user_infos[self.current_id][2]]
                    self.basket.append(self.order_time.copy())
                    self.basket_3 = self.basket.copy()
                    basket = [self.basket_3].copy()
                    if self.now_shop in self.basket_2.keys():  # 저번에 구매했던 가게에서 또 주문할때 뒤로
                        self.basket_2[self.now_shop] = self.basket_2[self.now_shop] + basket.copy()

                    elif self.now_shop not in self.basket_2.keys():  # 첫구매시 딕셔너리에 추가
                        self.basket_2[self.now_shop] = basket.copy()
                    self.all_basket.append(basket)
                    self.listWidget_2.clear()
                    self.all_price = self.basket_price
                    # self.basket_price = 0
                    print(self.basket_2)
                    self.basket.clear()
                    with open("basket.pickle", 'wb')as f:                                                #업체측에 주는 피클정보
                        pickle.dump(self.basket_2, f)

                    with open("user_basket.pickle", 'wb')as ff:
                        user_basket = {}
                        user_basket[self.user_infos[self.current_id][1]] = self.basket_2
                        pickle.dump(user_basket, ff)                                                     #전체 유저 주문목록 저장
                    self.add_history()
                    self.stackedWidget.setCurrentIndex(7)
                else:
                    pass
        else:
            self.stackedWidget.setCurrentIndex(10)
            self.statusbar.setText("주문결제를 하시려면 로그인을 먼저 해주세요.")

    # 더사기
    def _back(self):
        if self.now_shop == "뽀식이네 감자탕":
            self.stackedWidget.setCurrentIndex(1)
            self.stackedWidget_4.setCurrentIndex(0)
        elif self.now_shop == "우람한 국밥":
            self.stackedWidget.setCurrentIndex(1)
            self.stackedWidget_4.setCurrentIndex(1)
        elif self.now_shop == "애기선훈반점":
            self.stackedWidget.setCurrentIndex(1)
            self.stackedWidget_4.setCurrentIndex(2)
        elif self.now_shop == "동국반점":
            self.stackedWidget.setCurrentIndex(1)
            self.stackedWidget_4.setCurrentIndex(3)
        elif self.now_shop == "성환미쯔야":
            self.stackedWidget.setCurrentIndex(1)
            self.stackedWidget_4.setCurrentIndex(4)
        elif self.now_shop == "선스시오":
            self.stackedWidget.setCurrentIndex(1)
            self.stackedWidget_4.setCurrentIndex(5)
        elif self.now_shop == "상준이 반마리치킨":
            self.stackedWidget.setCurrentIndex(1)
            self.stackedWidget_4.setCurrentIndex(6)
        elif self.now_shop == "bybyq치킨":
            self.stackedWidget.setCurrentIndex(1)
            self.stackedWidget_4.setCurrentIndex(7)
        elif self.now_shop == "영완피자":
            self.stackedWidget.setCurrentIndex(1)
            self.stackedWidget_4.setCurrentIndex(8)
        elif self.now_shop == "돌리노피자":
            self.stackedWidget.setCurrentIndex(1)
            self.stackedWidget_4.setCurrentIndex(9)
        elif self.now_shop == "이루오드리오분식":
            self.stackedWidget.setCurrentIndex(1)
            self.stackedWidget_4.setCurrentIndex(10)
        elif self.now_shop == "광인분식":
            self.stackedWidget.setCurrentIndex(1)
            self.stackedWidget_4.setCurrentIndex(11)
        elif self.now_shop == "상동버거":
            self.stackedWidget.setCurrentIndex(1)
            self.stackedWidget_4.setCurrentIndex(12)
        elif self.now_shop == "맥두리아":
            self.stackedWidget.setCurrentIndex(1)
            self.stackedWidget_4.setCurrentIndex(13)

    def no_show(self):
        self.basket.clear()
        self.listWidget_2.clear()
        return self.close_shop()

    def add_history(self):
        self.detail_btn_no = self.btn_end_no
        self.new_orders = {}
        time_stamp = str(time.strftime('%y-%m-%d %H:%M:%S'))

        details_text = "\n"
        for m, a, p in self.basket_2[self.now_shop][-1][:-1]:
            details_text += m+" "
            details_text += str(a)+"개"
            details_text += str(p)+"원\n"
        details_text += "배달팁: {}원".format(str(self.deliv))

        if len(self.basket_2[self.now_shop][-1]) > 2:
            details = "{} 외 {}개 주문 / 총결제금액: {}원".format(self.basket_2[self.now_shop][-1][0][0],
                                                   len(self.basket_2[self.now_shop][-1])-2,
                                                   int(self.basket_price)+int(self.deliv))
        else:
            details = "{} {}개 주문 / 총결제금액: {}원".format(self.basket_2[self.now_shop][-1][0][0],
                                                   self.basket_2[self.now_shop][-1][0][1],
                                                   int(self.basket_price)+int(self.deliv))
        label_texts = [time_stamp, self.now_shop, details]
        new_order = self.create_custom_frame(self.frame_no, 400, 180,
                                             self.btn_start_no, self.btn_end_no,
                                             label_texts, self.label_start_no, self.label_end_no, 1, 2, details_text)
        self.new_orders[self.detail_btn_no] = new_order
        self.history_layout.addWidget(new_order)
        self.frame_no += 1
        self.btn_start_no += 3
        self.btn_end_no += 3
        self.label_start_no += 3
        self.label_end_no += 3

    def creat_blank_frame(self, start_num, end_num, minW, minH):
        frames = []
        for i in range(start_num, end_num + 1):
            globals()['empty_frame_{}'.format(i)] = QFrame()
            frames.append(globals()['empty_frame_{}'.format(i)])
        for i in range(len(frames)):
            frames[i].setMinimumSize(minW, minH)
        return frames

    def create_btn(self, start_num, end_num, minW, minH, maxW, maxH):
        btns = []
        for i in range(start_num, end_num+1):
            globals()['btn_history_{}'.format(i)] = QPushButton()
            btns.append(globals()['btn_history_{}'.format(i)])
        for i in range(len(btns)):
            btns[i].setMinimumSize(minW, minH)
            btns[i].setMaximumSize(maxW, maxH)
        return btns

    def create_label(self, texts, start_num, end_num, minW, minH, maxW, maxH, align='left'):
        if align == 'left':
            align = Qt.AlignLeft
        elif align == 'right':
            align = Qt.AlignRight
        else:
            align = Qt.AlignCenter
        labels = []
        count = 0
        for i in range(start_num, end_num+1):
            globals()['label_history_{}'.format(i)] = QLabel(texts[count])
            labels.append(globals()['label_history_{}'.format(i)])
            count += 1
        for i in range(len(labels)):
            labels[i].setMinimumSize(minW, minH)
            labels[i].setMaximumSize(maxW, maxH)
            if i == 0:
                labels[i].setAlignment(Qt.AlignRight)
            else:
                labels[i].setAlignment(align)
        return labels

    def create_custom_frame(self, frame_no, width, height, btn_start_no, btn_end_no,
                            texts, label_start_no, label_end_no, f_start_no, f_end_no, details_text):
        btn_list1 = self.create_btn(btn_start_no, btn_start_no, 0, 0, 100, 100)
        btn_list2 = self.create_btn(btn_start_no+1, btn_end_no, 0, 40, 400, 100)

        label_list = self.create_label(texts, label_start_no, label_end_no, 0, 0, 400, 25)
        frame_list1 = self.creat_blank_frame(f_start_no, f_start_no, 0, 0)
        frame_list2 = self.creat_blank_frame(f_start_no+1, f_end_no, 0, 0)

        btn_list1[0].setStyleSheet("QPushButton{"
                                   "border: none;"
                                   "image: url(:/icon_image/images/bike-001.png);"
                                   "background-color: rgb(255,255,255);"
                                   "}")
        btn_list2[0].setStyleSheet("QPushButton{"
                                   "border: none;"
                                   "image: url(:/icon_image/images/progress_bar-001.png);"
                                   "background-color: rgb(255,255,255);"
                                   "}")
        btn_list2[1].setStyleSheet("QPushButton{"
                                   "border: none;"
                                   "image: url(:/icon_image/images/order_detail-001.png);"
                                   "background-color: rgb(255,255,255);"
                                   "}"
                                   "QPushButton:hover{"
                                   "image: url(:/icon_image/images/order_detail-001 (1).png);"
                                   "background-color: rgb(255,255,255);"
                                   "}")

        btn_list2[1].clicked.connect(lambda: self.show_history_details(texts, details_text))

        label_list[0].setFont(QtGui.QFont("나눔스퀘어_ac Light", 8))
        label_list[1].setFont(QtGui.QFont("나눔스퀘어_ac", 13, QtGui.QFont.Bold))
        label_list[2].setFont(QtGui.QFont("나눔스퀘어_ac", 9))

        grid = QGridLayout()
        grid.setContentsMargins(0,0,0,0)
        grid.setSpacing(0)

        grid.addWidget(btn_list1[0], 0, 0, 3, 3)
        grid.addWidget(label_list[0], 0, 3, 1, 4)
        grid.addWidget(label_list[1], 1, 3, 1, 4)
        grid.addWidget(label_list[2], 2, 3, 1, 4)
        grid.addWidget(frame_list1[0], 0, 7, 3, 1)
        grid.addWidget(btn_list2[0], 3, 0, 1, 8)
        grid.addWidget(btn_list2[1], 4,0,1,8)
        grid.addWidget(frame_list2[0], 5,0,1,8)

        frames = []
        globals()['frame_{}'.format(frame_no)] = QFrame(self)
        frames.append(globals()['frame_{}'.format(frame_no)])
        frames[0].resize(width, height)
        frames[0].setMinimumSize(width, height)
        frames[0].setMaximumSize(width, height)
        frames[0].setLayout(grid)
        frames[0].setContentsMargins(0,8,0,0)
        frames[0].setStyleSheet("QFrame{background-color: rgb(255,255,255); border: none;}")
        return frames[0]

    def show_history_details(self, texts, details_text):
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget_9.setCurrentIndex(1)
        self.details(texts, details_text)

    def details(self, texts, details_text):
        self.msg_details = QMessageBox()
        self.msg_details.setWindowTitle("{} 주문상세내역".format(texts[1]))
        btn_reply = self.msg_details.setStandardButtons(QMessageBox.Ok)
        self.msg_details.resize(300, 300)

        self.msg_details.setText("{}\n{}\n{}".format(texts[0], texts[-1], details_text))
        self.msg_details.show()
        if btn_reply == QMessageBox.Ok:
            self.stackedWidget.setCurrentIndex(7)
            self.msg_details.close()

    # 전화번호 리스트위젯 번호띄어주기
    def call4(self):
        self.msg1 = QMessageBox()
        self.msg1.setWindowTitle("한식집 전화번호")
        self.msg1.setStandardButtons(QMessageBox.Ok)
        self.msg1.setText("""
우람한국밥:02-720-2748
뽀식이네감자탕:02-736-0828""")
        self.msg1.show()
    def call6(self):
        self.msg2 = QMessageBox()
        self.msg2.setWindowTitle("일식집 전화번호")
        self.msg2.setStandardButtons(QMessageBox.Ok)
        self.msg2.setText("""
성환미쯔야: 02-275-1475
선스시오: 02-920-8576""")
        self.msg2.show()
    def call3(self):
        self.msg3 = QMessageBox()
        self.msg3.setWindowTitle("중국집 전화번호")
        self.msg3.setStandardButtons(QMessageBox.Ok)
        self.msg3.setText("""
애기선훈반점: 02-355-1197
동국반점: 02-804-4902""")
        self.msg3.show()
    def call1(self):
        self.msg4 = QMessageBox()
        self.msg4.setWindowTitle("분식집 전화번호")
        self.msg4.setStandardButtons(QMessageBox.Ok)
        self.msg4.setText("""
이루오드리오분식: 02-976-3753
광인분식: 02-376-4975""")
        self.msg4.show()
    def call2(self):
        self.msg5 = QMessageBox()
        self.msg5.setWindowTitle("Chicken 전화번호")
        self.msg5.setStandardButtons(QMessageBox.Ok)
        self.msg5.setText("""
상준이 반마리치킨: 02-736-0828
bybyQ치킨: 02-250-2694""")
        self.msg5.show()
    def call7(self):
        self.msg6 = QMessageBox()
        self.msg6.setWindowTitle("Pizza 전화번호")
        self.msg6.setStandardButtons(QMessageBox.Ok)
        self.msg6.setText("""
영완피자: 02-837-3319
돌리노피자: 02-250-2694""")
        self.msg6.show()
    def call5(self):
        self.msg7 = QMessageBox()
        self.msg7.setWindowTitle("Burger 전화번호")
        self.msg7.setStandardButtons(QMessageBox.Ok)
        self.msg7.setText("""
상동버거: 02-720-2748
맥두리아: 02-537-8828""")
        self.msg7.show()

    def like_msg(self):
        self.msg8 = QMessageBox()
        self.msg8.setWindowTitle("Check msg")
        self.msg8.setStandardButtons(QMessageBox.Ok)
        self.msg8.setText("""
"'찜' 리스트에 추가되셨어요!"
 """)
        self.msg8.show()

    def search_msg_box(self):
        self.msg9 = QMessageBox()
        self.msg9.setWindowTitle("Check msg")
        self.msg9.setStandardButtons(QMessageBox.Ok)
        self.msg9.setText("""
해당메뉴가 없습니다!!
    """)
        self.msg9.show()

    def search_msg_box2(self):
        self.msg10 = QMessageBox()
        self.msg10.setWindowTitle("Check msg")
        self.msg10.setStandardButtons(QMessageBox.Ok)
        self.msg10.setText("""
검색어를 입력해주세요!!
    """)
        self.msg10.show()
 # 전화번호 리스트위젯 번호띄어주기
    def bbosik_num(self):
        self.msg_1 = QMessageBox()
        self.msg_1.setWindowTitle("뽀식이네 전화번호")
        self.msg_1.setStandardButtons(QMessageBox.Ok)
        self.msg_1.setText("""
뽀식이네감자탕:02-736-0828""")
        self.msg_1.show()

    def wooram_num(self):
        self.msg_2 = QMessageBox()
        self.msg_2.setWindowTitle("우람이네 전화번호")
        self.msg_2.setStandardButtons(QMessageBox.Ok)
        self.msg_2.setText("""
우람한국밥:02-720-2748""")

        self.msg_2.show()

    def ksh_num(self):
        self.msg_3 = QMessageBox()
        self.msg_3.setWindowTitle("성환이네 전화번호")
        self.msg_3.setStandardButtons(QMessageBox.Ok)
        self.msg_3.setText("""
성환미쯔야: 02-275-1475""")
        self.msg_3.show()

    def sun_num(self):
        self.msg_4 = QMessageBox()
        self.msg_4.setWindowTitle("선스시오 전화번호")
        self.msg_4.setStandardButtons(QMessageBox.Ok)
        self.msg_4.setText("""
선스시오: 02-920-8576""")
        self.msg_4.show()

    def by_sh_num(self):
        self.msg_5 = QMessageBox()
        self.msg_5.setWindowTitle("애기선훈이네 전화번호")
        self.msg_5.setStandardButtons(QMessageBox.Ok)
        self.msg_5.setText("""
애기선훈반점: 02-355-1197""")
        self.msg_5.show()

    def dong_num(self):
        self.msg_6 = QMessageBox()
        self.msg_6.setWindowTitle("동국이네 전화번호")
        self.msg_6.setStandardButtons(QMessageBox.Ok)
        self.msg_6.setText("""
동국반점: 02-804-4902""")
        self.msg_6.show()

    def luo_num(self):
        self.msg_7 = QMessageBox()
        self.msg_7.setWindowTitle("'루오' 전화번호")
        self.msg_7.setStandardButtons(QMessageBox.Ok)
        self.msg_7.setText("""
이루오드리오분식: 02-976-3753""")
        self.msg_7.show()

    def kwang_num(self):
        self.msg_8 = QMessageBox()
        self.msg_8.setWindowTitle("광인이네 전화번호")
        self.msg_8.setStandardButtons(QMessageBox.Ok)
        self.msg_8.setText("""
광인분식: 02-376-4975""")
        self.msg_8.show()

    def jun_num(self):
        self.msg_9 = QMessageBox()
        self.msg_9.setWindowTitle("'상준' 전화번호")
        self.msg_9.setStandardButtons(QMessageBox.Ok)
        self.msg_9.setText("""
상준이 반마리치킨: 02-736-0828""")
        self.msg_9.show()

    def byq_num(self):
        self.msg_10 = QMessageBox()
        self.msg_10.setWindowTitle("byq 전화번호")
        self.msg_10.setStandardButtons(QMessageBox.Ok)
        self.msg_10.setText("""
bybyQ치킨: 02-250-2694""")
        self.msg_10.show()

    def yw_num(self):
        self.msg_11 = QMessageBox()
        self.msg_11.setWindowTitle("'영완' 전화번호")
        self.msg_11.setStandardButtons(QMessageBox.Ok)
        self.msg_11.setText("""
영완피자: 02-837-3319""")
        self.msg_11.show()

    def dol_num(self):
        self.msg_12 = QMessageBox()
        self.msg_12.setWindowTitle("돌리노피자 전화번호")
        self.msg_12.setStandardButtons(QMessageBox.Ok)
        self.msg_12.setText("""
돌리노피자: 02-250-2694""")
        self.msg_12.show()

    def sang_num(self):
        self.msg_13 = QMessageBox()
        self.msg_13.setWindowTitle("상동버거 전화번호")
        self.msg_13.setStandardButtons(QMessageBox.Ok)
        self.msg_13.setText("""
상동버거: 02-720-2748""")
        self.msg_13.show()

    def mac_num(self):
        self.msg_14 = QMessageBox()
        self.msg_14.setWindowTitle("맥두리아 전화번호")
        self.msg_14.setStandardButtons(QMessageBox.Ok)
        self.msg_14.setText("""
맥두리아: 02-537-8828""")
        self.msg_14.show()


    def keyPressEvent(self, e):
       if e.key()==16777220:
            if len(self.user_searchbar.text())>=1:
                self.search_dish()
                self.search_store_button()
                self.pay_atonce_button()
            elif len(self.pw_main_2.text())>=1:
                self.custapp()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = CustApp()
    form.show()
    exit(app.exec_())