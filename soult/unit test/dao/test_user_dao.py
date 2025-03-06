import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
from unittest.mock import patch, MagicMock
import dao.user_dao as user_dao

# Sample user data
user_data = {
    "id": "69c5ed6f35a24794bf9c1d9804e8d742",
    "firstname": "John",
    "lastname": "Doe",
    "phone_no": "1234567890",
    "email": "john.doe@example.com",
}


@pytest.fixture
def mock_dynamodb():
    with patch("boto3.resource") as mock_boto3:
        mock_dynamodb = MagicMock()
        mock_table = MagicMock()
        mock_boto3.return_value = mock_dynamodb
        mock_dynamodb.Table.return_value = mock_table
        yield mock_table


@pytest.fixture
def mock_decorators():
    """Mocks decorators to allow direct function execution."""
    with patch("dao.user_dao.with_connection", lambda func: func), \
            patch("dao.user_dao.audit_log", lambda *args, **kwargs: lambda func: func):
        yield

def test_create_user(mock_dynamodb, mock_decorators):
    user_id = user_data["id"]
    mock_dynamodb.put_item.return_value = {}
    response = user_dao.create(user_id, user_data)
    assert isinstance(response, dict)
    assert response == user_data


def test_delete_user(mock_dynamodb, mock_decorators):
    user_id = user_data["id"]
    table_mock = mock_dynamodb.Table.return_value
    table_mock.get_item.return_value = {"Item": user_data}
    table_mock.delete_item.return_value = {}
    response= user_dao.delete(user_id, "dummy_id")
    assert response == {"Message": "User deleted", "id": user_id}

def test_find_user(mock_dynamodb, mock_decorators):
    user_id = user_data["id"]
    mock_dynamodb.get_item.return_value = {"Item": user_data}
    response, _ = user_dao.find(user_id)
    assert response == user_data

def test_update_user(mock_dynamodb, mock_decorators):
    user_id = user_data["id"]
    updated_data = {"firstname": "Jane"}
    mock_dynamodb.get_item.return_value = {"Item": user_data}
    mock_dynamodb.update_item.return_value = {"Attributes": {**user_data, **updated_data}}
    response = user_dao.update(user_id, updated_data)
    assert response["firstname"] == "Jane"

def test_user_exists(mock_dynamodb, mock_decorators):
    user_id = user_data["id"]
    mock_dynamodb.get_item.return_value = {"Item": user_data}

    assert user_dao.user_exists(user_id) is True

def test_user_not_exists(mock_dynamodb, mock_decorators):
    user_id = "nonexistent"
    mock_dynamodb.get_item.return_value = {}
    assert user_dao.user_exists(user_id) is False

def test_get_user_details(mock_dynamodb, mock_decorators):
    user_id = user_data["id"]
    mock_dynamodb.get_item.return_value = {"Item": user_data}
    response = user_dao.get_user_details(user_id)
    expected = {
        "email": user_data["email"],
        "firstname": user_data["firstname"],
        "lastname": user_data["lastname"],
    }
    assert response == expected

def test_find_phone(mock_dynamodb, mock_decorators):
    phone_no = user_data["phone_no"]
    mock_dynamodb.query.return_value = {"Items": [user_data]}
    assert user_dao.find_phone(phone_no) is True

def test_find_phone_not_found(mock_dynamodb, mock_decorators):
    phone_no = "0000000000"
    mock_dynamodb.query.return_value = {"Items": []}
    assert user_dao.find_phone(phone_no) is False

def test_find_email(mock_dynamodb, mock_decorators):
    email = user_data["email"]
    mock_dynamodb.query.return_value = {"Items": [user_data]}
    assert user_dao.find_email(email) is True

def test_find_email_not_found(mock_dynamodb, mock_decorators):
    email = "unknown@example.com"
    mock_dynamodb.query.return_value = {"Items": []}
    assert user_dao.find_email(email) is False
