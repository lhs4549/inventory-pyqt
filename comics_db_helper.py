import pymysql

DB_CONFIG = dict(
    host="localhost",
    user="root",
    password="3554demon!",
    database="comicdb",
    charset="utf8"
)

class DB:
    def __init__(self, **config):
        self.config = config

    def connect(self):
        return pymysql.connect(**self.config)

    # 로그인 검증
    def verify_user(self, username, password):
        sql = "SELECT COUNT(*) FROM users WHERE username=%s AND password=%s"
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (username, password))
                count, = cur.fetchone()
                return count == 1

    # 만화책 전체 조회
    def fetch_comics(self):
        sql = "SELECT id, title, author, volume, price, stock FROM comics ORDER BY id"
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()  # [(id, title, author, volume, price, stock), ...]

    # 만화책 추가
    def insert_comic(self, title, author, volume, price, stock):
        sql = "INSERT INTO comics (title, author, volume, price, stock) VALUES (%s, %s, %s, %s, %s)"
        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, (title, author, volume, price, stock))
                conn.commit()
                return True
            except Exception:
                conn.rollback()
                return False

    # 만화책 수정 (id 기준)
    def update_comic(self, comic_id, title, author, volume, price, stock):
        sql = "UPDATE comics SET title=%s, author=%s, volume=%s, price=%s, stock=%s WHERE id=%s"
        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, (title, author, volume, price, stock, comic_id))
                conn.commit()
                return True
            except Exception:
                conn.rollback()
                return False
            
    # 만화책 삭제 (id 기준)
    def delete_comic(self, comic_id):
        sql = "DELETE FROM comics WHERE id=%s"
        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, (comic_id,))
                conn.commit()
                return True
            except Exception:
                conn.rollback()
                return False