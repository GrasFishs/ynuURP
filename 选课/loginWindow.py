from PyQt5.QtWidgets import QApplication,QDialog,QPushButton,QMessageBox,QLineEdit,QVBoxLayout,QHBoxLayout,QLabel,QWidget
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import pyqtSignal
from ynuer import Ynu
from tabDialog import TabDialog

class LoginWindow(QDialog):

    close_signal = pyqtSignal()
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.ynu = Ynu()
        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowTitle("登录URP")
        self.setFixedSize(300,200)

        #用户名
        self.u = QLabel("学  号")
        self.userName = QLineEdit(self)
        self.userName.setPlaceholderText("学号")

        #密码
        self.p = QLabel("密  码")
        self.passWord = QLineEdit(self)
        self.passWord.setEchoMode(QLineEdit.Password)
        self.passWord.setPlaceholderText("密码")

        #验证码
        self.v = QLabel("验证码")
        self.code = QLineEdit(self)
        self.code.setPlaceholderText("验证码(不区分大小写)")

        #登录，退出按钮
        self.loginBtn = QPushButton("登录",self)
        self.loginBtn.setMaximumWidth(50)
        self.cancelBtn = QPushButton("取消",self)
        self.cancelBtn.setMaximumWidth(50)

        self.loginBtn.clicked.connect(self.login)
        self.cancelBtn.clicked.connect(self.reject)

        #验证码
        self.png = QLabel()
        self.downloadPic(self.png)

        #用户名布局
        ulayout = QHBoxLayout()
        ulayout.addWidget(self.u)
        ulayout.addWidget(self.userName)

        #密码布局
        playout = QHBoxLayout()
        playout.addWidget(self.p)
        playout.addWidget(self.passWord)

        #验证码布局
        vlayout = QHBoxLayout()
        vlayout.addWidget(self.v)
        vlayout.addWidget(self.code)

        #底部布局
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.png)
        bottomLayout.addWidget(self.loginBtn)
        bottomLayout.addWidget(self.cancelBtn)

        #全局布局
        layout = QVBoxLayout()
        layout.addLayout(ulayout)
        layout.addLayout(playout)
        layout.addLayout(vlayout)
        layout.addLayout(bottomLayout)
        self.setLayout(layout)


    def closeEvent(self, QCloseEvent):
        self.close_signal.emit()
        self.close()

    def downloadPic(self, pic):
        self.ynu.downloadCode()
        pic.setPixmap(QPixmap("验证码.png"))

    def login(self):
        un = self.userName.text()
        pw = self.passWord.text()
        v = self.code.text()
        self.ynu.singIn(un, pw, v)
        if self.ynu.clickSign():
            print("登录成功")
            tab.setInfos(self.ynu.getInfo())
            tab.pushInfos()
            tab.show()
            self.close()
            return True
        else:
            warnning = QMessageBox.warning(self, "警告！", "账号或密码或验证码不对!", QMessageBox.Yes)
            self.code.setText("")
            self.downloadPic(self.png)
            return False


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    tab = TabDialog()
    sys.exit(app.exec_())