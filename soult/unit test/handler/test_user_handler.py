import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
from unittest.mock import patch
import handler.user_handler as handler

@pytest.fixture
def mock_db():
    with patch("handler.user_handler.db") as mock:
        yield mock

@pytest.fixture
def mock_validator():
    with patch("handler.user_handler.validator.validate") as mock:
        yield mock

@pytest.fixture
def mock_build_response():
    with patch("handler.user_handler.build_response") as mock:
        yield mock

@pytest.fixture
def mock_cognito():
    with patch("handler.user_handler.create_cognito_id") as mock:
        yield mock

@pytest.fixture
def mock_event_decorator():
    with patch("utils.sns_utils.event", lambda *args, **kwargs: lambda func: func):
        yield

# Test User Creation
def test_create_user_success(mock_db, mock_validator, mock_build_response, mock_cognito, mock_event_decorator):
    user_data = {"firstname": "john", "lastname": "doe", "phone_no": "1234567890", "email": "john.doe@example.com",
                 "mpin": "1234"}
    mock_validator.return_value = user_data
    mock_cognito.return_value = "69c5ed6f35a24794bf9c1d9804e8d742"
    mock_db.create_user.return_value = {"status": "User created successfully"}
    mock_build_response.return_value = {"statusCode": 200, "body": "Success"}
    response = handler.create(user_data)
    mock_validator.assert_called_once_with(user_data)
    mock_cognito.assert_called_once()
    mock_db.create_user.assert_called_once()
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "Success"}

def test_create_user_validation_error(mock_db, mock_validator, mock_build_response, mock_event_decorator):
    user_data = {"firstname": "john", "lastname": "doe", "phone_no": "", "email": "invalid_email"}  # Invalid data
    mock_validator.return_value = {"errors": ["Invalid email"]}
    mock_build_response.return_value = {"statusCode": 400, "body": "Invalid email"}
    response = handler.create(user_data)
    mock_validator.assert_called_once_with(user_data)
    mock_db.create_user.assert_not_called()
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 400, "body": "Invalid email"}

# Test User Update
def test_update_user_success(mock_db, mock_validator, mock_build_response, mock_event_decorator):
    user_id = "69c5ed6f35a24794bf9c1d9804e8d742"
    updated_data = {"firstname": "john", "lastname": "doe", "phone_no": "1234567890", "email": "john.doe@example.com"}
    mock_validator.return_value = updated_data
    mock_db.update_user.return_value = updated_data
    mock_build_response.return_value = {"statusCode": 200, "body": "Update Success"}
    response = handler.update(user_id, updated_data)
    mock_validator.assert_called_once_with(updated_data)
    mock_db.update_user.assert_called_once()
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "Update Success"}

def test_update_user_validation_error(mock_db, mock_validator, mock_build_response, mock_event_decorator):
    user_id = "69c5ed6f35a24794bf9c1d9804e8d742"
    updated_data = {"firstname": "", "lastname": "", "phone_no": "", "email": "invalid_email"}  # Invalid data
    mock_validator.return_value = {"errors": ["Invalid email"]}
    mock_build_response.return_value = {"statusCode": 400, "body": "Invalid email"}
    response = handler.update(user_id, updated_data)
    mock_validator.assert_called_once_with(updated_data)
    mock_db.update_user.assert_not_called()
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 400, "body": "Invalid email"}

# Test User Deletion
def test_delete_user_success(mock_db, mock_build_response):
    user_id = "69c5ed6f35a24794bf9c1d9804e8d742"
    model_id = "USER"
    mock_db.delete_user.return_value = {"message": "User deleted successfully"}
    mock_build_response.return_value = {"statusCode": 200, "body": "Deleted successfully"}
    response = handler.delete(user_id, model_id)
    mock_db.delete_user.assert_called_once_with(user_id, model_id)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "Deleted successfully"}

# Test Finding Users
def test_find_user_success(mock_db, mock_build_response):
    user_id = "69c5ed6f35a24794bf9c1d9804e8d742"
    mock_db.find_user.return_value = {"id": user_id, "firstname": "John", "lastname": "Doe"}
    mock_build_response.return_value = {"statusCode": 200, "body": "User Found"}
    response = handler.find(user_id)
    mock_db.find_user.assert_called_once_with(user_id)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "User Found"}

def test_find_phone_success(mock_db, mock_build_response):
    phone_number = "1234567890"
    mock_db.find_phone.return_value = True
    mock_build_response.return_value = {"statusCode": 200, "body": "Phone Exists"}
    response = handler.find_phone(phone_number)
    mock_db.find_phone.assert_called_once_with(phone_number)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "Phone Exists"}


def test_find_email_success(mock_db, mock_build_response):
    email = "john.doe@example.com"
    mock_db.find_email.return_value = True
    mock_build_response.return_value = {"statusCode": 200, "body": "Email Exists"}
    response = handler.find_email(email)
    mock_db.find_email.assert_called_once_with(email)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "Email Exists"}

# Test Cognito Validation
def test_validate_user_success(mock_build_response):
    user_id = "69c5ed6f35a24794bf9c1d9804e8d742"
    with patch("handler.user_handler.validate_cognito_user") as mock_validate_cognito:
        mock_validate_cognito.return_value = {"valid": True}
        mock_build_response.return_value = {"statusCode": 200, "body": "Valid User"}
        response = handler.validate(user_id)
        mock_validate_cognito.assert_called_once_with(user_id)
        mock_build_response.assert_called_once()
        assert response == {"statusCode": 200, "body": "Valid User"}
