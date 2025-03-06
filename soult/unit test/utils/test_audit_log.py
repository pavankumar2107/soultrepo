import pytest
import datetime
from unittest.mock import MagicMock, patch
from utils.models import Operation, Model
from utils.audit_log import audit_log  # Adjust path if needed

# Sample dataset
sample_old_values = {
    "id": "8dab5fd2f2e840b68b2ab413772062ba",
    "organ": "Kidney",
    "additional_conditions": "Only for emergency cases",
    "created_at": "2025-01-10T11:00:00Z",
    "updated_at": "2025-01-20T15:00:00Z",
    "status": "Active"
}

sample_new_values = {
    "id": "8dab5fd2f2e840b68b2ab413772062ba",
    "organ": "Kidney",
    "additional_conditions": "Only for emergency cases",
    "created_at": "2025-01-10T11:00:00Z",
    "updated_at": "2025-01-20T15:00:00Z",
    "status": "Inactive"
}

@pytest.fixture
def mock_dynamodb():
    mock_dynamodb = MagicMock()
    mock_table = MagicMock()
    mock_dynamodb.Table.return_value = mock_table
    return mock_dynamodb, mock_table

@pytest.fixture
def mock_generate_uuid():
    with patch("utils.audit_log.generate_uuid", return_value="audit-log-1234"):
        yield

@pytest.fixture
def mock_datetime():
    with patch("datetime.datetime") as mock_datetime:
        mock_now = datetime.datetime(2025, 1, 20, 15, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.now().isoformat.return_value = "2025-01-20T15:00:00"  # Fix the issue
        yield mock_datetime


def test_audit_log_create(mock_dynamodb, mock_generate_uuid, mock_datetime):
    dynamodb, mock_table = mock_dynamodb
    user_id = "69c5ed6f35a24794bf9c1d9804e8d742"
    new_data = {"organ": "Heart", "status": "Active"}

    @audit_log(Model.FA.value, Operation.CREATE.value)
    def mock_create(*args, **kwargs):
        print(*args, **kwargs)
        return {"id": "new-id-123"}, None  # Expected return for create

    mock_create(dynamodb, user_id, new_data)

    mock_table.put_item.assert_called_once_with(Item={
        "id": "audit-log-1234",
        "user_id": user_id,
        "model": Model.FA.value,
        "model_id": "new-id-123",
        "old_values": None,
        "new_values": {"id": "new-id-123", **new_data},
        "operation": Operation.CREATE.value,
        "created_at": "2025-01-20T15:00:00",
    })

def test_audit_log_update(mock_dynamodb, mock_generate_uuid, mock_datetime):
    dynamodb, mock_table = mock_dynamodb
    user_id = "69c5ed6f35a24794bf9c1d9804e8d742"
    model_id = "8dab5fd2f2e840b68b2ab413772062ba"
    updated_data = {**sample_new_values}

    @audit_log(Model.FA.value, Operation.UPDATE.value)
    def mock_update(*args, **kwargs):
        print(*args, **kwargs)
        return updated_data, sample_old_values

    mock_update(dynamodb, user_id, model_id, updated_data)

    mock_table.put_item.assert_called_once_with(Item={
        "id": "audit-log-1234",
        "user_id": user_id,
        "model": Model.FA.value,
        "model_id": model_id,
        "old_values": sample_old_values,
        "new_values": updated_data,
        "operation": Operation.UPDATE.value,
        "created_at": "2025-01-20T15:00:00",
    })

def test_audit_log_delete(mock_dynamodb, mock_generate_uuid, mock_datetime):
    dynamodb, mock_table = mock_dynamodb
    user_id = "69c5ed6f35a24794bf9c1d9804e8d742"
    model_id = "8dab5fd2f2e840b68b2ab413772062ba"

    @audit_log(Model.FA.value, Operation.DELETE.value)
    def mock_delete(*args, **kwargs):
        print(*args, **kwargs)
        return {"message": "Financial Asset deleted", "user_id": user_id, "id": model_id}, sample_old_values

    mock_delete(dynamodb, user_id, model_id)

    mock_table.put_item.assert_called_once_with(Item={
        "id": "audit-log-1234",
        "user_id": user_id,
        "model": Model.FA.value,
        "model_id": model_id,
        "old_values": sample_old_values,
        "new_values": None,
        "operation": Operation.DELETE.value,
        "created_at": "2025-01-20T15:00:00",
    })
