import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pytest
from validator.financial_asset_validator import validate

@pytest.fixture
def valid_financial_asset_data():
    return {
        "id": "123",
        "type": "Stock",
        "fund_name": "Tech Fund",
        "maturity_date": "2030-12-31",
        "details": "Investment details",
        "document_arn": "arn:aws:s3:::some-document",
        "nominees": [
            {
                "loved_one_id": "789",
                "share": 50
            }
        ]
    }

@pytest.fixture
def invalid_financial_asset_data():
    return {
        "id": "",
        "type": "",
        "fund_name": "",
        "maturity_date": 2030-12-31,
        "details": "",
        "document_arn": "",
        "nominees": [
            {
                "loved_one_id": 789,
                "share": "20"
            }
        ]
    }

def test_validate_success(valid_financial_asset_data):
    result = validate(valid_financial_asset_data)
    assert "errors" not in result  # No errors should be returned

def test_validate_failure(invalid_financial_asset_data):
    result = validate(invalid_financial_asset_data)

    expected_errors = [
        "Field 'id' should be a non-empty string",
        "Field 'type' should be non-empty string",
        "Field 'fund_name' should be non-empty string",
        "Field 'maturity_date' should be a non-empty string",
        "Field 'details' should be a non-empty string",
        "Field 'document_arn' should be a non-empty string",
        "Field 'loved_one_id' should be a non-empty string"
    ]

    assert "errors" in result
    assert set(result["errors"]) == set(expected_errors)

def test_validate_partial_invalid_data():
    partial_invalid_data = {
        "id": "123",  # Valid
        "type": "",  # Invalid
        "fund_name": "",  # Invalid
    }
    result = validate(partial_invalid_data)

    expected_errors = [
        "Field 'type' should be non-empty string",
        "Field 'fund_name' should be non-empty string"
    ]

    assert "errors" in result
    assert set(result["errors"]) == set(expected_errors)

def test_validate_missing_fields():
    missing_fields_data = {
        "created_at": "2025-01-01"
    }
    result = validate(missing_fields_data)

    assert "errors" not in result

