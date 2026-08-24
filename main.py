from fastapi import FastAPI
from fastapi import HTTPException
from schemas import DocumentCreate
from database import (
    init_db,
    insert_document,
    get_all_documents,
    get_document_by_id
    )

app = FastAPI()

init_db()

@app.get("/")
def simple_get():
    return {"message": "hello"}

@app.get("/health") 
def get_health():
    return {"status": "ok"}


@app.post("/documents")
def create_document(document: DocumentCreate):
    doc_id = insert_document(document.title, document.content, "active")
    return {
        "title": f"{document.title}",
        "content": f"{document.content}",
        "id": doc_id
            }

@app.get("/documents")
def list_documents():
    documents = get_all_documents()
    return documents


@app.get("/documents/{document_id}")
def get_document(document_id: int):
    document = get_document_by_id(document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document