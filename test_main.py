import pytest
import os
from fastapi.testclient import TestClient
import database
import main


@pytest.fixture
def client():
    database.DB_NAME = "test_documents.db"
    database.init_db()
    test_client = TestClient(main.app)

    yield test_client

    if os.path.exists("test_documents.db"):
        os.remove("test_documents.db")


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "hello"}


def test_create_document(client):
    response = client.post(
        "/documents", json={"title": "post_title", "content": "post_content"}
    )
    assert response.status_code == 200
    doc_id = response.json()["id"]
    assert response.json() == {
        "title": "post_title",
        "content": "post_content",
        "id": doc_id,
    }


def test_create_document_missing_title(client):
    response = client.post("/documents", json={"content": "post_content"})
    assert response.status_code == 422


def test_create_document_missing_content(client):
    response = client.post("/documents", json={"title": "post_title"})
    assert response.status_code == 422


def test_list_documents_empty(client):
    response = client.get("/documents")
    assert response.json() == []


def test_list_documents_after_create(client):
    response = client.post(
        "/documents", json={"title": "post_title", "content": "post_content"}
    )
    response = client.get("/documents")
    assert len(response.json()) > 0


def test_get_document_by_id(client):
    response = client.post(
        "/documents", json={"title": "post_title", "content": "post_content"}
    )
    doc_id = response.json()["id"]
    response2 = client.get(f"/documents/{doc_id}")
    assert response2.json()["id"] == doc_id
    assert response2.json()["status"] == "active"
    assert response2.json()["title"] == "post_title"
    assert response2.json()["content"] == "post_content"


def test_get_document_not_found(client):
    response = client.get("/documents/9999")
    assert response.status_code == 404


def test_delete_document(client):
    response = client.post(
        "/documents", json={"title": "test_title", "content": "test_content"}
    )
    doc_id = response.json()["id"]

    response2 = client.delete(f"/documents/{doc_id}")
    assert response2.status_code == 200


def test_delete_document_not_found(client):
    response = client.delete("/documents/999")
    assert response.status_code == 404


def test_delete_then_get(client):
    response = client.post(
        "/documents", json={"title": "test_title", "content": "test_content"}
    )
    doc_id = response.json()["id"]
    client.delete(f"/documents/{doc_id}")
    response2 = client.get(f"/documents/{doc_id}")

    assert response2.status_code == 404


# Update document tests
def test_update_document(client):
    response = client.post(
        "/documents", json={"title": "old title", "content": "old content"}
    )
    doc_id = response.json()["id"]

    response2 = client.put(
        f"/documents/{doc_id}",
        json={"title": "update title", "content": "update content"},
    )
    assert response2.status_code == 200

    response3 = client.get(f"/documents/{doc_id}")
    assert response3.json()["id"] == doc_id
    assert response3.json()["title"] == "update title"
    assert response3.json()["content"] == "update content"


def test_update_document_not_found(client):
    response = client.put(
        "/documents/9999", json={"title": "update title", "content": "update content"}
    )
    assert response.status_code == 404


def test_update_document_missing_field(client):
    response = client.post(
        "/documents", json={"title": "old title", "content": "old content"}
    )
    doc_id = response.json()["id"]

    response2 = client.put(f"/documents/{doc_id}", json={"title": "update title"})
    assert response2.status_code == 422


def test_list_documents_filter_by_status(client):
    client.post("/documents", json={"title": "t1", "content": "c1"})

    response = client.get("/documents?status=active")
    assert len(response.json()) > 0

    for doc in response.json():
        assert doc["status"] == "active"

    response2 = client.get("/documents?status=inactive")
    assert response2.json() == []
