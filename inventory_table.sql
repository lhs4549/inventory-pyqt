CREATE DATABASE IF NOT EXISTS comicdb DEFAULT CHARACTER SET utf8mb4;
USE comicdb;

-- 회원 테이블
CREATE TABLE IF NOT EXISTS users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(100) NOT NULL
);

INSERT INTO users (username, password) VALUES ('admin', 'admin123')
ON DUPLICATE KEY UPDATE password=VALUES(password);

-- 만화책 테이블 (user_id로 회원별 소유 구분)
CREATE TABLE IF NOT EXISTS comics (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  title VARCHAR(100) NOT NULL,
  author VARCHAR(50) NOT NULL,
  volume INT NOT NULL,
  price INT NOT NULL,
  stock INT NOT NULL DEFAULT 0,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- admin 계정 기준 예시 데이터
INSERT INTO comics (user_id, title, author, volume, price, stock)
VALUES
((SELECT id FROM users WHERE username='admin'), '원피스', '오다 에이치로', 100, 4950, 5),
((SELECT id FROM users WHERE username='admin'), '나루토', '키시모토 마사시', 70, 4900, 10),
((SELECT id FROM users WHERE username='admin'), '블루 록', '카네시로 무네유키', 30, 5400, 12);