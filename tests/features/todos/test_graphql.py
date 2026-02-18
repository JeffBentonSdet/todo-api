"""Tests for the todo GraphQL interface. Verifies query and mutation resolvers produce correct results."""

import json


def _query(client, query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    return client.post(
        "/graphql",
        data=json.dumps(payload),
        content_type="application/json",
    )


# Queries

def test_todos_query_empty(client):
    response = _query(client, "{ todos { id title completed } }")
    assert response.status_code == 200
    data = response.get_json()
    assert data["data"]["todos"] == []


def test_todos_query_after_create(client):
    _query(client, 'mutation { createTodo(title: "First") { id } }')
    _query(client, 'mutation { createTodo(title: "Second") { id } }')

    response = _query(client, "{ todos { id title completed } }")
    data = response.get_json()
    assert len(data["data"]["todos"]) == 2


def test_todo_query(client):
    create_resp = _query(client, 'mutation { createTodo(title: "Find me") { id } }')
    todo_id = create_resp.get_json()["data"]["createTodo"]["id"]

    response = _query(client, "query($id: ID!) { todo(id: $id) { id title completed createdAt updatedAt } }", {"id": todo_id})
    data = response.get_json()
    assert data["data"]["todo"]["title"] == "Find me"
    assert data["data"]["todo"]["completed"] is False
    assert data["data"]["todo"]["createdAt"] is not None


def test_todo_query_not_found(client):
    response = _query(client, '{ todo(id: "999") { id title } }')
    data = response.get_json()
    assert data.get("errors") is not None


# Mutations

def test_create_todo_mutation(client):
    response = _query(client, 'mutation { createTodo(title: "New todo") { id title completed } }')
    assert response.status_code == 200
    data = response.get_json()
    todo = data["data"]["createTodo"]
    assert todo["title"] == "New todo"
    assert todo["completed"] is False
    assert todo["id"] is not None


def test_create_todo_blank_title(client):
    response = _query(client, 'mutation { createTodo(title: "   ") { id } }')
    data = response.get_json()
    assert data.get("errors") is not None


def test_toggle_todo_mutation(client):
    create_resp = _query(client, 'mutation { createTodo(title: "Toggle me") { id } }')
    todo_id = create_resp.get_json()["data"]["createTodo"]["id"]

    response = _query(client, "mutation($id: ID!) { toggleTodo(id: $id) { id completed } }", {"id": todo_id})
    data = response.get_json()
    assert data["data"]["toggleTodo"]["completed"] is True

    response = _query(client, "mutation($id: ID!) { toggleTodo(id: $id) { id completed } }", {"id": todo_id})
    data = response.get_json()
    assert data["data"]["toggleTodo"]["completed"] is False


def test_toggle_todo_not_found(client):
    response = _query(client, 'mutation { toggleTodo(id: "999") { id } }')
    data = response.get_json()
    assert data.get("errors") is not None


def test_delete_todo_mutation(client):
    create_resp = _query(client, 'mutation { createTodo(title: "Delete me") { id } }')
    todo_id = create_resp.get_json()["data"]["createTodo"]["id"]

    response = _query(client, "mutation($id: ID!) { deleteTodo(id: $id) { success } }", {"id": todo_id})
    data = response.get_json()
    assert data["data"]["deleteTodo"]["success"] is True

    # Verify it's gone
    response = _query(client, "query($id: ID!) { todo(id: $id) { id } }", {"id": todo_id})
    data = response.get_json()
    assert data.get("errors") is not None


def test_delete_todo_not_found(client):
    response = _query(client, 'mutation { deleteTodo(id: "999") { success } }')
    data = response.get_json()
    assert data.get("errors") is not None
