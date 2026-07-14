import streamlit as st
from db import get_connection

st.title("B. 登録")

conn = get_connection()
cur = conn.cursor()

try:
    cur.execute("SELECT user_id, user_name FROM users")
    user_to_id = {name: uid for uid, name in cur.fetchall()}

    cur.execute("SELECT status_id, name FROM statuses")
    status_to_id = {name: sid for sid, name in cur.fetchall()}

    cur.execute("SELECT tag_id, name FROM tags")
    tag_to_id = {name: tid for tid, name in cur.fetchall()}

    assignee = st.text_input("担当")
    status = st.selectbox("状態", list(status_to_id.keys()))
    title = st.text_input("タイトル")
    content = st.text_area("内容", height=120)
    deadline = st.date_input("期限", value=None)
    tags = st.multiselect("タグ", list(tag_to_id.keys()))

    if st.button("登録する"):
        if not title.strip():
            st.warning("タイトルを入力してください")
        elif not assignee.strip():
            st.warning("担当者を入力してください")
        else:
            try:
                assignee_name = assignee.strip()
                cur.execute("SELECT user_id FROM users WHERE user_name = %s", (assignee_name,))
                user_row = cur.fetchone()

                if user_row is None:
                    cur.execute("INSERT INTO users (user_name) VALUES (%s)", (assignee_name,))
                    user_id = cur.lastrowid
                else:
                    user_id = user_row[0]

                sql = """
                INSERT INTO task
                (user_id, status_id, title, content, deadline)
                VALUES (%s, %s, %s, %s, %s)
                """

                cur.execute(
                    sql,
                    (
                        user_id,
                        status_to_id[status],
                        title,
                        content or None,
                        deadline,
                    ),
                )

                task_id = cur.lastrowid

                for tag in tags:
                    cur.execute(
                        "INSERT INTO task_tags(task_id, tag_id) VALUES (%s,%s)",
                        (task_id, tag_to_id[tag]),
                    )

                conn.commit()
                st.success(f"登録しました：{title}")
                st.rerun()

            except Exception as e:
                conn.rollback()
                st.error(e)

finally:
    cur.close()
    conn.close()
