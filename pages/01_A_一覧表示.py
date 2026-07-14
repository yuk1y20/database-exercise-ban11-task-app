# -*- coding: utf-8 -*-
# 担当: 水谷（一覧表示）— メンバー未提出のため暫定版
import pandas as pd
import streamlit as st
from db import get_connection

st.title("A. タスク一覧")

conn = get_connection()
df = pd.read_sql(
    """
    SELECT
        t.task_id AS ID,
        u.user_name AS 担当者,
        s.name AS 状態,
        t.title AS タスク名,
        t.content AS 内容,
        t.deadline AS 期限,
        GROUP_CONCAT(tg.name ORDER BY tg.tag_id SEPARATOR ', ') AS タグ
    FROM task t
    JOIN users u ON t.user_id = u.user_id
    JOIN statuses s ON t.status_id = s.status_id
    LEFT JOIN task_tags tt ON t.task_id = tt.task_id
    LEFT JOIN tags tg ON tt.tag_id = tg.tag_id
    GROUP BY t.task_id, u.user_name, s.name, t.title, t.content, t.deadline
    ORDER BY t.task_id
    """,
    conn,
)
conn.close()

st.dataframe(df, use_container_width=True)
