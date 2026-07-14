# タスク管理アプリ（データベース演習 班2-11）

麗澤大学 データベースシステム演習のグループワーク成果物です。  
Streamlit + MySQL でタスクの一覧・登録・検索・状態変更・タグ付けを行います。

## 機能と担当

| ページ | 担当 |
|---|---|
| A 一覧表示 | 水谷（暫定版） |
| B 登録 | 山﨑 |
| C 検索 | 松下 |
| D 状態変更 | 牧野 |
| I タグ付け | 前田 |

## 前提

- Docker Desktop
- [dbclass-mysql](https://github.com/) 相当の MySQL コンテナ（`student` / `student`）
- Python 3.10+（[uv](https://github.com/astral-sh/uv) 推奨）

## セットアップ

```powershell
# 1. MySQL 起動（docker-compose.yml がある場所で）
docker compose up -d

# 2. データベース作成（初回のみ・sampledb と衝突する場合）
docker exec -i dbclass-mysql-db-1 mysql -uroot -proot -e "CREATE DATABASE IF NOT EXISTS task_app CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; GRANT ALL ON task_app.* TO 'student'@'%'; FLUSH PRIVILEGES;"

# 3. スキーマ投入
Get-Content .\schema.sql | docker exec -i dbclass-mysql-db-1 mysql -ustudent -pstudent task_app

# 4. アプリ起動
uv run --with streamlit --with pandas --with mysql-connector-python streamlit run app.py
```

`db.py` の `port` と `database` は各自の Docker 設定に合わせて変更してください。

## 構成

```
├── schema.sql      # 班共通テーブル定義
├── db.py           # DB接続（共通）
├── app.py          # ホーム
└── pages/          # 1人1機能
```

## ライセンス

授業課題用。再配布・商用利用は授業ルールに従ってください。
