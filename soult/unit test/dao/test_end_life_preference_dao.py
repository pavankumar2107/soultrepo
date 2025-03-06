import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch
import dao.end_life_preference_dao as end_life_preference_dao

# Sample User ID
USER_ID = "123"

# Sample End-of-Life Preferences Data
FAKE_ELP = {
    "resuscitation": "No",
    "decision_maker": {
        "type": "loved_one",
        "id": "3fbfd18f456b450bbe16d1fa83b59324"
    },
    "condition_for_withdrawal": "Brain Death",
    "duration_of_support": 5,
    "ventilator": "Yes",
    "status": True,
    "updated_at": "2025-01-20T15:00:00Z",
    "created_at": "2025-01-01T10:00:00Z"
}

# Updated Data for End-of-Life Preferences
UPDATED_ELP = {
    "resuscitation": "Yes",
    "duration_of_support": 3,
    "status": False
}

FAKE_ELP_UPDATED = {**FAKE_ELP, **UPDATED_ELP, "updated_at": datetime.now().isoformat()}


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
    with patch("dao.end_life_preference_dao.with_connection", lambda func: func), \
            patch("dao.end_life_preference_dao.audit_log", lambda *args, **kwargs: lambda func: func):
        yield


def test_create_end_life_preferences(mock_dynamodb, mock_decorators):
    mock_dynamodb.update_item.return_value = {"Attributes": FAKE_ELP}
    response= end_life_preference_dao.create(USER_ID, FAKE_ELP)
    assert response["resuscitation"] == FAKE_ELP["resuscitation"]
    assert response["decision_maker"]["id"] == FAKE_ELP["decision_maker"]["id"]
    assert response["duration_of_support"] == FAKE_ELP["duration_of_support"]
    assert response["status"] is True
    assert "created_at" in response

def test_update_end_life_preferences(mock_dynamodb, mock_decorators):
    mock_dynamodb.get_item.return_value = {"Item": {"end_life_preferences": FAKE_ELP}}
    mock_dynamodb.update_item.return_value = {"Attributes": FAKE_ELP_UPDATED}
    response = end_life_preference_dao.update(USER_ID, UPDATED_ELP)
    assert response["resuscitation"] == UPDATED_ELP["resuscitation"]
    assert response["duration_of_support"] == UPDATED_ELP["duration_of_support"]
    assert response["status"] is False
    assert "updated_at" in response


def test_delete_end_life_preferences(mock_dynamodb, mock_decorators):
    mock_dynamodb.get_item.return_value = {"Item": {"end_life_preferences": FAKE_ELP}}
    mock_dynamodb.update_item.return_value = {}
    response= end_life_preference_dao.delete(USER_ID, "elp_id")
    assert response == {"message": "End life preference deleted", "user_id": USER_ID}


def test_find_end_life_preferences(mock_dynamodb, mock_decorators):
    mock_dynamodb.get_item.return_value = {"Item": {"end_life_preferences": FAKE_ELP}}
    response = end_life_preference_dao.find(USER_ID)
    assert response == FAKE_ELP


