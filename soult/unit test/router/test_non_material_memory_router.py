from fastapi.testclient import TestClient
from unittest.mock import patch
from router.non_material_memories_router import router

client = TestClient(router)

@patch("handler.non_material_memories_handler.find")
def test_get_non_material_memory_success(mock_find):
    mock_find.return_value = {"id": "nm123", "title": "Memory 1"}
    response = client.get("/user/123/non_material_memory/nm123")
    assert response.status_code == 200
    assert response.json() == {"id": "nm123", "title": "Memory 1"}
    mock_find.assert_called_once_with("123", "nm123")

@patch("handler.non_material_memories_handler.find_all")
def test_get_all_non_material_memories_success(mock_find_all):
    mock_find_all.return_value = [{"id": "nm123", "title": "Memory 1"}]
    response = client.get("/user/123/non_material_memory/")
    assert response.status_code == 200
    assert response.json() == [{"id": "nm123", "title": "Memory 1"}]
    mock_find_all.assert_called_once_with("123")

@patch("handler.non_material_memories_handler.create")
def test_create_non_material_memory_success(mock_create):
    mock_create.return_value = {"id": "nm123", "title": "New Memory"}
    response = client.post("/user/123/non_material_memory/", json={"title": "New Memory"})
    assert response.status_code == 200
    assert response.json() == {"id": "nm123", "title": "New Memory"}
    mock_create.assert_called_once_with("123", {"title": "New Memory"})

@patch("handler.non_material_memories_handler.update")
def test_update_non_material_memory_success(mock_update):
    mock_update.return_value = {"id": "nm123", "title": "Updated Memory"}
    response = client.put("/user/123/non_material_memory/nm123", json={"title": "Updated Memory"})
    assert response.status_code == 200
    assert response.json() == {"id": "nm123", "title": "Updated Memory"}
    mock_update.assert_called_once_with("123", "nm123", {"title": "Updated Memory"})

@patch("handler.non_material_memories_handler.delete")
def test_delete_non_material_memory_success(mock_delete):
    mock_delete.return_value = {"message": "Non-material memory deleted"}
    response = client.delete("/user/123/non_material_memory/nm123")
    assert response.status_code == 200
    assert response.json() == {"message": "Non-material memory deleted"}
    mock_delete.assert_called_once_with("123", "nm123")


