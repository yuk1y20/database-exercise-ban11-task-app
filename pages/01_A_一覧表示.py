# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
from db import get_connection

st.title("A. 一覧表示")

# DB接続
conn = get_connection()

# 一覧取得
sql = """
SELECT
    t.task_id    AS ID,
    u.user_name  AS 担当者,
    s.name       AS 状態,
    t.title      AS タイトル,
    t.content    AS 内容,
    t.deadline   AS 締切
FROM task t
JOIN users u
    ON t.user_id = u.user_id
JOIN statuses s
    ON t.status_id = s.status_id
ORDER BY t.task_id DESC;
"""

df = pd.read_sql(sql, conn)

conn.close()

# 表示
st.dataframe(df, use_container_width=True)

# ランダム表示
if st.button("ランダムに1件表示"):
    conn = get_connection()

    one = pd.read_sql(
        "SELECT title FROM task ORDER BY RAND() LIMIT 1",
        conn
    )

    conn.close()

    if len(one) > 0:
        st.success(f"今日のタスク：{one.iloc[0]['title']}")
    else:
        st.warning("タスクが登録されていません。")