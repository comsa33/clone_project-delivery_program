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
import datetime
import time
from time import gmtime
import ast                                              #문자열을 리스트로 바꾸기 위해 썼던 모듈입니다
import random                                           #주문시간 추가를 위한 랜덤모듈입니다
from find_pwB import *
from signupB import *


form_class = uic.loadUiType("business.1.6.ui")[0]

class BusinessApp(QMainWindow, form_class):

    # 고객으로부터 들어온 주문내용(나중에 아래 코드에서 피클로 로드함)
    current_business_orders = dict()
    # 업체가 기존에 수락했던 주문건들
    current_business_accepted_orders = {}

    import BM_business_rc
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

        # 좌측 상단 날짜를 오늘 날짜로 표시
        self.label_title_date.setText(date.today().isoformat())
        # 프로그램 구동되면 첫 화면: 로그인화면 설정
        self.stackedWidget.setCurrentIndex(0)

        ## 사이드버튼 스택위젯 연결
        self.go_sw(0)
        self.go_sw(1)
        self.go_sw(2)
        self.go_sw(3)
        self.go_sw(4)

        ## 로그인 관련
        self.Login_info = Login_info()
        self.business_info = self.Login_info.login
        self.pw_search = Pw_search()
        self.login_status = False

        self.choicelogin_button_2.clicked.connect(self.Login_info.show)  # 회원가입
        self.main_pw_search_btn_2.clicked.connect(self.pw_search.show)  # 비밀번호 찾기
        self.login_button.clicked.connect(self.businessapp)  # 로그인화면

        ### 좌측하단 로그인/로그아웃/회원가입 버튼 연결
        self.btn_login.clicked.connect(self.login_)
        self.btn_logout.clicked.connect(self.logout_)
        self.btn_signup.clicked.connect(self.signup_)

        ## 주문관련
        # 새로 들어온 주문의 항목을 더블클릭하면 발생하는 함수연결
        self.new_order_listwidget.itemDoubleClicked.connect(self.new_order_click)
        self.btn_new_order.clicked.connect(self.check_new_order) ## 새로운 주문건들을 확인하면 버튼의 빨간색 사라짐
        self.accepted = False   ## 주문수락하면 활성화되는 스위치
        self.last_row = 0 ## 주문 현황 리스트 마지막 줄을 반환하는 변수

        # 주문현황창
        self.tableWidget.cellDoubleClicked.connect(self.check_dish_done)

        # 배달현황창
        self.shipping_items = []        ## 배달리스트 (피클에 저장할)
        self.delivered_status = False
        self.company_btn.clicked.connect(lambda: self.assign_delivery(1))
        self.employee_btn.clicked.connect(lambda: self.assign_delivery(2))

        # 일매출현황/
        self.last_row_d = 0
        ### 일매출 (수락된 주문건) 저장 변수
        self.daily_sales_data = [[],[]]
        # self.btn_daily_sales.clicked.connect(lambda: self.load_daily_sales(self.daily_sales_data))

    # 모니터 중앙에 어플배치
    def initUI(self):
        self.setWindowTitle('B달의 민족_업체 POS')
        self.resize(1103, 674)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 사이드 버튼 클릭시 해당 위젯으로 이동 함수
    def go_sw(self, index):
        self.sidebtns = [self.btn_new_order, self.btn_order_status, self.btn_delivery_status,
                     self.btn_daily_sales, self.btn_monthly_sales]
        self.sidebtns[index].clicked.connect(lambda: self.show_sw(index+1))

    def show_sw(self, index):
        return self.stackedWidget.setCurrentIndex(index)

    # 로그인 눌렀을시 함수
    def businessapp(self):
        self.current_b = self.id_main_2.text()
        with open('배민회사측.pickle','rb') as r:
            self.z=pickle.load(r)

        if self.id_main_2.text() in self.z.keys():
            if self.pw_main_2.text() == self.z[self.id_main_2.text()][0]:
                # 로그인 성공시
                self.current_id = self.id_main_2.text()
                print(self.current_id)

                ### 고객용 주문 자료 피클 불러오기
                try:
                    with open("{}_orders.pickle".format(self.current_id), 'rb')as r:
                        self.current_business_orders = pickle.load(r)
                        print("1", self.current_business_orders)
                except FileNotFoundError:
                    pass

                ### 업체 배송리스트 자료 피클 불러오기
                try:
                    with open("{}_shipping_show.pickle".format(self.current_id), 'rb')as r:
                        self.shipping_items = pickle.load(r)
                        print("shipping_show 로드")
                except FileNotFoundError:
                    pass
                ### 배송 기존 데이터를 배송 리스트에 띄워주기 함수
                self.load_shipping_show_data(self.shipping_items)

                ### 기존 일매출 정보 피클로드
                try:
                    with open("{}_daily_sales.pickle".format(self.current_id), 'rb')as r:
                        self.daily_sales_data = pickle.load(r)
                        print("loaded_daily_sales: ", self.daily_sales_data)
                except FileNotFoundError:
                    pass
                ### 일매출 기존 정보 일매출테이블에 띄워주기 함수
                self.load_daily_sales(self.daily_sales_data)

                self.title_business_name.setText(self.current_id)
                self.label_3.setText(self.title_business_name.text())
                self.stackedWidget.setCurrentIndex(1)  ## 홈화면가기
                self.login_status = True
                self.now_order()
            else:
                self.statusbar_2.setText("비번이 맞지않습니다.")
        else:
            self.statusbar_2.setText("입력하신 ID로 가입된 정보가 없습니다.")

    # 좌측하단 로그인 클릭시; 로그아웃상태에서만 로그인 버튼 활성화
    def login_(self):
        if not self.login_status:
            self.stackedWidget.setCurrentIndex(0)
        else:
            pass

    def logout_(self):
        if self.login_status:
            self.stackedWidget.setCurrentIndex(0)
            self.id_main_2.clear()
            self.pw_main_2.clear()
            self.statusbar_2.setText("로그아웃 되었습니다.")
            self.login_status = False
        else:
            pass

    def signup_(self):
        if not self.login_status:
            self.Login_info.show()
        else:
            pass

    ## 새로운 주문수락 관련 함수들
    def now_order(self):
        if self.login_status:
            try:
                with open("{}_accepted_orders.pickle".format(self.current_id), 'rb')as r:
                    self.current_business_accepted_orders = pickle.load(r)
                    print("2", self.current_business_accepted_orders)
            except FileNotFoundError:
                pass

            ### 기존 주문 수락했던 리스트를 주문현황에 띄우기 함수
            orders_accepted_total = list(zip(self.current_business_accepted_orders.keys(),
                                             self.current_business_accepted_orders.values()))
            self.addExisting_tableWidget(orders_accepted_total)

            new_order_keys = list(set(self.current_business_orders.keys()) - set(self.current_business_accepted_orders.keys()))
            print(new_order_keys)
            self.new_orders = []
            for new_order_key in new_order_keys:
                self.new_orders.append([new_order_key, self.current_business_orders[new_order_key]])
            print("new", self.new_orders)

            if self.new_orders:
                for i in range(len(self.new_orders)):
                    time_stamp = self.new_orders[i][0]
                    order = self.new_orders[i][1]
                    self.new_order_listwidget.addItem("{} \t {}".format(str(time_stamp), str(order)))

                # 새로운 주문목록이 있으면 버튼 색깔이 바뀜 // [이루오] 수정
                self.btn_new_order.setStyleSheet(
                                                 "QPushButton{"                         
                                                 "border-right: 8px solid;"
                                                 "border-right-color: rgb(185, 60, 41);"
                                                 "}"
                                                 "QPushButton:hover{"
                                                 "border-right: 8px solid;"
                                                 "border-right-color: rgba(185, 60, 41, 100);"
                                                 "}"
                                                 )
            else:
                pass
        else:
            self.stackedWidget.setCurrentIndex(0)
            self.statusbar_2.setText("프로그램을 이용하시려면 로그인을 먼저 해주세요.")

    # 주문을 확인하면 버튼색깔이 다시 바뀜
    def check_new_order(self):
        self.btn_new_order.setStyleSheet("QPushButton{"
                                         "background-color: rgb(222, 255, 243);"
                                         "}"
                                         "QPushButton:hover{"
                                         "background-color: rgb(167, 255, 226);"
                                         "}")

    def new_order_click(self):
        self.new_order_item = self.new_order_listwidget.currentRow()
        return self.clicked(self.new_order_item)

    def clicked(self, current_index):
        self.system_msg1 = QMessageBox()
        self.system_msg1.setWindowTitle("system")
        self.system_msg1.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        self.system_msg1.setText("주문을 수락하시겠습니까?")
        self.system_msg1.show()
        retval = self.system_msg1.exec_()
        if retval == QMessageBox.Yes:
            self.accepted = True
            self.selected_key = self.new_order_listwidget.currentItem().text()[:17]
            self.current_business_accepted_orders[self.selected_key] = self.current_business_orders[self.selected_key]
            self.current_business_accepted_orders[self.selected_key][1].append("주문수락")
            ## 리스트위젯 항목을 하나하나 지우기
            self.new_order_listwidget.takeItem(current_index)
            ## 주문현황 리스트로 보내기 함수
            self.add_order_list(self.accepted)

        elif retval == QMessageBox.No:
            self.accepted = False
            self.selected_key = self.new_order_listwidget.currentItem().text()[:17]
            self.current_business_accepted_orders[self.selected_key] = self.current_business_orders[self.selected_key]
            self.current_business_accepted_orders[self.selected_key][1].append("주문거절")
            self.new_order_listwidget.takeItem(current_index)
            ## 주문현황 리스트로 보내기 함수
            self.add_order_list(self.accepted)
        else:
            pass
        print("current_business_accepted_orders: ", self.current_business_accepted_orders)

    ### new_orders 형태
    ### ('21-05-10 12:40:18', [[['팔보채', 1, '18000'], ['짬뽕', 1, '5500']], ['이루오', '광주 발산로 36 102-1202']])
    ## 주문 현황 보여주기 관련 함수
    def add_order_list(self, accepted = True):
        if accepted:
            accepted = "조리중"
            self.addNewItem_tableWidget(cooking_time=str(self.cal_cooking_time()), accepted=accepted)
            ### 일매출 더해주는 함수 추가 (공사중) ###
            self.add_daily_sales()
            self.accepted = False
        elif not accepted:
            accepted = "주문거절"
            self.addNewItem_tableWidget(cooking_time=" - ", accepted=accepted)

    def addNewItem_tableWidget(self, cooking_time, accepted):
        row = self.tableWidget.rowCount()
        new_order = self.current_business_accepted_orders[self.selected_key]
        self.tableWidget.setRowCount(row + len(new_order[0]))
        for i in range(len(new_order[0])):  # 음식 갯수만큼 반복
            self.tableWidget.setItem(self.last_row + i, 0, QTableWidgetItem(str(self.selected_key)))
            self.tableWidget.setItem(self.last_row + i, 1, QTableWidgetItem(str(new_order[0][i][0])))
            self.tableWidget.setItem(self.last_row + i, 2, QTableWidgetItem(str(new_order[0][i][1])))
            self.tableWidget.setItem(self.last_row + i, 3, QTableWidgetItem(str(new_order[0][i][2])))
            self.tableWidget.setItem(self.last_row + i, 4, QTableWidgetItem(str(cooking_time)))  # 조리시간
            self.tableWidget.setItem(self.last_row + i, 5, QTableWidgetItem(str(new_order[1][0])))
            self.tableWidget.setItem(self.last_row + i, 6, QTableWidgetItem(str(new_order[1][1])))
            self.tableWidget.setItem(self.last_row + i, 7, QTableWidgetItem(str(accepted)))  # 주문상태
        self.last_row += len(new_order[0])
        with open("{}_accepted_orders.pickle".format(self.current_id), 'wb')as f:
            pickle.dump(self.current_business_accepted_orders, f)

    ### [('21-05-10 15:43:25', [[['팔보채', 2, '36000'], ['짜장면', 1, '4000']], ['김성환', '광주 북구 중흥동']])]
    def addExisting_tableWidget(self, accepted_orders):
        for i in range(len(accepted_orders)):
            row = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(row + len(accepted_orders[i][1][0]))
            for j in range(len(accepted_orders[i][1][0])):
                self.tableWidget.setItem(self.last_row + j, 0, QTableWidgetItem(str(accepted_orders[i][0][-8:])))
                self.tableWidget.setItem(self.last_row + j, 1, QTableWidgetItem(str(accepted_orders[i][1][0][j][0])))
                self.tableWidget.setItem(self.last_row + j, 2, QTableWidgetItem(str(accepted_orders[i][1][0][j][1])))
                self.tableWidget.setItem(self.last_row + j, 3, QTableWidgetItem(str(accepted_orders[i][1][0][j][2])))
                self.tableWidget.setItem(self.last_row + j, 4, QTableWidgetItem(str("조리완료")))  # 조리시간
                self.tableWidget.setItem(self.last_row + j, 5, QTableWidgetItem(str(accepted_orders[i][1][1][0])))
                self.tableWidget.setItem(self.last_row + j, 6, QTableWidgetItem(str(accepted_orders[i][1][1][1])))
                self.tableWidget.setItem(self.last_row + j, 7, QTableWidgetItem(str(accepted_orders[i][1][1][2])))  # 주문상태
            self.last_row += len(accepted_orders[i][1][0])

    def cal_cooking_time(self):
        cooking_time = random.randint(15, 30)
        return cooking_time

    ## 주문현황에서 항목을 더블클릭하면 발생하는 함수
    def check_dish_done(self):
        print("done")
        selected_row = self.tableWidget.currentRow()
        self.tableWidget.setCurrentCell(selected_row, 0)
        selected_key = self.tableWidget.currentItem().text()
        for key in list(self.current_business_accepted_orders.keys()):
            if selected_key in key:
                selected_key = key
        print(self.current_business_accepted_orders[selected_key])
        self.add_to_delivery(self.current_business_accepted_orders[selected_key], selected_row)
        self.delivered_done_modify_data(selected_key=selected_key)

    def add_to_delivery(self, done_dish, current_row):
        selected_row = self.tableWidget.currentRow()
        self.tableWidget.setCurrentCell(selected_row, 7)
        selected_status = self.tableWidget.currentItem().text()
        if selected_status not in ["배송중", "배송완료", "주문거절"]:
            self.shipping_show.addItem(str(done_dish))
            self.tableWidget.setItem(current_row, 4, QTableWidgetItem("조리완료"))
            self.tableWidget.setItem(current_row, 7, QTableWidgetItem("배송중"))
            print(self.current_business_accepted_orders)

            ### 주문배달 상태 ON
            self.delivered_status = True
        else:
            pass

    def delivered_done_modify_data(self, selected_key):
        self.current_business_accepted_orders[selected_key][1][-1] = "배송완료"
        with open("{}_accepted_orders.pickle".format(self.current_id), 'wb')as f:
            pickle.dump(self.current_business_accepted_orders, f)

    # 배달대행 버튼 클릭시 배정된 배달료를 업체 데이터에 추가
    def match_delivery_fee(self, value, delivery_fee):
        print(value[:-10])
        print(self.current_business_accepted_orders)
        for new in self.new_orders:
            if value[:-10] in str(new):
                key_found = new[0]
                print(key_found)
                self.current_business_accepted_orders[key_found][1].append(delivery_fee[0])
                print("123", self.current_business_accepted_orders)

    def assign_delivery(self, messenger=1):
        delivered_status = self.delivered_status
        try:
            if delivered_status:
                row = self.shipping_show.currentRow()
                existing_item = self.shipping_show.currentItem().text()
                if messenger == 1:
                    delivery_fee_list = [1000, 1500, 2000, 2500, 3000, 3500]
                    delivery_staff = ["이선훈", "정상준", "이영완", "김성환", "이루오"]
                    self.delivery_fee = random.sample(delivery_fee_list, 1)
                    self.delivery_staff = random.sample(delivery_staff, 1)
                    print(existing_item)
                    self.match_delivery_fee(existing_item, self.delivery_fee)
                    listItem = QListWidgetItem(existing_item + " / [업체배달, 배달수임료: {}원, 배달직원: {}]".format(self.delivery_fee, self.delivery_staff))
                    self.shipping_show.takeItem(row)
                    self.shipping_show.addItem(listItem)
                elif messenger == 2:
                    print(existing_item)
                    self.delivery_fee = [0]
                    self.match_delivery_fee(existing_item, self.delivery_fee)
                    listItem = QListWidgetItem(existing_item + " // [가게배달]")
                    self.shipping_show.takeItem(row)
                    self.shipping_show.addItem(listItem)
                self.delivered_status = False
            else:
                pass
        except AttributeError:
            pass

    def save_shipping_show_data(self):
        for index in range(self.shipping_show.count()):
            self.shipping_items.append(self.shipping_show.item(index).text())
            print("shipping_items: ", self.shipping_items)

        with open("{}_shipping_show.pickle".format(self.current_id), 'wb')as f:
            pickle.dump(self.shipping_items, f)
        print(self.shipping_items)

    def load_shipping_show_data(self, list):
        for item in list:
            listItem = QListWidgetItem(item)
            self.shipping_show.addItem(listItem)

    ## 일매출 관련 함수
    def add_daily_sales(self):
        daily_sales_dates = self.daily_sales_data[0]
        daily_sales_values = self.daily_sales_data[1]
        row = self.daily_table.rowCount()
        new_order = self.current_business_accepted_orders[self.selected_key]
        daily_sales_dates.append(self.selected_key)
        daily_sales_values.append(new_order)
        self.daily_table.setRowCount(row + len(new_order[0]))
        for i in range(len(new_order[0])):  # 음식 갯수만큼 반복
            self.daily_table.setItem(self.last_row_d + i, 0, QTableWidgetItem(str(self.selected_key)))
            self.daily_table.setItem(self.last_row_d + i, 1, QTableWidgetItem(str(new_order[0][i][0])))
            self.daily_table.setItem(self.last_row_d + i, 2, QTableWidgetItem(str(new_order[0][i][1])))
            self.daily_table.setItem(self.last_row_d + i, 3, QTableWidgetItem(str(new_order[0][i][2])))
            self.daily_table.setItem(self.last_row_d + i, 4, QTableWidgetItem(str(new_order[1][0])))
            self.daily_table.setItem(self.last_row_d + i, 5, QTableWidgetItem(str(new_order[1][1])))
            self.daily_table.setItem(self.last_row_d + i, 6, QTableWidgetItem(str("미정")))    #배달료
            self.daily_table.setItem(self.last_row_d + i, 7, QTableWidgetItem(str(new_order[1][2])))
        self.last_row_d += len(new_order[0])
        self.daily_sales_data = [daily_sales_dates, daily_sales_values]
        with open("{}_daily_sales.pickle".format(self.current_id), 'wb')as f:
            pickle.dump(self.daily_sales_data, f)
        print("daily_sales", self.daily_sales_data)

    def load_daily_sales(self, daily_sales_data):
        daily_sales_dates = daily_sales_data[0]
        daily_sales_values = daily_sales_data[1]
        for i in range(len(daily_sales_values)):
            row = self.daily_table.rowCount()
            self.daily_table.setRowCount(row + len(daily_sales_values[i][1][0]))
            for j in range(len(daily_sales_values[i][0])):
                self.daily_table.setItem(self.last_row_d + j, 0, QTableWidgetItem(str(daily_sales_dates[i])))
                self.daily_table.setItem(self.last_row_d + j, 1, QTableWidgetItem(str(daily_sales_values[i][0][j][0])))
                self.daily_table.setItem(self.last_row_d + j, 2, QTableWidgetItem(str(daily_sales_values[i][0][j][1])))
                self.daily_table.setItem(self.last_row_d + j, 3, QTableWidgetItem(str(daily_sales_values[i][0][j][2])))
                self.daily_table.setItem(self.last_row_d + j, 4, QTableWidgetItem(str(daily_sales_values[i][1][0])))
                self.daily_table.setItem(self.last_row_d + j, 5, QTableWidgetItem(str(daily_sales_values[i][1][1])))
                self.daily_table.setItem(self.last_row_d + j, 6, QTableWidgetItem(str(daily_sales_values[i][1][3])))    #배달료
                self.daily_table.setItem(self.last_row_d + j, 7, QTableWidgetItem(str(daily_sales_values[i][1][2])))
            self.last_row_d += len(daily_sales_values[i][0])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = BusinessApp()
    form.show()
    if app.exec_() == 0:
        form.save_shipping_show_data()