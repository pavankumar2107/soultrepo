import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from datetime import datetime
import pytest
from unittest.mock import MagicMock, patch
import dao.organ_donation_preferences_dao as organ_donation_preferences_dao

# Sample User ID
USER_ID = "123"

# Sample Organ Donation Preference ID
FAKE_ODP_ID = "8dab5fd2f2e840b68b2ab413772062ba"

# Sample Organ Donation Preference Data
FAKE_ODP = {
    "id": FAKE_ODP_ID,
    "organ": "Kidney",
    "additional_conditions": "Only for emergency cases",
    "created_at": "2025-01-10T11:00:00Z",
    "updated_at": "2025-01-20T15:00:00Z",
    "status": True
}

# Updated Organ Donation Preference Data
UPDATED_ODP = {
    "organ": "Liver",
    "additional_conditions": "No restrictions",
    "status": False
}

FAKE_ODP_UPDATED = {**FAKE_ODP, **UPDATED_ODP, "updated_at": datetime.now().isoformat()}


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
    with patch("dao.organ_donation_preferences_dao.with_connection", lambda func: func), \
            patch("dao.organ_donation_preferences_dao.audit_log", lambda *args, **kwargs: lambda func: func):
        yield

@pytest.fixture
def mock_get_user_by_projection():
    with patch("dao.organ_donation_preferences_dao.get_user_by_projection") as mock:
        yield mock

def test_create_organ_donation_preference(mock_dynamodb, mock_decorators):
    mock_dynamodb.update_item.return_value = {"Attributes": FAKE_ODP}
    response= organ_donation_preferences_dao.create(USER_ID, FAKE_ODP)
    assert response["organ"] == FAKE_ODP["organ"]
    assert response["additional_conditions"] == FAKE_ODP["additional_conditions"]
    assert response["status"] is True
    assert "id" in response
    assert "created_at" in response

def test_update_organ_donation_preference(mock_dynamodb, mock_decorators, mock_get_user_by_projection):
    mock_get_user_by_projection.return_value = [FAKE_ODP]
    mock_dynamodb.update_item.return_value = {"Attributes": FAKE_ODP_UPDATED}
    response = organ_donation_preferences_dao.update(USER_ID, FAKE_ODP_ID, UPDATED_ODP)
    assert response["organ"] == UPDATED_ODP["organ"]
    assert response["additional_conditions"] == UPDATED_ODP["additional_conditions"]
    assert response["status"] is False
    assert "updated_at" in response

def test_delete_organ_donation_preference(mock_dynamodb, mock_decorators, mock_get_user_by_projection):
    mock_get_user_by_projection.return_value = [FAKE_ODP]
    mock_dynamodb.update_item.return_value = {}
    response = organ_donation_preferences_dao.delete(USER_ID, FAKE_ODP_ID)
    assert response == {"message": "Organ donation preference deleted", "user_id": USER_ID, "id": FAKE_ODP_ID}

def test_find_organ_donation_preference(mock_decorators, mock_get_user_by_projection):
    mock_get_user_by_projection.return_value = [FAKE_ODP]
    response = organ_donation_preferences_dao.find(USER_ID, FAKE_ODP_ID)
    assert response == FAKE_ODP

def test_find_organ_donation_preference_not_found(mock_decorators, mock_get_user_by_projection):
    mock_get_user_by_projection.return_value = []
    with pytest.raises(ValueError, match=f"Organ donation preference not found with ID: {FAKE_ODP_ID}"):
        organ_donation_preferences_dao.find(USER_ID, FAKE_ODP_ID)

def test_find_all_organ_donation_preferences(mock_decorators, mock_get_user_by_projection):
    mock_get_user_by_projection.return_value = [FAKE_ODP]
    response = organ_donation_preferences_dao.find_all(USER_ID)
    assert response == [FAKE_ODP]

def test_find_all_no_organ_donation_preferences(mock_decorators, mock_get_user_by_projection):
    mock_get_user_by_projection.return_value = []
    with pytest.raises(ValueError, match=f"No Organ donation preference for user with ID: {USER_ID}"):
        organ_donation_preferences_dao.find_all(USER_ID)
