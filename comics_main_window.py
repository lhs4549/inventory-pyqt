from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, \
    QLabel, QLineEdit, QPushButton, QMessageBox
from comics_db_helper import DB, DB_CONFIG


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("만화책 재고 관리")
        self.db = DB(**DB_CONFIG)

        # 현재 선택된 행의 id를 저장 (수정/삭제할 때 사용)
        self.selected_id = None

        # 중앙 위젯 및 레이아웃
        central = QWidget()
        self.setCentralWidget(central)
        vbox = QVBoxLayout(central)

        # 상단: 입력 폼(왼쪽) + 버튼(오른쪽) 가로 배치
        form_row = QHBoxLayout()

        # 왼쪽: 입력 필드들
        input_box = QHBoxLayout()
        self.input_title = QLineEdit()
        self.input_author = QLineEdit()
        self.input_volume = QLineEdit()
        self.input_price = QLineEdit()
        self.input_stock = QLineEdit()

        input_box.addWidget(QLabel("제목"))
        input_box.addWidget(self.input_title)
        input_box.addWidget(QLabel("작가"))
        input_box.addWidget(self.input_author)
        input_box.addWidget(QLabel("권수"))
        input_box.addWidget(self.input_volume)
        input_box.addWidget(QLabel("가격"))
        input_box.addWidget(self.input_price)
        input_box.addWidget(QLabel("재고"))
        input_box.addWidget(self.input_stock)

        # 오른쪽: 버튼 세로 배치 (일정 간격)
        btn_box = QVBoxLayout()
        btn_box.setSpacing(10)
        self.btn_add = QPushButton("추가")
        self.btn_update = QPushButton("수정")
        self.btn_delete = QPushButton("삭제")
        for btn in (self.btn_add, self.btn_update, self.btn_delete):
            btn.setFixedSize(80, 30)
        btn_box.addWidget(self.btn_add)
        btn_box.addWidget(self.btn_update)
        btn_box.addWidget(self.btn_delete)

        self.btn_add.clicked.connect(self.add_comic)
        self.btn_update.clicked.connect(self.update_comic)
        self.btn_delete.clicked.connect(self.delete_comic)

        form_row.addLayout(input_box)
        form_row.addLayout(btn_box)

        # 중앙: 테이블 위젯
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "제목", "작가", "권수", "가격", "재고"])
        self.table.setEditTriggers(self.table.NoEditTriggers)  # 목록은 읽기 전용
        self.table.verticalHeader().setVisible(False)
        self.table.cellClicked.connect(self.on_row_clicked)  # 행 클릭 시 입력창 채우기

        # 배치
        vbox.addLayout(form_row)
        vbox.addWidget(self.table)

        # 초기 데이터 로드
        self.load_comics()

    # ---------- 목록 조회 ----------
    def load_comics(self):
        rows = self.db.fetch_comics()
        self.table.setRowCount(len(rows))
        for r, (cid, title, author, volume, price, stock) in enumerate(rows):
            self.table.setItem(r, 0, QTableWidgetItem(str(cid)))
            self.table.setItem(r, 1, QTableWidgetItem(title))
            self.table.setItem(r, 2, QTableWidgetItem(author))
            self.table.setItem(r, 3, QTableWidgetItem(str(volume)))
            self.table.setItem(r, 4, QTableWidgetItem(str(price)))
            self.table.setItem(r, 5, QTableWidgetItem(str(stock)))
        self.table.resizeColumnsToContents()

    # ---------- 행 클릭 시 입력창 자동 채움 ----------
    def on_row_clicked(self, row, col):
        self.selected_id = int(self.table.item(row, 0).text())
        self.input_title.setText(self.table.item(row, 1).text())
        self.input_author.setText(self.table.item(row, 2).text())
        self.input_volume.setText(self.table.item(row, 3).text())
        self.input_price.setText(self.table.item(row, 4).text())
        self.input_stock.setText(self.table.item(row, 5).text())

    # ---------- 입력값 검증 (공통) ----------
    def get_input_values(self):
        title = self.input_title.text().strip()
        author = self.input_author.text().strip()
        volume = self.input_volume.text().strip()
        price = self.input_price.text().strip()
        stock = self.input_stock.text().strip()

        if not title or not author or not volume or not price or not stock:
            QMessageBox.warning(self, "오류", "모든 항목을 입력하세요.")
            return None

        try:
            volume = int(volume)
            price = int(price)
            stock = int(stock)
        except ValueError:
            QMessageBox.warning(self, "오류", "권수/가격/재고는 숫자로 입력하세요.")
            return None

        return title, author, volume, price, stock

    # ---------- 입력창 초기화 ----------
    def clear_inputs(self):
        self.input_title.clear()
        self.input_author.clear()
        self.input_volume.clear()
        self.input_price.clear()
        self.input_stock.clear()
        self.selected_id = None

    # ---------- 추가 ----------
    def add_comic(self):
        values = self.get_input_values()
        if values is None:
            return
        title, author, volume, price, stock = values

        ok = self.db.insert_comic(title, author, volume, price, stock)
        if ok:
            QMessageBox.information(self, "완료", "추가되었습니다.")
            self.clear_inputs()
            self.load_comics()
        else:
            QMessageBox.critical(self, "실패", "추가 중 오류가 발생했습니다.")

    # ---------- 수정 ----------
    def update_comic(self):
        if self.selected_id is None:
            QMessageBox.warning(self, "오류", "수정할 항목을 목록에서 먼저 선택하세요.")
            return

        values = self.get_input_values()
        if values is None:
            return
        title, author, volume, price, stock = values

        ok = self.db.update_comic(self.selected_id, title, author, volume, price, stock)
        if ok:
            QMessageBox.information(self, "완료", "수정되었습니다.")
            self.clear_inputs()
            self.load_comics()
        else:
            QMessageBox.critical(self, "실패", "수정 중 오류가 발생했습니다.")

    # ---------- 삭제 ----------
    def delete_comic(self):
        if self.selected_id is None:
            QMessageBox.warning(self, "오류", "삭제할 항목을 목록에서 먼저 선택하세요.")
            return

        reply = QMessageBox.question(
            self, "확인", "정말 삭제하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        ok = self.db.delete_comic(self.selected_id)
        if ok:
            QMessageBox.information(self, "완료", "삭제되었습니다.")
            self.clear_inputs()
            self.load_comics()
        else:
            QMessageBox.critical(self, "실패", "삭제 중 오류가 발생했습니다.")