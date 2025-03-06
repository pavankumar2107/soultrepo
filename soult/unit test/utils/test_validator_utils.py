from schema import Schema
from utils.validator_utils import validate_field, validate_field_dict

def test_validate_field_success():
    schema = {"age": int}
    result = validate_field("age", 25, schema)
    assert result is None

def test_validate_field_failure():
    schema = {"age": int}
    error_msg = validate_field("age", "twenty-five", schema)
    assert error_msg is not None

def test_validate_field_dict_success():
    schema = Schema({"age": int})
    result = validate_field_dict("age", 30, schema)
    assert result is None

def test_validate_field_dict_failure():
    schema = Schema({"age": int, "name": str})
    error_msg = validate_field_dict("age", "thirty", schema)
    assert error_msg is not None

def test_validate_field_dict_invalid_key():
    schema = Schema({"name": str})
    error_msg = validate_field_dict("age", 30, schema)
    assert error_msg is not None
