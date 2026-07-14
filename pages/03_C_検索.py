import pandas as pd
import streamlit as st
from db import get_connection

st.title("タスク検索・絞り込み")

keyword = st.text_input("タスク名で検索（キーワードを入力）")
status_choice = st.selectbox("ステータスで絞り込み", ["すべて", "未着手", "進行中", "完了"])

sql = """
SELECT
    t.task_id AS ID,
    t.title AS タスク名,
    t.content AS 詳細内容,
    s.name AS ステータス,
    t.deadline AS 期限
FROM task t
JOIN statuses s ON t.status_id = s.status_id
WHERE 1=1
"""

params = []

if keyword:
    sql += " AND t.title LIKE %s"
    params.append(f"%{keyword}%")

if status_choice != "すべて":
    sql += " AND s.name = %s"
    params.append(status_choice)

sql += " ORDER BY t.deadline ASC"

try:
    conn = get_connection()
    df = pd.read_sql(sql, conn, params=params)
    conn.close()

    st.write(f"検索結果: {len(df)} 件")

    if len(df) > 0:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("該当するタスクが見つかりませんでした。")

except Exception as e:
    st.error(f"エラーが発生しました: {e}")
