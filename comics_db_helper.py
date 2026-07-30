import pymysql

DB_CONFIG = dict(
    host="localhost",
    user="root",
    password="4549",
    database="comicdb",
    charset="utf8"
)


class DB:
    def __init__(self, **config):
        self.config = config

    def connect(self):
        return pymysql.connect(**self.config)

    # ---------- 회원가입 ----------
    def register_user(self, username, password):
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, (username, password))
                conn.commit()
                return True
            except Exception:
                # username이 UNIQUE라서, 이미 있는 아이디면 여기서 에러가 남
                conn.rollback()
                return False

    # ---------- 로그인 검증 ----------
    def verify_user(self, username, password):
        sql = "SELECT id FROM users WHERE username=%s AND password=%s"
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (username, password))
                row = cur.fetchone()
                if row:
                    return row[0]   # user_id 반환
                return None

    # ---------- 만화책 전체 조회 (로그인한 회원 것만) ----------
    def fetch_comics(self, user_id):
        sql = "SELECT id, title, author, volume, price, stock FROM comics WHERE user_id=%s ORDER BY id"
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (user_id,))
                return cur.fetchall()

    # ---------- 만화책 추가 (로그인한 회원 소유로 등록) ----------
    def insert_comic(self, user_id, title, author, volume, price, stock):
        sql = "INSERT INTO comics (user_id, title, author, volume, price, stock) VALUES (%s, %s, %s, %s, %s, %s)"
        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, (user_id, title, author, volume, price, stock))
                conn.commit()
                return True
            except Exception:
                conn.rollback()
                return False

    # ---------- 만화책 수정 (id + user_id 둘 다 일치해야 수정됨) ----------
    def update_comic(self, comic_id, user_id, title, author, volume, price, stock):
        sql = "UPDATE comics SET title=%s, author=%s, volume=%s, price=%s, stock=%s WHERE id=%s AND user_id=%s"
        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, (title, author, volume, price, stock, comic_id, user_id))
                conn.commit()
                return True
            except Exception:
                conn.rollback()
                return False

    # ---------- 만화책 삭제 (id + user_id 둘 다 일치해야 삭제됨) ----------
    def delete_comic(self, comic_id, user_id):
        sql = "DELETE FROM comics WHERE id=%s AND user_id=%s"
        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, (comic_id, user_id))
                conn.commit()
                return True
            except Exception:
                conn.rollback()
                return False