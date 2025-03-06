from fastapi.testclient import TestClient
from unittest.mock import patch
from router.loved_ones_router import router
client = TestClient(router)

@patch("handler.loved_ones_handler.find")
def test_get_loved_one_success(mock_find):
    mock_find.return_value = {"id": "lo123", "name": "John Doe"}
    response = client.get("/user/123/loved_ones/lo123")
    assert response.status_code == 200
    assert response.json() == {"id": "lo123", "name": "John Doe"}
    mock_find.assert_called_once_with("123", "lo123")

@patch("handler.loved_ones_handler.find_all")
def test_get_all_loved_ones_success(mock_find_all):
    mock_find_all.return_value = [{"id": "lo123", "name": "John Doe"}]
    response = client.get("/user/123/loved_ones/")
    assert response.status_code == 200
    assert response.json() == [{"id": "lo123", "name": "John Doe"}]
    mock_find_all.assert_called_once_with("123")

@patch("handler.loved_ones_handler.create")
def test_create_loved_one_success(mock_create):
    mock_create.return_value = {"id": "lo123", "name": "Jane Doe"}
    response = client.post("/user/123/loved_ones/", json={"name": "Jane Doe"})
    assert response.status_code == 200
    assert response.json() == {"id": "lo123", "name": "Jane Doe"}
    mock_create.assert_called_once_with("123", {"name": "Jane Doe"})

@patch("handler.loved_ones_handler.update")
def test_update_loved_one_success(mock_update):
    mock_update.return_value = {"id": "lo123", "name": "Updated Name"}
    response = client.put("/user/123/loved_ones/lo123", json={"name": "Updated Name"})
    assert response.status_code == 200
    assert response.json() == {"id": "lo123", "name": "Updated Name"}
    mock_update.assert_called_once_with("123", "lo123", {"name": "Updated Name"})

@patch("handler.loved_ones_handler.delete")
def test_delete_loved_one_success(mock_delete):
    mock_delete.return_value = {"message": "Loved one deleted"}
    response = client.delete("/user/123/loved_ones/lo123")
    assert response.status_code == 200
    assert response.json() == {"message": "Loved one deleted"}
    mock_delete.assert_called_once_with("123", "lo123")
