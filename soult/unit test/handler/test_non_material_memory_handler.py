import pytest
from unittest.mock import patch
import handler.non_material_memories_handler as handler

@pytest.fixture
def mock_db():
    with patch("handler.non_material_memories_handler.db") as mock:
        yield mock

@pytest.fixture
def mock_validator():
    with patch("handler.non_material_memories_handler.validator.validate") as mock:
        yield mock

@pytest.fixture
def mock_build_response():
    with patch("handler.non_material_memories_handler.build_response") as mock:
        yield mock

@pytest.fixture
def mock_event_decorator():
    with patch("utils.sns_utils.event", lambda *args, **kwargs: lambda func: func):
        yield

def test_create_non_material_memory_success(mock_db, mock_validator, mock_build_response, mock_event_decorator):
    user_id = "user123"
    non_material_memory = {
        "type": "Artwork",
        "details": "Painting by ABC",
        "memories": [
            {"type": "pdf", "document_arn": "s3 path"},
            {"type": "mp4", "document_arn": "s3 path"}
        ],
        "created_at": "2025-01-10T11:00:00Z",
        "updated_at": "2025-01-20T15:00:00Z",
        "status": True
    }
    mock_validator.return_value = non_material_memory
    mock_db.create_non_material_memory.return_value = {"id": "3fc4720e9e5f4e0b9b7a48d355fca34d", **non_material_memory}
    mock_build_response.return_value = {"statusCode": 200, "body": "Created Successfully"}
    response = handler.create(user_id, non_material_memory)
    mock_validator.assert_called_once_with(non_material_memory)
    mock_db.create_non_material_memory.assert_called_once_with(user_id, non_material_memory)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "Created Successfully"}

def test_create_non_material_memory_validation_error(mock_db, mock_validator, mock_build_response, mock_event_decorator):
    user_id = "user123"
    invalid_data = {"type": "", "details": "Invalid data"}
    mock_validator.return_value = {"errors": ["Type field is required"]}
    mock_build_response.return_value = {"statusCode": 400, "body": "Validation Error"}
    response = handler.create(user_id, invalid_data)
    mock_validator.assert_called_once_with(invalid_data)
    mock_db.create_non_material_memory.assert_not_called()
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 400, "body": "Validation Error"}


def test_update_non_material_memory_success(mock_db, mock_validator, mock_build_response, mock_event_decorator):
    user_id = "user123"
    non_asset_id = "3fc4720e9e5f4e0b9b7a48d355fca34d"
    updated_data = {
        "type": "Artwork",
        "details": "Updated Painting by ABC",
        "memories": [
            {"type": "pdf", "document_arn": "s3 path"},
            {"type": "mp4", "document_arn": "s3 path"}
        ],
        "created_at": "2025-01-10T11:00:00Z",
        "updated_at": "2025-01-20T15:00:00Z",
        "status": True
    }
    mock_validator.return_value = updated_data
    mock_db.update_non_material_memory.return_value = {"id": non_asset_id, **updated_data}
    mock_build_response.return_value = {"statusCode": 200, "body": "Updated Successfully"}
    response = handler.update(user_id, non_asset_id, updated_data)
    mock_validator.assert_called_once_with(updated_data)
    mock_db.update_non_material_memory.assert_called_once_with(user_id, non_asset_id, updated_data)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "Updated Successfully"}


def test_update_non_material_memory_validation_error(mock_db, mock_validator, mock_build_response,
                                                     mock_event_decorator):
    user_id = "user123"
    non_asset_id = "3fc4720e9e5f4e0b9b7a48d355fca34d"
    invalid_data = {"type": "", "details": "Invalid Data"}
    mock_validator.return_value = {"errors": ["Type field is required"]}
    mock_build_response.return_value = {"statusCode": 400, "body": "Validation Error"}
    response = handler.update(user_id, non_asset_id, invalid_data)
    mock_validator.assert_called_once_with(invalid_data)
    mock_db.update_non_material_memory.assert_not_called()
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 400, "body": "Validation Error"}


def test_delete_non_material_memory(mock_db, mock_build_response):
    user_id = "user123"
    non_material_memory_id = "3fc4720e9e5f4e0b9b7a48d355fca34d"
    mock_db.delete_non_material_memory.return_value = {"message": "Deleted Successfully"}
    mock_build_response.return_value = {"statusCode": 200, "body": "Deleted Successfully"}
    response = handler.delete(user_id, non_material_memory_id)
    mock_db.delete_non_material_memory.assert_called_once_with(user_id, non_material_memory_id)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "Deleted Successfully"}


def test_find_non_material_memory(mock_db, mock_build_response):
    user_id = "user123"
    non_material_memory_id = "3fc4720e9e5f4e0b9b7a48d355fca34d"
    mock_db.find_non_material_memory.return_value = {
        "id": non_material_memory_id,
        "type": "Artwork",
        "details": "Painting by ABC"
    }
    mock_build_response.return_value = {"statusCode": 200, "body": "Found Successfully"}
    response = handler.find(user_id, non_material_memory_id)
    mock_db.find_non_material_memory.assert_called_once_with(user_id, non_material_memory_id)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "Found Successfully"}


def test_find_all_non_material_memory(mock_db, mock_build_response):
    user_id = "user123"
    mock_db.find_all_non_material_memory.return_value = [
        {
            "id": "3fc4720e9e5f4e0b9b7a48d355fca34d",
            "type": "Artwork",
            "details": "Painting by ABC"
        }
    ]
    mock_build_response.return_value = {"statusCode": 200, "body": "All Found Successfully"}
    response = handler.find_all(user_id)
    mock_db.find_all_non_material_memory.assert_called_once_with(user_id)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "All Found Successfully"}