import sqlite3
from datetime import datetime


def init_db():
    conn = sqlite3.connect("documents.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT NOT NULL,
        status TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()


def insert_document(title, content, status):
    now_str = datetime.now().isoformat()

    conn = sqlite3.connect("documents.db")
    cursor = conn.cursor()
    cursor.execute(
        """
    INSERT INTO documents (title, content, created_at, status)
        VALUES (?, ?, ?, ?)
    """,
        (title, content, now_str, status),
    )

    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return new_id


def get_all_documents():
    conn = sqlite3.connect("documents.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documents")
    conn.commit()
    documents = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "content": row[2],
            "created_at": row[3],
            "status": row[4],
        }
        for row in documents
    ]


def get_document_by_id(document_id):
    conn = sqlite3.connect("documents.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM documents WHERE id = ?",
        (document_id,)
        )

    conn.commit()
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        return None
    
    dict_row = {
            "id": row[0],
            "title": row[1],
            "content": row[2],
            "created_at": row[3],
            "status": row[4],
        }
    return dict_row

