import sqlite3
from datetime import datetime

DB_NAME = "documents.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
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

    conn = sqlite3.connect(DB_NAME)
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


def get_all_documents(status=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if status:
        cursor.execute("SELECT * FROM documents WHERE status = ?", (status,))
    else:
        cursor.execute("SELECT * FROM documents")
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
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documents WHERE id = ?", (document_id,))

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


def delete_document(document_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM documents WHERE id = ?", (document_id,))
    conn.commit()
    deleted_count = cursor.rowcount
    conn.close()

    return True if deleted_count > 0 else False


def update_document(doc_id, title, content):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
    UPDATE documents
    SET title = ?, content = ?
    WHERE id = ?
    """,
        (title, content, doc_id),
    )
    conn.commit()
    updated_count = cursor.rowcount
    conn.close()

    return True if updated_count > 0 else False
