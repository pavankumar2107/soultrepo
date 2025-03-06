from fastapi.testclient import TestClient
from unittest.mock import patch
from router.user_router import router

client = TestClient(router)

@patch("handler.user_handler.find_phone")
def test_find_phone_success(mock_find_phone):
    mock_find_phone.return_value = True
    response = client.get("/user/phone?phone_number=1234567890")
    assert response.status_code == 200
    assert response.json() == {"exists": True}
    mock_find_phone.assert_called_once_with("1234567890")

@patch("handler.user_handler.find_phone")
def test_find_phone_not_found(mock_find_phone):
    mock_find_phone.return_value = False
    response = client.get("/user/phone?phone_number=9876543210")
    assert response.status_code == 200
    assert response.json() == {"exists": False}
    mock_find_phone.assert_called_once_with("9876543210")

@patch("handler.user_handler.find_email")
def test_find_email_success(mock_find_email):
    mock_find_email.return_value = True
    response = client.get("/user/email?email=test@example.com")
    assert response.status_code == 200
    assert response.json() == {"exists": True}
    mock_find_email.assert_called_once_with("test@example.com")

@patch("handler.user_handler.find")
def test_get_user_success(mock_find):
    mock_find.return_value = {"id": "123", "name": "Test User"}
    response = client.get("/user/123")
    assert response.status_code == 200
    assert response.json() == {"id": "123", "name": "Test User"}
    mock_find.assert_called_once_with("123")

@patch("handler.user_handler.validate")
def test_get_cognito_user_success(mock_validate):
    mock_validate.return_value = {"id": "123", "valid": True}
    response = client.get("/user/cognito/123")
    assert response.status_code == 200
    assert response.json() == {"id": "123", "valid": True}
    mock_validate.assert_called_once_with("123")

@patch("handler.user_handler.create")
def test_create_user_success(mock_create):
    mock_create.return_value = {"id": "123", "name": "New User"}
    response = client.post("/user/", json={"name": "New User"})
    assert response.status_code == 200
    assert response.json() == {"id": "123", "name": "New User"}
    mock_create.assert_called_once()

@patch("handler.user_handler.update")
def test_update_user_success(mock_update):
    mock_update.return_value = {"id": "123", "name": "Updated User"}
    response = client.put("/user/123", json={"name": "Updated User"})
    assert response.status_code == 200
    assert response.json() == {"id": "123", "name": "Updated User"}
    mock_update.assert_called_once_with("123", {"name": "Updated User"})

@patch("handler.user_handler.delete")
def test_delete_user_success(mock_delete):
    mock_delete.return_value = {"message": "User deleted"}
    response = client.delete("/user/123")
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted"}
    mock_delete.assert_called_once_with("123", model_id="user")

