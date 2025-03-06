import pytest
from unittest.mock import patch
import handler.organ_donation_preferences_handler as handler

# Sample organ donation preference dataset
organ_donation_data = {
    "id": "8dab5fd2f2e840b68b2ab413772062ba",
    "organ": "Kidney",
    "additional_conditions": "Only for emergency cases",
}

@pytest.fixture
def mock_db():
    with patch("handler.organ_donation_preferences_handler.db") as mock:
        yield mock

@pytest.fixture
def mock_validator():
    with patch("handler.organ_donation_preferences_handler.validator.validate") as mock:
        yield mock

@pytest.fixture
def mock_build_response():
    with patch("handler.organ_donation_preferences_handler.build_response") as mock:
        yield mock

@pytest.fixture
def mock_event_decorator():
    with patch("utils.sns_utils.event", lambda *args, **kwargs: lambda func: func):
        yield


def test_create_organ_donation_success(mock_db, mock_validator, mock_build_response, mock_event_decorator):
    user_id = "user123"
    mock_validator.return_value = organ_donation_data
    mock_db.create_organ_donation_preference.return_value = {**organ_donation_data, "id": "odp123"}
    mock_build_response.return_value = {"statusCode": 200, "body": "Success"}
    response = handler.create(user_id, organ_donation_data)
    mock_validator.assert_called_once_with(organ_donation_data)
    mock_db.create_organ_donation_preference.assert_called_once_with(user_id, organ_donation_data)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "Success"}


def test_create_organ_donation_validation_error(mock_db, mock_validator, mock_build_response, mock_event_decorator):
    user_id = "user123"
    invalid_data = {"organ": "Heart", "additional_conditions": 300}  # Invalid data
    mock_validator.return_value = {"errors": ["Invalid conditions"]}
    mock_build_response.return_value = {"statusCode": 400, "body": "Invalid conditions"}
    response = handler.create(user_id, invalid_data)
    mock_validator.assert_called_once_with(invalid_data)
    mock_db.create_organ_donation_preference.assert_not_called()
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 400, "body": "Invalid conditions"}


def test_update_organ_donation_success(mock_db, mock_validator, mock_build_response, mock_event_decorator):
    user_id = "user123"
    organ_donation_id = "odp456"
    updated_data = {**organ_donation_data, "additional_conditions": "Emergency cases only"}
    mock_validator.return_value = updated_data
    mock_db.update_organ_donation_preference.return_value = updated_data
    mock_build_response.return_value = {"statusCode": 200, "body": "Update Success"}
    response = handler.update(user_id, organ_donation_id, updated_data)
    mock_validator.assert_called_once_with(updated_data)
    mock_db.update_organ_donation_preference.assert_called_once_with(user_id, organ_donation_id, updated_data)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "Update Success"}


def test_delete_organ_donation_success(mock_db, mock_build_response):
    user_id = "user123"
    organ_donation_id = "odp789"
    mock_db.delete_organ_donation_preference.return_value = {"message": "Deleted successfully"}
    mock_build_response.return_value = {"statusCode": 200, "body": "Deleted successfully"}
    response = handler.delete(user_id, organ_donation_id)
    mock_db.delete_organ_donation_preference.assert_called_once_with(user_id, organ_donation_id)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "Deleted successfully"}


def test_find_organ_donation_success(mock_db, mock_build_response):
    user_id = "user123"
    organ_donation_id = "odp789"
    mock_db.find_organ_donation_preference.return_value = {**organ_donation_data, "id": organ_donation_id}
    mock_build_response.return_value = {"statusCode": 200, "body": "Preference Found"}
    response = handler.find(user_id, organ_donation_id)
    mock_db.find_organ_donation_preference.assert_called_once_with(user_id, organ_donation_id)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "Preference Found"}


def test_find_all_organ_donations_success(mock_db, mock_build_response):
    user_id = "user123"
    mock_db.find_all_organ_donation_preferences.return_value = [organ_donation_data,
                                                          {"id": "odp2", "organ": "Liver", "status": False}]
    mock_build_response.return_value = {"statusCode": 200, "body": "Preferences Found"}
    response = handler.find_all(user_id)
    mock_db.find_all_organ_donation_preferences.assert_called_once_with(user_id)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "Preferences Found"}
