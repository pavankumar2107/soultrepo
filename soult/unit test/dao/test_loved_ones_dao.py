import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from datetime import datetime
import pytest
from unittest.mock import MagicMock, patch
import dao.loved_ones_dao as loved_ones_dao

# Sample User ID
USER_ID = "123"

# Sample Loved One ID
FAKE_LOVED_ONE_ID = "71bb784eb11d4d30bd7062b75311f4f3"

# Sample Loved One Data
FAKE_LOVED_ONE = {
    "id": FAKE_LOVED_ONE_ID,
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
    "aadhar": "7890 7655 3421",
    "created_at": "2025-01-10T11:00:00Z",
    "updated_at": "2025-01-20T15:00:00Z"
}

# Updated Loved One Data
UPDATED_LOVED_ONE = {
    "phone_no": "1234567890",
    "email": "jane.new@example.com",
    "address": "456 Oak Street, Springfield"
}

# Expected Updated Loved One Data
FAKE_LOVED_ONE_UPDATED = {**FAKE_LOVED_ONE, **UPDATED_LOVED_ONE, "updated_at": datetime.now().isoformat()}


@pytest.fixture
def mock_dynamodb():
    """Mock DynamoDB Table"""
    with patch("boto3.resource") as mock_boto3:
        mock_dynamodb = MagicMock()
        mock_table = MagicMock()
        mock_boto3.return_value = mock_dynamodb
        mock_dynamodb.Table.return_value = mock_table
        yield mock_table


@pytest.fixture
def mock_decorators():
    """Mock decorators to avoid actual database operations"""
    with patch("dao.loved_ones_dao.with_connection", lambda func: func), \
            patch("dao.loved_ones_dao.audit_log", lambda *args, **kwargs: lambda func: func):
        yield


@pytest.fixture
def mock_get_user_by_projection():
    """Mock the get_user_by_projection function"""
    with patch("dao.loved_ones_dao.get_user_by_projection") as mock:
        yield mock


def test_create_loved_one(mock_dynamodb, mock_decorators):
    mock_dynamodb.update_item.return_value = {"Attributes": FAKE_LOVED_ONE}
    response= loved_ones_dao.create(USER_ID, FAKE_LOVED_ONE)

    assert response["firstname"] == FAKE_LOVED_ONE["firstname"]
    assert response["lastname"] == FAKE_LOVED_ONE["lastname"]
    assert response["relationship"] == FAKE_LOVED_ONE["relationship"]
    assert "id" in response
    assert "created_at" in response


def test_update_loved_one(mock_dynamodb, mock_decorators, mock_get_user_by_projection):
    """Test updating a loved one"""
    mock_get_user_by_projection.return_value = [FAKE_LOVED_ONE]
    mock_dynamodb.update_item.return_value = {"Attributes": FAKE_LOVED_ONE_UPDATED}
    response= loved_ones_dao.update(USER_ID, FAKE_LOVED_ONE_ID, UPDATED_LOVED_ONE)
    assert response["phone_no"] == UPDATED_LOVED_ONE["phone_no"]
    assert response["email"] == UPDATED_LOVED_ONE["email"]
    assert response["address"] == UPDATED_LOVED_ONE["address"]
    assert "updated_at" in response


def test_delete_loved_one(mock_dynamodb, mock_decorators, mock_get_user_by_projection):
    mock_get_user_by_projection.return_value = [FAKE_LOVED_ONE]
    mock_dynamodb.update_item.return_value = {}
    response = loved_ones_dao.delete(USER_ID, FAKE_LOVED_ONE_ID)
    assert response == {"Message": "loved one deleted", "user_id": USER_ID, "id": FAKE_LOVED_ONE_ID}


def test_find_loved_one(mock_decorators, mock_get_user_by_projection):
    mock_get_user_by_projection.return_value = [FAKE_LOVED_ONE]
    response = loved_ones_dao.find(USER_ID, FAKE_LOVED_ONE_ID)
    assert response == FAKE_LOVED_ONE


def test_find_loved_one_not_found(mock_decorators, mock_get_user_by_projection):
    mock_get_user_by_projection.return_value = []
    with pytest.raises(ValueError, match=f"Loved One not found with ID: {FAKE_LOVED_ONE_ID}"):
        loved_ones_dao.find(USER_ID, FAKE_LOVED_ONE_ID)


def test_find_all_loved_ones(mock_decorators, mock_get_user_by_projection):
    mock_get_user_by_projection.return_value = [FAKE_LOVED_ONE]
    response = loved_ones_dao.find_all(USER_ID)
    assert response == [FAKE_LOVED_ONE]


def test_find_all_no_loved_ones(mock_decorators, mock_get_user_by_projection):
    mock_get_user_by_projection.return_value = []
    with pytest.raises(ValueError, match="No Loved One found for user"):
        loved_ones_dao.find_all(USER_ID)
