-- ============================================================
-- タスク管理アプリ スキーマ  (班2-11)
-- 第11回〜第12回 グループワーク共通
-- ============================================================
--
-- 流し込み例 (C:\dbclass-mysql で docker compose up -d 後):
--   Get-Content .\schema.sql |
--     docker compose exec -T db mysql -ustudent -pstudent sampledb
--
-- ※ sampledb に他課題の users 等があると DROP に失敗する場合:
--   docker exec -i dbclass-mysql-db-1 mysql -uroot -proot -e "CREATE DATABASE IF NOT EXISTS task_app ..."
--   Get-Content .\schema.sql | docker exec -i dbclass-mysql-db-1 mysql -ustudent -pstudent task_app
--   → db.py の database を task_app に変更して動作確認
--
-- ============================================================

DROP TABLE IF EXISTS task_tags;
DROP TABLE IF EXISTS task;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS statuses;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id   INT          AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(50)  NOT NULL
);

CREATE TABLE statuses (
    status_id INT         AUTO_INCREMENT PRIMARY KEY,
    name      VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE tags (
    tag_id INT         AUTO_INCREMENT PRIMARY KEY,
    name   VARCHAR(20) NOT NULL UNIQUE,
    color  VARCHAR(10)
);

CREATE TABLE task (
    task_id   INT          AUTO_INCREMENT PRIMARY KEY,
    user_id   INT          NOT NULL,
    status_id INT          NOT NULL,
    title     VARCHAR(50)  NOT NULL,
    content   TEXT,
    deadline  DATE,
    FOREIGN KEY (user_id)   REFERENCES users(user_id),
    FOREIGN KEY (status_id) REFERENCES statuses(status_id)
);

CREATE TABLE task_tags (
    task_id INT NOT NULL,
    tag_id  INT NOT NULL,
    PRIMARY KEY (task_id, tag_id),
    FOREIGN KEY (task_id) REFERENCES task(task_id),
    FOREIGN KEY (tag_id)  REFERENCES tags(tag_id)
);

INSERT INTO users (user_name) VALUES
    ('前田'),
    ('牧野'),
    ('松下'),
    ('水谷'),
    ('山崎');

INSERT INTO statuses (name) VALUES
    ('未着手'),
    ('進行中'),
    ('完了');

INSERT INTO tags (name, color) VALUES
    ('授業',   '#6366f1'),
    ('急ぎ',   '#ef4444'),
    ('生活',   '#10b981');

INSERT INTO task (user_id, status_id, title, content, deadline) VALUES
    (1, 1, 'レポートを出す',   'DB演習のレポート',  '2026-07-10'),
    (1, 2, 'スライドを作る',   '発表用スライド',    '2026-07-07'),
    (2, 1, '買い物に行く',    NULL,               '2026-07-01');

INSERT INTO task_tags (task_id, tag_id) VALUES
    (1, 1),
    (1, 2),
    (2, 1),
    (3, 3);
