import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from datetime import datetime
import pytest
from unittest.mock import MagicMock, patch
import dao.financial_asset_dao as financial_asset_dao

USER_ID = "test-user"
FAKE_ASSET_ID = "asset-123"
FAKE_ASSET = {
    "id": FAKE_ASSET_ID,
    "name": "Stocks",
    "value": 5000,
    "created_at": "2025-02-25 10:00:00"
}
UPDATED_ASSET = {
    "name": "Updated Stocks",
    "value": 6000
}
FAKE_ASSET_UPDATED = {**FAKE_ASSET, **UPDATED_ASSET, "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

@pytest.fixture
def mock_dynamodb():
    """Mock DynamoDB resource and table."""
    with patch("boto3.resource") as mock_boto3:
        mock_dynamodb = MagicMock()
        mock_table = MagicMock()
        mock_boto3.return_value = mock_dynamodb
        mock_dynamodb.Table.return_value = mock_table
        yield mock_table

@pytest.fixture
def mock_decorators():
    """Mocks decorators to allow direct function execution."""
    with patch("dao.financial_asset_dao.with_connection", lambda func: func), \
            patch("dao.financial_asset_dao.audit_log", lambda *args, **kwargs: lambda func: func):
        yield

@pytest.fixture
def mock_get_user_by_projection():
    """Mock get_user_by_projection to return financial assets."""
    with patch("dao.financial_asset_dao.get_user_by_projection") as mock:
        yield mock

# ---- Test Create ----
def test_create_financial_asset(mock_dynamodb, mock_decorators):
    mock_dynamodb.update_item.return_value = {"Attributes": FAKE_ASSET}
    response = financial_asset_dao.create(USER_ID, FAKE_ASSET)
    assert response["name"] == FAKE_ASSET["name"]
    assert response["value"] == FAKE_ASSET["value"]
    assert "id" in response
    assert "created_at" in response
    assert response.get("status") is True

# ---- Test Update ----
def test_update_financial_asset(mock_dynamodb, mock_decorators, mock_get_user_by_projection):
    mock_get_user_by_projection.return_value = [FAKE_ASSET]
    mock_dynamodb.update_item.return_value = {"Attributes": FAKE_ASSET_UPDATED}
    response = financial_asset_dao.update(USER_ID, FAKE_ASSET_ID, UPDATED_ASSET)
    assert response == FAKE_ASSET_UPDATED

# ---- Test Delete ----
def test_delete_financial_asset(mock_dynamodb, mock_decorators, mock_get_user_by_projection):
    mock_get_user_by_projection.return_value = [FAKE_ASSET]
    mock_dynamodb.update_item.return_value = {}
    response = financial_asset_dao.delete(USER_ID, FAKE_ASSET_ID)
    assert response == {"message": "Financial Asset deleted", "user_id": USER_ID, "id": FAKE_ASSET_ID}

# ---- Test Find ----
def test_find_financial_asset(mock_decorators, mock_get_user_by_projection):
    mock_get_user_by_projection.return_value = [FAKE_ASSET]
    response = financial_asset_dao.find(USER_ID, FAKE_ASSET_ID)
    assert response == FAKE_ASSET

def test_find_financial_asset_not_found(mock_decorators, mock_get_user_by_projection):
    mock_get_user_by_projection.return_value = []
    with pytest.raises(ValueError, match=f"No assets found for user with ID '{USER_ID}'."):
        financial_asset_dao.find(USER_ID, FAKE_ASSET_ID)

# ---- Test Find All ----
def test_find_all_financial_assets(mock_decorators, mock_get_user_by_projection):
    mock_get_user_by_projection.return_value = [FAKE_ASSET]
    response = financial_asset_dao.find_all(USER_ID)
    assert response == [FAKE_ASSET]

def test_find_all_no_assets(mock_decorators, mock_get_user_by_projection):
    mock_get_user_by_projection.return_value = []

    with pytest.raises(ValueError, match="No Financial Asset found for user."):
        financial_asset_dao.find_all(USER_ID)
