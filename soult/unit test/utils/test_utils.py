import json
import uuid
import hashlib
from decimal import Decimal
import pytest
from unittest.mock import patch, MagicMock
from utils.utils import generate_uuid, IntConvertor, build_response, hash_value


def test_generate_uuid():
    uuid_val = generate_uuid()
    assert isinstance(uuid_val, str)
    assert len(uuid_val) == 36
    assert uuid.UUID(uuid_val)


def test_int_converter():
    data = {"amount": Decimal("42.0")}
    json_data = json.dumps(data, cls=IntConvertor)
    assert json.loads(json_data) == {"amount": 42}


@pytest.fixture
def mock_logger():
    """Fixture to mock logger."""
    with patch("utils.utils.get_logger") as mock_logger:
        logger_mock = MagicMock()
        mock_logger.return_value = logger_mock
        yield logger_mock


def test_build_response_with_body(mock_logger):
    body = {"message": "Success", "count": Decimal("5")}
    response = build_response(200, body)
    expected_body = json.dumps({"message": "Success", "count": 5})  # Decimal converted to int
    assert response == {
        "statusCode": 200,
        "headers": {
            "Content-Type": "Application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": expected_body,
    }

    mock_logger.info.assert_called_once_with(json.loads(expected_body))

def test_hash_value():
    test_input = "test_string"
    expected_hash = hashlib.sha256(test_input.encode()).hexdigest()
    assert hash_value(test_input) == expected_hash
