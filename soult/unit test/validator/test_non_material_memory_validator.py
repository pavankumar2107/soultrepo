import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pytest
from validator.non_material_memory_validator import validate

@pytest.fixture
def valid_non_material_memory_data():
    return {
        "id": "26e059ba-e815-406b-8464-1343fe88c0d7",
        "created_at": "2025-02-04T14:48:19.483007",
        "details": "painting",
        "memory": [
            {
                "id": "93e91043-bf95-4527-9d70-3b8ec65142d8",
                "document_arn": "s3",
                "type": "pds"
            }
        ],
        "non_asset_type": "art",
        "status": True,
        "updated_at": "2025-02-04T14:48:19.483007"
    }

@pytest.fixture
def invalid_non_material_memory_data():
    return {
        "id": "",
        "created_at": "",
        "details": "painting",
        "memory": [
            {
                "id": "",
                "document_arn": "s3",
                "type": "pds"
            }
        ],
        "non_asset_type": "",
        "status": "Active",
        "updated_at": ""
    }

def test_validate_success(valid_non_material_memory_data):
    result = validate(valid_non_material_memory_data)
    assert "errors" not in result  # No errors should be returned

def test_validate_failure(invalid_non_material_memory_data):
    result = validate(invalid_non_material_memory_data)

    expected_errors = [
        "Field 'id' should be a non-empty string  ",
        "Field 'created_at' should be a non-empty string  ",
        "Field 'id' should be non-empty string",
        "Field 'non_asset_type' should be non-empty string",
        "Field 'status' should be a boolean",
        "Field 'updated_at' should be a non-empty string  "
    ]

    assert "errors" in result
    assert set(result["errors"]) == set(expected_errors)

def test_validate_partial_invalid_data():
    partial_invalid_data = {
        "id": "",  # Valid
        "non_asset_type": "",
        "memory": [
            {
                "id": "93e91043-bf95-4527-9d70-3b8ec65142d8",
                "document_arn": "s3",
                "type": "pds"
            }
        ]
    }
    result = validate(partial_invalid_data)

    expected_errors = [
        "Field 'id' should be a non-empty string  ",
        "Field 'non_asset_type' should be non-empty string"
    ]

    assert "errors" in result
    assert set(result["errors"]) == set(expected_errors)

def test_validate_missing_fields():
    missing_fields_data = {
        "created_at": "2025-01-01"
    }
    result = validate(missing_fields_data)

    assert "errors" not in result

