"""Tests for the todo REST endpoints. Verifies HTTP request handling, response formats, and status codes."""

import json


def test_list_todos_empty(client):
    response = client.get("/api/todos")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_todo(client):
    response = client.post(
        "/api/todos",
        data=json.dumps({"title": "Buy milk"}),
        content_type="application/json",
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Buy milk"
    assert data["completed"] is False
    assert "id" in data


def test_create_todo_missing_title(client):
    response = client.post(
        "/api/todos",
        data=json.dumps({}),
        content_type="application/json",
    )
    assert response.status_code == 400


def test_create_todo_blank_title(client):
    response = client.post(
        "/api/todos",
        data=json.dumps({"title": "   "}),
        content_type="application/json",
    )
    assert response.status_code == 400


def test_create_todo_no_body(client):
    response = client.post("/api/todos", content_type="application/json")
    assert response.status_code == 400


def test_list_todos_after_create(client):
    client.post(
        "/api/todos",
        data=json.dumps({"title": "First"}),
        content_type="application/json",
    )
    client.post(
        "/api/todos",
        data=json.dumps({"title": "Second"}),
        content_type="application/json",
    )
    response = client.get("/api/todos")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2


def test_get_todo(client):
    create_resp = client.post(
        "/api/todos",
        data=json.dumps({"title": "Get me"}),
        content_type="application/json",
    )
    todo_id = create_resp.get_json()["id"]

    response = client.get(f"/api/todos/{todo_id}")
    assert response.status_code == 200
    assert response.get_json()["title"] == "Get me"


def test_get_todo_not_found(client):
    response = client.get("/api/todos/999")
    assert response.status_code == 404
    assert "error" in response.get_json()


def test_toggle_todo(client):
    create_resp = client.post(
        "/api/todos",
        data=json.dumps({"title": "Toggle me"}),
        content_type="application/json",
    )
    todo_id = create_resp.get_json()["id"]

    response = client.patch(f"/api/todos/{todo_id}")
    assert response.status_code == 200
    assert response.get_json()["completed"] is True

    response = client.patch(f"/api/todos/{todo_id}")
    assert response.status_code == 200
    assert response.get_json()["completed"] is False


def test_toggle_todo_not_found(client):
    response = client.patch("/api/todos/999")
    assert response.status_code == 404


def test_delete_todo(client):
    create_resp = client.post(
        "/api/todos",
        data=json.dumps({"title": "Delete me"}),
        content_type="application/json",
    )
    todo_id = create_resp.get_json()["id"]

    response = client.delete(f"/api/todos/{todo_id}")
    assert response.status_code == 204

    response = client.get(f"/api/todos/{todo_id}")
    assert response.status_code == 404


def test_delete_todo_not_found(client):
    response = client.delete("/api/todos/999")
    assert response.status_code == 404
