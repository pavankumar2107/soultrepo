from fastapi.testclient import TestClient
from unittest.mock import patch
from router.end_life_preference_router import router
client = TestClient(router)

@patch("handler.end_life_preference_handler.find")
def test_get_end_life_preferences_success(mock_find):
    mock_find.return_value = {"id": "123", "preferences": "Sample Preferences"}
    response = client.get("/user/123/end_life_preferences/")
    assert response.status_code == 200
    assert response.json() == {"id": "123", "preferences": "Sample Preferences"}
    mock_find.assert_called_once_with("123")

@patch("handler.end_life_preference_handler.create")
def test_create_end_life_preferences_success(mock_create):
    mock_create.return_value = {"id": "123", "preferences": "New Preferences"}
    response = client.post("/user/123/end_life_preferences/", json={"preferences": "New Preferences"})
    assert response.status_code == 200
    assert response.json() == {"id": "123", "preferences": "New Preferences"}
    mock_create.assert_called_once_with("123", {"preferences": "New Preferences"})

@patch("handler.end_life_preference_handler.update")
def test_update_end_life_preferences_success(mock_update):
    mock_update.return_value = {"id": "123", "preferences": "Updated Preferences"}
    response = client.put("/user/123/end_life_preferences/", json={"preferences": "Updated Preferences"})
    assert response.status_code == 200
    assert response.json() == {"id": "123", "preferences": "Updated Preferences"}
    mock_update.assert_called_once_with("123", {"preferences": "Updated Preferences"})

@patch("handler.end_life_preference_handler.delete")
def test_delete_end_life_preferences_success(mock_delete):
    mock_delete.return_value = {"message": "End-of-life preferences deleted"}
    response = client.delete("/user/123/end_life_preferences/")
    assert response.status_code == 200
    assert response.json() == {"message": "End-of-life preferences deleted"}
    mock_delete.assert_called_once_with("123", end_life_preferences_id="")

