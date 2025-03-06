import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pytest
from validator.user_validator import validate

@pytest.fixture
def valid_user_data():
    return {
    "id": "e1ed0621-64e7-4594-ab95-ca3dda146d34",
    "created_at": "2025-02-06",
    "updated_at": "2025-02-14T11:34:05.923640",
    "status": True,
    "firstname": "Barry",
    "lastname": "Allen",
    "phone_no": "7890123468",
    "email": "a@gmail.com",
    "address" :"hyderabad",
    "dob":"26-06-2656",
    "gender":"male",
    "mpin":"5698"
}

@pytest.fixture
def invalid_user_data():
    return {
    "id": "",
    "created_at": "",
    "updated_at": "",
    "status": "True",
    "firstname": "",
    "lastname": "",
    "phone_no": "789022123468",
    "email": "amail.com",
    "address" :"",
    "dob":"",
    "gender":"",
    "mpin":""
}

def test_validate_success(valid_user_data):
    result = validate(valid_user_data)
    assert "errors" not in result  # No errors should be returned

def test_validate_failure(invalid_user_data):
    result = validate(invalid_user_data)

    expected_errors = [
        "Field 'id' should be a non-empty string",
        "Field 'created_at' should be a non-empty string",
        "Field 'updated_at' should be a non-empty string",
        "Field 'status' should be a boolean",
        "Field 'firstname' should be a non-empty string",
        "Field 'lastname' should be a non-empty string",
        'Phone number must be a 10-digit number',
        'Invalid email format',
        "Field 'address' should be a non-empty string",
        "Field 'dob' should be a non-empty string",
        "Field 'gender' should be a non-empty string",
        "Field 'mpin' should be a non-empty string"
    ]

    assert "errors" in result
    assert set(result["errors"]) == set(expected_errors)

def test_validate_partial_invalid_data():
    partial_invalid_data = {
        "id": "123",  # Valid
        "lastname": "",
        "phone_no": "789022123468",
    }
    result = validate(partial_invalid_data)

    expected_errors = [
        "Field 'lastname' should be a non-empty string",
        'Phone number must be a 10-digit number',
    ]

    assert "errors" in result
    assert set(result["errors"]) == set(expected_errors)

def test_validate_missing_fields():
    missing_fields_data = {
        "created_at": "2025-01-01"
    }
    result = validate(missing_fields_data)

    assert "errors" not in result

