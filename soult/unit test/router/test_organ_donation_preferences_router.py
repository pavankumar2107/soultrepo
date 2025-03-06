from fastapi.testclient import TestClient
from unittest.mock import patch
from router.organ_donation_preferences_router import router

client = TestClient(router)

@patch("handler.organ_donation_preferences_handler.find")
def test_get_organ_donation_preference_success(mock_find):
    mock_find.return_value = {"id": "1", "preference": "Donate all organs"}
    response = client.get("/user/123/organ_donation/1")
    assert response.status_code == 200
    assert response.json() == {"id": "1", "preference": "Donate all organs"}


@patch("handler.organ_donation_preferences_handler.find_all")
def test_get_all_organ_donation_preferences_success(mock_find_all):
    mock_find_all.return_value = [{"id": "1", "preference": "Donate all organs"}]
    response = client.get("/user/123/organ_donation/")
    assert response.status_code == 200
    assert response.json() == [{"id": "1", "preference": "Donate all organs"}]


@patch("handler.organ_donation_preferences_handler.create")
def test_create_organ_donation_preference_success(mock_create):
    mock_create.return_value = {"id": "1", "preference": "Donate all organs"}
    response = client.post("/user/123/organ_donation/", json={"preference": "Donate all organs"})
    assert response.status_code == 200
    assert response.json() == {"id": "1", "preference": "Donate all organs"}

@patch("handler.organ_donation_preferences_handler.update")
def test_update_organ_donation_preference_success(mock_update):
    mock_update.return_value = {"id": "1", "preference": "Donate specific organs"}
    response = client.put("/user/123/organ_donation/1", json={"preference": "Donate specific organs"})
    assert response.status_code == 200
    assert response.json() == {"id": "1", "preference": "Donate specific organs"}



@patch("handler.organ_donation_preferences_handler.delete")
def test_delete_organ_donation_preference_success(mock_delete):
    mock_delete.return_value = {"message": "Deleted successfully"}
    response = client.delete("/user/123/organ_donation/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Deleted successfully"}


