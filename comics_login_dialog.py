from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QMessageBox
)
from comics_db_helper import DB, DB_CONFIG


class SignupDialog(QDialog):
    """회원가입 전용 다이얼로그"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("회원가입")
        self.db = DB(**DB_CONFIG)

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password_confirm = QLineEdit()
        self.password_confirm.setEchoMode(QLineEdit.Password)

        form = QFormLayout()
        form.addRow("아이디", self.username)
        form.addRow("비밀번호", self.password)
        form.addRow("비밀번호 확인", self.password_confirm)

        self.btn_signup = QPushButton("가입하기")
        self.btn_signup.clicked.connect(self.try_signup)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.btn_signup)
        self.setLayout(layout)

    def try_signup(self):
        uid = self.username.text().strip()
        pw = self.password.text().strip()
        pw_confirm = self.password_confirm.text().strip()

        if not uid or not pw or not pw_confirm:
            QMessageBox.warning(self, "오류", "모든 항목을 입력하세요.")
            return

        if pw != pw_confirm:
            QMessageBox.warning(self, "오류", "비밀번호가 일치하지 않습니다.")
            return

        ok = self.db.register_user(uid, pw)
        if ok:
            QMessageBox.information(self, "완료", "회원가입이 완료되었습니다. 로그인해주세요.")
            self.accept()
        else:
            QMessageBox.critical(self, "실패", "이미 존재하는 아이디입니다.")


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("로그인 - 만화책 재고 관리")
        self.db = DB(**DB_CONFIG)

        # 로그인 성공 시 여기에 로그인한 사용자의 id가 저장됨
        self.user_id = None

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        form = QFormLayout()
        form.addRow("아이디", self.username)
        form.addRow("비밀번호", self.password)

        self.btn_login = QPushButton("로그인")
        self.btn_login.clicked.connect(self.try_login)

        self.btn_signup = QPushButton("회원가입")
        self.btn_signup.clicked.connect(self.open_signup)

        btn_row = QHBoxLayout()
        btn_row.addWidget(self.btn_login)
        btn_row.addWidget(self.btn_signup)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addLayout(btn_row)
        self.setLayout(layout)

    def try_login(self):
        uid = self.username.text().strip()
        pw = self.password.text().strip()
        if not uid or not pw:
            QMessageBox.warning(self, "오류", "아이디와 비밀번호를 모두 입력하세요.")
            return

        user_id = self.db.verify_user(uid, pw)
        if user_id is not None:
            self.user_id = user_id   # 로그인한 사용자의 id를 저장해둠
            self.accept()
        else:
            QMessageBox.critical(self, "실패", "아이디 또는 비밀번호가 올바르지 않습니다.")

    def open_signup(self):
        dialog = SignupDialog(self)
        dialog.exec_()   # 회원가입 창을 닫으면 다시 로그인 화면으로 돌아옴