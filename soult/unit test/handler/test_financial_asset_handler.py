import pytest
from unittest.mock import patch
import handler.financial_asset_handler as handler

# Sample financial asset dataset
financial_asset_data = {
    "id": "ec5ca9d51e334dd2811169d4d2ce14c4",
    "type": "Fixed Deposit",
    "maturity_date": "2026-01-11",
    "details": "200000 with interest of 7% per year",
    "document_arn": "<s3 path>",
    "nominees": [
        {"loved_one_id": "71bb784eb11d4d30bd7062b75311f4f3", "share": 30},
        {"loved_one_id": "71bb784eb11d56345535bd7062b75311f4f3", "share": 50}
    ],
    "created_at": "2025-01-10T11:00:00Z",
    "updated_at": "2025-01-20T15:00:00Z",
    "status": True
}


@pytest.fixture
def mock_db():
    with patch("handler.financial_asset_handler.db") as mock:
        yield mock


@pytest.fixture
def mock_validator():
    with patch("handler.financial_asset_handler.validator.validate") as mock:
        yield mock


@pytest.fixture
def mock_build_response():
    with patch("handler.financial_asset_handler.build_response") as mock:
        yield mock


@pytest.fixture
def mock_event_decorator():
    with patch("utils.sns_utils.event", lambda *args, **kwargs: lambda func: func):
        yield


def test_create_financial_asset_success(mock_db, mock_validator, mock_build_response, mock_event_decorator):
    user_id = "user123"
    mock_validator.return_value = financial_asset_data
    mock_db.create_financial_asset.return_value = {**financial_asset_data, "id": "asset123"}
    mock_build_response.return_value = {"statusCode": 200, "body": "Success"}
    response = handler.create(user_id, financial_asset_data)
    mock_validator.assert_called_once_with(financial_asset_data)
    mock_db.create_financial_asset.assert_called_once_with(user_id, financial_asset_data)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "Success"}


def test_create_financial_asset_validation_error(mock_db, mock_validator, mock_build_response, mock_event_decorator):
    user_id = "user123"
    financial_asset = {"asset": "stocks", "details": -1000}  # Invalid data
    mock_validator.return_value = {"errors": ["Invalid value"]}
    mock_build_response.return_value = {"statusCode": 400, "body": "Invalid value"}
    response = handler.create(user_id, financial_asset)
    mock_validator.assert_called_once_with(financial_asset)
    mock_db.create_financial_asset.assert_not_called()
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 400, "body": "Invalid value"}


def test_update_financial_asset_success(mock_db, mock_validator, mock_build_response, mock_event_decorator):
    user_id = "user123"
    financial_asset_id = "asset456"
    updated_data = {**financial_asset_data, "details": 5000}  # Example of update with new value
    mock_validator.return_value = updated_data
    mock_db.update_financial_asset.return_value = updated_data
    mock_build_response.return_value = {"statusCode": 200, "body": "Update Success"}
    response = handler.update(user_id, financial_asset_id, updated_data)
    mock_validator.assert_called_once_with(updated_data)
    mock_db.update_financial_asset.assert_called_once_with(user_id, financial_asset_id, updated_data)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "Update Success"}


def test_update_financial_asset_validation_error(mock_db, mock_validator, mock_build_response, mock_event_decorator):
    user_id = "user123"
    financial_asset_id = "asset456"
    updated_data = {**financial_asset_data, "details": -5000}  # Invalid data
    mock_validator.return_value = {"errors": ["Invalid value"]}
    mock_build_response.return_value = {"statusCode": 400, "body": "Invalid value"}
    response = handler.update(user_id, financial_asset_id, updated_data)
    mock_validator.assert_called_once_with(updated_data)
    mock_db.update_financial_asset.assert_not_called()
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 400, "body": "Invalid value"}


def test_delete_financial_asset_success(mock_db, mock_build_response):
    user_id = "user123"
    financial_asset_id = "asset789"
    mock_db.delete_financial_asset.return_value = {"message": "Deleted successfully"}
    mock_build_response.return_value = {"statusCode": 200, "body": "Deleted successfully"}
    response = handler.delete(user_id, financial_asset_id)
    mock_db.delete_financial_asset.assert_called_once_with(user_id, financial_asset_id)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "Deleted successfully"}


def test_find_financial_asset_success(mock_db, mock_build_response):
    user_id = "user123"
    financial_asset_id = "asset789"
    mock_db.find_financial_asset.return_value = {**financial_asset_data, "id": financial_asset_id}
    mock_build_response.return_value = {"statusCode": 200, "body": "Asset Found"}
    response = handler.find(user_id, financial_asset_id)
    mock_db.find_financial_asset.assert_called_once_with(user_id, financial_asset_id)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "Asset Found"}


def test_find_all_financial_assets_success(mock_db, mock_build_response):
    user_id = "user123"
    mock_db.find_all_financial_asset.return_value = [financial_asset_data,
                                               {"id": "asset2", "type": "bonds", "value": 3000}]
    mock_build_response.return_value = {"statusCode": 200, "body": "Assets Found"}
    response = handler.find_all(user_id)
    mock_db.find_all_financial_asset.assert_called_once_with(user_id)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "Assets Found"}
