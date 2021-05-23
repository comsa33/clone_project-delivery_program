from PyQt5 import uic
from PyQt5.QtWidgets import *
import sys, pickle
import threading
from datetime import date
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui
from PyQt5 import uic


login_info_sub= uic.loadUiType("info.ui")[0]

class Login_info(QMainWindow, login_info_sub): # 회원가입 창

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.initUI()

        # 회원가입하면 신규회원의 정보를 딕셔너리에 저장
        # {key:value} = {id:[password_info, name_info, address_info, ph_num_info]}
        self.login = {}

        self.info_button.clicked.connect(self.loginfo) # 회원가입 버튼
        self.info_button_2.clicked.connect(self.check) # 중복확인

        try:
            with open("log_b.pickle",'rb')as r:
                self.login=pickle.load(r)
        except FileNotFoundError:
            pass

    def initUI(self):
        self.setWindowTitle('B달의 민족_업체 POS_회원가입')
        self.resize(372, 250)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def check(self):                              #중복확인 함수
        if self.id_info.text() in self.login.keys():
            self.statusBar().showMessage("다른 아이디를 사용해주세요")
        else:
            self.statusBar().showMessage("사용가능한 아이디 입니다.")

    # 메세지박스 띄우고
    # 입력된 정보를 login 딕셔너리에 저장
    def loginfo(self):
        msg="회원가입을 하시겠습니까?"
        buttonReply = QMessageBox.question(self, '회원가입', msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if buttonReply == QMessageBox.Yes:
            QMessageBox.about(self, "저장", "입력하신 정보로 저장되었습니다.")
            self.statusBar().showMessage("저장되었습니다.")

            # id 키값 / 나머지 value
            self.login[self.id_info.text()] = [self.password_info.text(), self.name_info.text(),
                                               self.address_info.text(), self.ph_num_info.text()]

            with open("log_b.pickle", 'wb')as f:
                pickle.dump(self.login, f)

        elif buttonReply == QMessageBox.No:
            pass

        print(self.login)
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = Login_info()
    login.show()
    app.exec_()