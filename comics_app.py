import sys
from PyQt5.QtWidgets import QApplication
from comics_login_dialog import LoginDialog
from comics_main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginDialog()
    if login.exec_() == LoginDialog.Accepted:
        w = MainWindow(login.user_id)   # 로그인한 사용자의 id를 메인 화면에 전달
        w.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)