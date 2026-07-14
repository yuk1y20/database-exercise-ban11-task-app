# -*- coding: utf-8 -*-
# ============================================================
# カテゴリI: タグ付け・多対多(中間テーブル)
# 班2-11 タスク管理アプリ / 担当: 前田守海
#
# 「1つのタスクに複数のタグ」= 多対多 → 中間テーブル task_tags に分解
# タグを付ける = 中間テーブルに1行 INSERT するだけ
# タグを外す   = 中間テーブルから DELETE（task と tags 本体は消さない）
# タグで絞り込む = 中間テーブルを経由して「2回JOIN」する
#
# 置き換えポイント:
#   ・task / tags / task_tags は班の schema.sql のテーブル名
#   ・複合主キー(task_id, tag_id)で同じ組み合わせの重複を防ぐ
# ============================================================
import streamlit as st
import pandas as pd
import mysql.connector
from db import get_connection

st.title("I. タグ付け・多対多")

conn = get_connection()
cur = conn.cursor()

# タスクとタグの一覧を取得（selectbox 用）
cur.execute("SELECT task_id, title FROM task")
task_to_id = {f"{tid}: {title}": tid for tid, title in cur.fetchall()}

cur.execute("SELECT tag_id, name FROM tags")
tag_to_id = {name: tid for tid, name in cur.fetchall()}

if not task_to_id or not tag_to_id:
    st.warning("タスクまたはタグがありません。先に schema.sql を流し込んでください。")
    conn.close()
    st.stop()

# --- タグを付ける（INSERT）---
st.subheader("タグを付ける")

with st.form("add_tag"):
    task_choice = st.selectbox("タスク", list(task_to_id.keys()))
    tag_choice = st.selectbox("付けるタグ", list(tag_to_id.keys()))
    add_submitted = st.form_submit_button("タグを付ける")

    if add_submitted:
        try:
            cur.execute(
                "INSERT INTO task_tags (task_id, tag_id) VALUES (%s, %s)",
                (task_to_id[task_choice], tag_to_id[tag_choice]),
            )
            conn.commit()
            st.success("タグを付けました")
            st.rerun()
        except mysql.connector.IntegrityError:
            st.warning("そのタグはすでに付いています")

# --- タグを外す（DELETE）---
st.subheader("タグを外す")

cur.execute(
    """
    SELECT tt.task_id, t.title, tt.tag_id, tg.name AS tag_name
    FROM task_tags tt
    JOIN task t  ON tt.task_id = t.task_id
    JOIN tags tg ON tt.tag_id = tg.tag_id
    ORDER BY tt.task_id, tt.tag_id
    """
)
linked = cur.fetchall()

if not linked:
    st.info("外せるタグはありません。")
else:
    linked_to_key = {
        f"{task_id}: {title} / {tag_name}": (task_id, tag_id)
        for task_id, title, tag_id, tag_name in linked
    }

    with st.form("remove_tag"):
        remove_choice = st.selectbox("外す組み合わせ", list(linked_to_key.keys()))
        ok = st.checkbox("本当に外してよい")
        remove_submitted = st.form_submit_button("タグを外す")

        if remove_submitted:
            if not ok:
                st.warning("チェックボックスに同意してください。")
            else:
                task_id, tag_id = linked_to_key[remove_choice]
                cur.execute(
                    "DELETE FROM task_tags WHERE task_id = %s AND tag_id = %s",
                    (task_id, tag_id),
                )
                conn.commit()
                st.success("タグを外しました")
                st.rerun()

st.subheader("このタグが付いたタスクを見る")

# タグ名で絞り込み(多対多は必ず「2回JOIN」)
filter_tag = st.selectbox("タグで絞り込み", list(tag_to_id.keys()))
df = pd.read_sql(
    """
    SELECT t.title AS タスク名, tg.name AS タグ
    FROM task t
    JOIN task_tags tt ON t.task_id = tt.task_id
    JOIN tags tg ON tt.tag_id = tg.tag_id
    WHERE tg.name = %s
    """,
    conn,
    params=[filter_tag],
)
st.dataframe(df, use_container_width=True)

st.subheader("タスクごとのタグ一覧")

overview = pd.read_sql(
    """
    SELECT
        t.task_id AS タスクID,
        t.title AS タスク名,
        GROUP_CONCAT(tg.name ORDER BY tg.tag_id SEPARATOR ', ') AS タグ一覧
    FROM task t
    LEFT JOIN task_tags tt ON t.task_id = tt.task_id
    LEFT JOIN tags tg ON tt.tag_id = tg.tag_id
    GROUP BY t.task_id, t.title
    ORDER BY t.task_id
    """,
    conn,
)
st.dataframe(overview, use_container_width=True)

conn.close()
