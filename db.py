# -*- coding: utf-8 -*-
# ============================================================
# db.py : 班で共通のDB接続部品(全員がこれを import する)
# 置き換えポイント: port は docker-compose.yml の ports に合わせる
# ============================================================
import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "port": 13306,  # C:\dbclass-mysql\docker-compose.yml の "13306:3306"
    "user": "student",
    "password": "student",
    "database": "task_app",  # 班内共通。sampledb は他課題と users が衝突しやすい
}


def get_connection():
    """呼ぶたびに新しい接続を返す(使い終わったら close すること)"""
    return mysql.connector.connect(**DB_CONFIG)
