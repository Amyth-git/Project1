from fastapi.testclient import TestClient

from project1.main import app

client = TestClient(app)


def test_create_and_list_items() -> None:
    created = client.post("/items", json={"name": "probe", "description": "canary"})
    assert created.status_code == 201
    body = created.json()
    listed = client.get("/items")
    assert listed.status_code == 200
    assert any(item["id"] == body["id"] for item in listed.json())


def test_delete_missing_item() -> None:
    response = client.delete("/items/does-not-exist")
    assert response.status_code == 404
