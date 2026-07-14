import streamlit as st
import pandas as pd
from db import get_connection

st.title("タスクの状態変更")

conn = get_connection()
cur = conn.cursor()

cur.execute(
    """
    SELECT status_id, name
    FROM statuses
    """
)
status_rows = cur.fetchall()
status_dict = {name: sid for sid, name in status_rows}

cur.execute(
    """
    SELECT t.task_id, t.title, s.name
    FROM task t
    JOIN statuses s ON t.status_id = s.status_id
    ORDER BY t.task_id ASC
    """
)
task_rows = cur.fetchall()

if not task_rows:
    st.info("変更できるタスクがありません。")
    cur.close()
    conn.close()
    st.stop()

task_choices = {
    f"{tid}: {title}（{sname}）": tid
    for tid, title, sname in task_rows
}

st.subheader("対象タスクの選択")
selected_task_label = st.selectbox(
    "状態を変更するタスク",
    list(task_choices.keys()),
)

st.subheader("新しい状態の選択")
selected_status_name = st.selectbox(
    "新しい状態",
    list(status_dict.keys()),
)

if st.button("状態を変更する"):
    new_status_id = status_dict[selected_status_name]
    target_task_id = task_choices[selected_task_label]

    cur.execute(
        """
        UPDATE task
        SET status_id = %s
        WHERE task_id = %s
        """,
        (new_status_id, target_task_id),
    )
    conn.commit()
    st.success("状態を変更しました")
    st.rerun()

cur.close()
conn.close()
