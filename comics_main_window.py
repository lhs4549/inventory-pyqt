from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, \
    QLabel, QLineEdit, QPushButton, QMessageBox, QHeaderView
from comics_db_helper import DB, DB_CONFIG


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("만화책 재고 관리")
        self.db = DB(**DB_CONFIG)
        self.selected_id = None
 
        central = QWidget()
        self.setCentralWidget(central)
        vbox = QVBoxLayout(central)
 
        # ---------- 입력 필드 (라벨을 입력창 '위'에 배치) ----------
        def make_field(label_text):
            box = QVBoxLayout()
            box.setSpacing(4)
            label = QLabel(label_text)
            line_edit = QLineEdit()
            box.addWidget(label)
            box.addWidget(line_edit)
            return box, line_edit
 
        title_box, self.input_title = make_field("제목")
        author_box, self.input_author = make_field("작가")
        volume_box, self.input_volume = make_field("권수")
        price_box, self.input_price = make_field("가격")
        stock_box, self.input_stock = make_field("재고")
 
        # 1행: 제목 + 작가
        row1 = QHBoxLayout()
        row1.addLayout(title_box)
        row1.addLayout(author_box)
 
        # 2행: 권수 + 가격 + 재고
        row2 = QHBoxLayout()
        row2.addLayout(volume_box)
        row2.addLayout(price_box)
        row2.addLayout(stock_box)
 
        # 입력 필드 전체(1행+2행)를 세로로 묶기
        fields_col = QVBoxLayout()
        fields_col.setSpacing(10)
        fields_col.addLayout(row1)
        fields_col.addLayout(row2)
 
        # ---------- 버튼 (오른쪽, 세로 배치) ----------
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
 
        # 입력 필드 + 버튼을 가로로 배치
        form_row = QHBoxLayout()
        form_row.addLayout(fields_col)
        form_row.addLayout(btn_box)
 
        # ---------- 테이블 ----------
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "제목", "작가", "권수", "가격", "재고"])
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(self.table.SelectRows)   # 행 전체 선택
        self.table.setSelectionMode(self.table.SingleSelection)  # 한 번에 한 행만
        self.table.cellClicked.connect(self.on_row_clicked)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)       # 기본은 고정 너비
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # 제목
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # 작가
        self.table.setColumnWidth(0, 30)   # ID
        self.table.setColumnWidth(3, 60)   # 권수
        self.table.setColumnWidth(4, 80)   # 가격
        self.table.setColumnWidth(5, 60)   # 재고

 
        vbox.addLayout(form_row)
        vbox.addWidget(self.table)
 
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