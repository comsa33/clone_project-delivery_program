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
from signupB import *

pw_search= uic.loadUiType("pw_search.ui")[0]

class Pw_search(QMainWindow, pw_search):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.initUI()

        self.pw_search_btn.clicked.connect(self.search)  # 중복확인
        self.Login_info = Login_info()

    def initUI(self):
        self.setWindowTitle('B달의 민족_업체 POS_비번찾기')
        self.resize(264, 152)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def search(self):
        try:
            if self.pw_search_id_QLine.text() in self.Login_info.login.keys():
                if self.pw_search_name_QLine.text() in self.Login_info.login[self.pw_search_id_QLine.text()][1]:
                    self.statusBar().showMessage("{}님의 비밀번호 : ".format(self.Login_info.login[self.pw_search_id_QLine.text()][1])+self.Login_info.login[self.pw_search_id_QLine.text()][0])
                else:
                    self.statusBar().showMessage("ID와 이름이 매칭이 되지 않습니다.")
            else:
                self.statusBar().showMessage("입력하신 정보로 가입된 ID가 없습니다.")
        except TypeError:
            self.statusBar().showMessage("이름과 비밀번호가 정확히 입력되었는지 확인해주세요.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = Pw_search()
    login.show()
    exit(app.exec_())