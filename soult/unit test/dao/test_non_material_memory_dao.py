import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from datetime import datetime
import pytest
from unittest.mock import MagicMock, patch
import dao.non_material_memory_dao as non_material_memory_dao

USER_ID = "123"
FAKE_MEMORY_ID = "3fc4720e9e5f4e0b9b7a48d355fca34d"
FAKE_MEMORY = {
    "id": FAKE_MEMORY_ID,
    "type": "Artwork",
    "details": "Painting by ABC",
    "memories": [
        {
            "type": "pdf",
            "document_arn": "s3 path"
        }
    ],
    "created_at": "2025-01-10T11:00:00Z",
    "updated_at": "2025-01-20T15:00:00Z",
    "status": True
}

UPDATED_MEMORY = {
    "details": "Updated Painting by ABC",
    "status": False
}

FAKE_MEMORY_UPDATED = {**FAKE_MEMORY, **UPDATED_MEMORY, "updated_at": datetime.now().isoformat()}

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
    with patch("dao.non_material_memory_dao.with_connection", lambda func: func), \
            patch("dao.non_material_memory_dao.audit_log", lambda *args, **kwargs: lambda func: func):
        yield

@pytest.fixture
def mock_get_user_by_projection():
    with patch("dao.non_material_memory_dao.get_user_by_projection") as mock:
        yield mock

def test_create_non_material_memory(mock_dynamodb, mock_decorators):
    mock_dynamodb.update_item.return_value = {"Attributes": FAKE_MEMORY}
    response= non_material_memory_dao.create(USER_ID, FAKE_MEMORY)
    assert response["type"] == FAKE_MEMORY["type"]
    assert response["details"] == FAKE_MEMORY["details"]
    assert response["memories"] == FAKE_MEMORY["memories"]
    assert "id" in response
    assert "created_at" in response
    assert response["status"] is True

def test_update_non_material_memory(mock_dynamodb, mock_decorators, mock_get_user_by_projection):
    mock_get_user_by_projection.return_value = [FAKE_MEMORY]
    mock_dynamodb.update_item.return_value = {"Attributes": FAKE_MEMORY_UPDATED}
    response = non_material_memory_dao.update(USER_ID, FAKE_MEMORY_ID, UPDATED_MEMORY)
    assert response["details"] == UPDATED_MEMORY["details"]
    assert response["status"] is False
    assert "updated_at" in response

def test_delete_non_material_memory(mock_dynamodb, mock_decorators, mock_get_user_by_projection):
    mock_get_user_by_projection.return_value = [FAKE_MEMORY]
    mock_dynamodb.update_item.return_value = {}
    response= non_material_memory_dao.delete(USER_ID, FAKE_MEMORY_ID)
    assert response == {"message": "Non Material Asset deleted", "user_id": USER_ID, "id": FAKE_MEMORY_ID}

def test_find_non_material_memory(mock_decorators, mock_get_user_by_projection):
    mock_get_user_by_projection.return_value = [FAKE_MEMORY]
    response = non_material_memory_dao.find(USER_ID, FAKE_MEMORY_ID)
    assert response == FAKE_MEMORY

def test_find_non_material_memory_not_found(mock_decorators, mock_get_user_by_projection):
    mock_get_user_by_projection.return_value = []
    with pytest.raises(ValueError, match=f"Non Material Assets Not Found For User With ID '{USER_ID}'."):
        non_material_memory_dao.find(USER_ID, FAKE_MEMORY_ID)

def test_find_all_non_material_memories(mock_decorators, mock_get_user_by_projection):
    mock_get_user_by_projection.return_value = [FAKE_MEMORY]
    response = non_material_memory_dao.find_all(USER_ID)
    assert response == [FAKE_MEMORY]

def test_find_all_no_non_material_memories(mock_decorators, mock_get_user_by_projection):
    mock_get_user_by_projection.return_value = []
    with pytest.raises(ValueError, match="Non Material Assets Not Found For User"):
        non_material_memory_dao.find_all(USER_ID)
