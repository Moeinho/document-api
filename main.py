from fastapi import FastAPI
from fastapi import HTTPException
from schemas import DocumentCreate
from database import (
    init_db,
    insert_document,
    get_all_documents,
    get_document_by_id,
    delete_document,
    update_document,
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
        "title": document.title,
        "content": document.content,
        "id": doc_id,
    }


@app.get("/documents")
def list_documents(status: str | None = None):
    documents = get_all_documents(status=status)
    return documents


@app.get("/documents/{document_id}")
def get_document(document_id: int):
    document = get_document_by_id(document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@app.delete("/documents/{document_id}")
def delete_document_route(document_id: int):
    is_deleted = delete_document(document_id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document deleted"}


@app.put("/documents/{document_id}")
def update_document_route(document_id: int, document: DocumentCreate):
    is_updated = update_document(document_id, document.title, document.content)
    if not is_updated:
        raise HTTPException(status_code=404, detail="Document not found")
    return {
        "id": document_id,
        "title": document.title,
        "content": document.content,
    }
