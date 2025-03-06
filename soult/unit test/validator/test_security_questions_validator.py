import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pytest
from validator.security_questions_validator import validate

@pytest.fixture
def valid_organ_donation_preference_data():
    return  [
      {
       "answer": "89eccb0940a76c11197cdf2341ec57c0053637e9b882d64a5753d9a2c79131f3",
       "question": "What is your lastname?"
      },
      {
       "answer": "c6cfe6e4f129a34671d10c1bbe158eff05197d388727e331951b0ec2637c194e",
       "question": "What is your favorite color?"
      }
     ]

@pytest.fixture
def invalid_organ_donation_preference_data():
    return [
      {
       "answer": 123,
       "question": 321
      },
      {
       "answer": 321,
       "question": 321
      }
    ]

def test_validate_success(valid_organ_donation_preference_data):
    res = validate(valid_organ_donation_preference_data)
    result=res[0]
    assert "errors" not in result  # No errors should be returned

def test_validate_failure(invalid_organ_donation_preference_data):
    res = validate(invalid_organ_donation_preference_data)
    result = res[0]
    expected_errors = [
        "data is in wrong format"
    ]

    assert "errors" in result
    assert set(result["errors"]) == set(expected_errors)

