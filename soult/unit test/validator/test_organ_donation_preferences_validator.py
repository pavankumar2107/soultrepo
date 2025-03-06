import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pytest
from validator.organ_donation_preferences_validator import validate

@pytest.fixture
def valid_organ_donation_preference_data():
    return {
       "id": "a2539625-ca66-4e01-8e86-a538da43b426",
       "additional_conditions": "no",
       "created_at": "2025-01-25",
       "organ": "Kidney",
       "status": True,
       "updated_at": "2025-01-25T11:18:56.014366"
    }

@pytest.fixture
def invalid_organ_donation_preference_data():
    return {
       "id": "",
       "additional_conditions": "",
       "created_at": "",
       "organ": "",
       "status": "True",
       "updated_at": ""
    }

def test_validate_success(valid_organ_donation_preference_data):
    result = validate(valid_organ_donation_preference_data)
    assert "errors" not in result  # No errors should be returned

def test_validate_failure(invalid_organ_donation_preference_data):
    result = validate(invalid_organ_donation_preference_data)

    expected_errors = [
        "Field 'id' should be a non-empty string",
        "Field 'additional_conditions' should be a string",
        "Field 'created_at' should be a non-empty string",
        "Field 'organ' should be a string",
        "Field 'status' should be a boolean",
        "Field 'updated_at' should be a non-empty string"
    ]

    assert "errors" in result
    assert set(result["errors"]) == set(expected_errors)

def test_validate_partial_invalid_data():
    partial_invalid_data = {
        "id": "123",  # Valid
        "organ": 123,
        "additional_conditions": "",
    }
    result = validate(partial_invalid_data)

    expected_errors = [
        "Field 'additional_conditions' should be a string",
        "Field 'organ' should be a string",
    ]

    assert "errors" in result
    assert set(result["errors"]) == set(expected_errors)

def test_validate_missing_fields():
    missing_fields_data = {
        "created_at": "2025-01-01"
    }
    result = validate(missing_fields_data)

    assert "errors" not in result

