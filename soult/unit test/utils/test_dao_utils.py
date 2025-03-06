from unittest.mock import patch
from datetime import datetime

import pytest

from utils.dao_utils import build_record, from_attributes_to_json  # Replace `your_module` with the actual module name


@patch("utils.dao_utils.generate_uuid")
@patch("utils.dao_utils.datetime")
def test_build_record(mock_datetime, mock_generate_uuid):
    """Test build_record function."""
    mock_generate_uuid.return_value = "mock-uuid-1234"
    mock_datetime.now.return_value = datetime(2025, 2, 27, 12, 0, 0)
    expected_result = {
        "id": "mock-uuid-1234",
        "status": True,
        "created_at": "2025-02-27 12:00:00",
    }
    result = build_record()
    assert result == expected_result
    mock_generate_uuid.assert_called_once()
    mock_datetime.now.assert_called_once()

def test_from_attributes_to_json():
    attribute_data = {"id": {"S": "1234"}, "status": {"BOOL": True}}
    expected_json = {"id": "1234", "status": True}
    result = from_attributes_to_json(attribute_data)
    assert result == expected_json

