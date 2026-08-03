# 📚 만화책 재고 관리 (inventory-pyqt)

PyQt5 + PyMySQL로 만든 **회원별 만화책 재고 관리 프로그램**입니다.
회원가입 후 로그인하면, **본인이 등록한 만화책만** 조회·추가·수정·삭제할 수 있습니다.

---

## ✨ 주요 기능

- 회원가입 / 로그인
- 로그인한 회원 본인의 만화책 목록 조회
- 만화책 추가 / 수정 / 삭제
- 다른 회원이 등록한 책은 보이지도, 수정/삭제되지도 않음

---

## 🗂️ 테이블 구조

**users** (회원)
| 컬럼 | 설명 |
| --- | --- |
| id | 회원 고유번호 (PK) |
| username | 아이디 (중복 불가) |
| password | 비밀번호 |

**comics** (만화책)
| 컬럼 | 설명 |
| --- | --- |
| id | 책 고유번호 (PK) |
| user_id | 이 책을 등록한 회원의 id (users.id 참조) |
| title / author / volume / price / stock | 제목 / 작가 / 권수 / 가격 / 재고 |

> 핵심: `comics.user_id`가 `users.id`를 가리켜서, **"이 책은 이 회원 것"**이라는 관계를 만듭니다.

---

## 🔑 동작 원리 (가장 중요한 부분)

1. **로그인 성공 시 `verify_user()`가 True/False가 아니라 해당 회원의 `id`(user_id)를 반환**합니다.
2. 로그인창은 이 `user_id`를 기억해두었다가, 메인 화면을 열 때 그대로 넘겨줍니다.
3. 메인 화면은 이후 모든 조회/추가/수정/삭제에 **`user_id`를 항상 함께 사용**합니다.
   - 조회: `WHERE user_id=%s` → 내 책만 보임
   - 추가: 새 책에 `user_id` 저장 → "내 책"으로 등록됨
   - 수정/삭제: `WHERE id=%s AND user_id=%s` → id를 알아도 내 책이 아니면 절대 수정/삭제 불가 (보안)

---

## 🛠️ 사용 기술

Python 3 · PyQt5 · PyMySQL · MySQL

---

## 📁 파일 구성

```
inventory-pyqt/
├── comics_app.py           # 실행 진입점 (로그인 → 메인화면 연결)
├── comics_db_helper.py     # DB 함수 (회원가입/로그인/조회/추가/수정/삭제)
├── comics_login_dialog.py  # 로그인 화면 + 회원가입 화면
├── comics_main_window.py   # 메인 화면 (목록 + 추가/수정/삭제 UI)
├── comicdb_full.sql        # DB 생성 스크립트
└── README.md
```

---

## 🚀 실행 방법

1. MySQL에서 `comicdb_full.sql` 실행 (DB·테이블 생성)
2. 패키지 설치
   ```bash
   pip install pymysql PyQt5
   ```
3. `comics_db_helper.py`의 `DB_CONFIG`에 본인 MySQL 접속 정보 입력
4. 실행
   ```bash
   python comics_app.py
   ```
5. "회원가입"으로 새 계정을 만든 뒤 로그인 → 빈 목록에서 시작 → 만화책 추가 테스트