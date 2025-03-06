import pytest
from unittest.mock import patch
import handler.loved_ones_handler as handler
# Sample loved ones dataset
loved_ones_data = {
    "id": "71bb784eb11d4d30bd7062b75311f4f3",
    "firstname": "Jane",
    "lastname": "Doe",
    "maiden_name": "Jose",
    "relationship": "Brother",
    "role": "Primary Contact",
    "phone_no": "9876543210",
    "email": "jane.doe@example.com",
    "dob": "1990-01-01",
    "gender": "Female",
    "address": "123 Elm Street, Springfield",
    "aadhar": "7890 7655 3421"
}

@pytest.fixture
def mock_db():
    with patch("handler.loved_ones_handler.db") as mock:
        yield mock

@pytest.fixture
def mock_validator():
    with patch("handler.loved_ones_handler.validator.validate") as mock:
        yield mock


@pytest.fixture
def mock_build_response():
    with patch("handler.loved_ones_handler.build_response") as mock:
        yield mock


@pytest.fixture
def mock_event_decorator():
    with patch("utils.sns_utils.event", lambda *args, **kwargs: lambda func: func):
        yield


def test_create_loved_one_success(mock_db, mock_validator, mock_build_response, mock_event_decorator):
    user_id = "user123"
    mock_validator.return_value = loved_ones_data
    mock_db.create_loved_ones.return_value = {**loved_ones_data, "id": "loved_one123"}
    mock_build_response.return_value = {"statusCode": 200, "body": "Success"}
    response = handler.create(user_id, loved_ones_data)
    mock_validator.assert_called_once_with(loved_ones_data)
    mock_db.create_loved_ones.assert_called_once_with(user_id, loved_ones_data)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "Success"}


def test_create_loved_one_validation_error(mock_db, mock_validator, mock_build_response, mock_event_decorator):
    user_id = "user123"
    invalid_data = {"firstname": "", "lastname": "Doe"}  # Missing required fields
    mock_validator.return_value = {"errors": ["Invalid data"]}
    mock_build_response.return_value = {"statusCode": 400, "body": "Invalid data"}
    response = handler.create(user_id, invalid_data)
    mock_validator.assert_called_once_with(invalid_data)
    mock_db.create_loved_ones.assert_not_called()
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 400, "body": "Invalid data"}


def test_update_loved_one_success(mock_db, mock_validator, mock_build_response, mock_event_decorator):
    user_id = "user123"
    loved_one_id = "loved_one123"
    updated_data = {**loved_ones_data, "relationship": "Sister"}
    mock_validator.return_value = updated_data
    mock_db.update_loved_ones.return_value = updated_data
    mock_build_response.return_value = {"statusCode": 200, "body": "Update Success"}
    response = handler.update(user_id, loved_one_id, updated_data)
    mock_validator.assert_called_once_with(updated_data)
    mock_db.update_loved_ones.assert_called_once_with(user_id, loved_one_id, updated_data)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "Update Success"}


def test_update_loved_one_validation_error(mock_db, mock_validator, mock_build_response, mock_event_decorator):
    user_id = "user123"
    loved_one_id = "loved_one123"
    invalid_data = {**loved_ones_data, "phone_no": "invalid_phone"}  # Invalid phone format
    mock_validator.return_value = {"errors": ["Invalid phone number"]}
    mock_build_response.return_value = {"statusCode": 400, "body": "Invalid phone number"}
    response = handler.update(user_id, loved_one_id, invalid_data)
    mock_validator.assert_called_once_with(invalid_data)
    mock_db.update_loved_ones.assert_not_called()
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 400, "body": "Invalid phone number"}


def test_delete_loved_one_success(mock_db, mock_build_response):
    user_id = "user123"
    loved_one_id = "loved_one789"
    mock_db.delete_loved_ones.return_value = {"message": "Deleted successfully"}
    mock_build_response.return_value = {"statusCode": 200, "body": "Deleted successfully"}
    response = handler.delete(user_id, loved_one_id)
    mock_db.delete_loved_ones.assert_called_once_with(user_id, loved_one_id)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "Deleted successfully"}


def test_find_loved_one_success(mock_db, mock_build_response):
    user_id = "user123"
    loved_one_id = "loved_one456"
    mock_db.find_loved_ones.return_value = {**loved_ones_data, "id": loved_one_id}
    mock_build_response.return_value = {"statusCode": 200, "body": "Loved One Found"}
    response = handler.find(user_id, loved_one_id)
    mock_db.find_loved_ones.assert_called_once_with(user_id, loved_one_id)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "Loved One Found"}


def test_find_all_loved_ones_success(mock_db, mock_build_response):
    user_id = "user123"
    mock_db.find_all_loved_ones.return_value = [
        loved_ones_data,
        {"id": "loved_one2", "firstname": "John", "lastname": "Doe"}
    ]
    mock_build_response.return_value = {"statusCode": 200, "body": "Loved Ones Found"}
    response = handler.find_all(user_id)
    mock_db.find_all_loved_ones.assert_called_once_with(user_id)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "Loved Ones Found"}
