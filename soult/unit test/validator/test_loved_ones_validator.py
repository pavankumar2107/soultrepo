import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from validator.loved_ones_validator import validate
import pytest


@pytest.fixture
def valid_loved_one_data():
    return {
        "id": "f1b79dba-a822-4847-8e03-ec94c2f0d045",
       "aadhar_number": "127014804252",
       "address": "fas",
       "created_at": "2025-02-21 18:52:34",
       "dob": "3326",
       "email_id": "n@gmail.com",
       "first_name": "a",
       "gender": "f",
       "last_name": "neha",
       "maiden_name": "a",
       "phone_number": "8639890782",
       "relationship": "a",
       "role": "a",
       "status": True
    }

@pytest.fixture
def invalid_loved_one_data():
    return {
        "id": "",
        "created_at":"",
        "updated_at":"",
        "status": "True",
        "first_name": "",
        "maiden_name": "",
        "last_name": "",
        "relationship": "",
        "role": "",
        "phone_number": 869890782,
        "gender": "",
        "email_id": "nmail.com",
        "aadhar_number": "12701480224252",
        "dob": 3326,
        "address": ""
    }

def test_validate_success(valid_loved_one_data):
    result = validate(valid_loved_one_data)
    assert "errors" not in result

def test_validate_failure(invalid_loved_one_data):
    result = validate(invalid_loved_one_data)

    expected_errors = [
        "Field 'id' should be a non-empty string",
        "Field 'created_at' should be a non-empty string",
        "Field 'updated_at' should be a non-empty string",
        "Field 'status' should be a boolean",
        "Field 'first_name' should be a non-empty string",
        "Field 'maiden_name' should be a non-empty string",
        "Field 'last_name' should be a non-empty string",
        "Field 'relationship' should be a non-empty string",
        "Field 'role' should be a non-empty string",
        "Phone number must be a 10-digit number",
        "Field 'gender' should be a non-empty string",
        "Invalid email format",
        "Field 'address' should be a non-empty string",
        "Field 'dob' should be a non-empty string",
        "Aadhar number must be 12 digits"
    ]

    assert "errors" in result
    assert set(result["errors"]) == set(expected_errors)

def test_validate_partial_invalid_data():
    partial_invalid_data = {
        "id": "123",  # Valid
        "first_name": "",
        "aadhar_number": "12714804252",  # Invalid
    }
    result = validate(partial_invalid_data)

    expected_errors = [
        "Field 'first_name' should be a non-empty string",
        "Aadhar number must be 12 digits"
    ]

    assert "errors" in result
    assert set(result["errors"]) == set(expected_errors)

def test_validate_missing_fields():
    missing_fields_data = {
        "created_at": "2025-01-01"
    }
    result = validate(missing_fields_data)

    assert "errors" not in result


