import sqlite3
import os
from datetime import datetime
import uuid

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../../data/drafts.db")


# ==============================
# 🔹 DB INIT
# ==============================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drafts (
        id TEXT PRIMARY KEY,
        username TEXT,
        title TEXT,
        content TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# ==============================
# 🔹 CREATE
# ==============================
def add_draft(username, title, content):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 🔥 CHECK LIMIT (10 drafts per user)
    cursor.execute("""
        SELECT COUNT(*) FROM drafts WHERE username = ?
    """, (username,))
    
    count = cursor.fetchone()[0]

    if count >= 10:
        conn.close()
        return {"error": "Draft limit reached (max 10)"}

    # 🔥 INSERT
    draft_id = str(uuid.uuid4())

    cursor.execute("""
        INSERT INTO drafts (id, username, title, content, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (draft_id, username, title, content, datetime.now().isoformat()))

    conn.commit()
    conn.close()

    return {"id": draft_id, "message": "Created"}


# ==============================
# 🔹 GET ALL
# ==============================
def load_drafts(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, content, created_at
        FROM drafts
        WHERE username = ?
        ORDER BY created_at DESC
    """, (username,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "title": r[1],
            "content": r[2],
            "created_at": r[3]
        }
        for r in rows
    ]


# ==============================
# 🔹 DELETE
# ==============================
def delete_draft(username, draft_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM drafts
        WHERE id = ? AND username = ?
    """, (draft_id, username))

    conn.commit()
    conn.close()

    return {"message": "Deleted"}


# ==============================
# 🔹 SEARCH
# ==============================
def search_drafts(username, query):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = f"%{query.lower()}%"

    cursor.execute("""
        SELECT id, title, content, created_at
        FROM drafts
        WHERE username = ?
        AND (LOWER(title) LIKE ? OR LOWER(content) LIKE ?)
        ORDER BY created_at DESC
    """, (username, query, query))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "title": r[1],
            "content": r[2],
            "created_at": r[3]
        }
        for r in rows
    ]