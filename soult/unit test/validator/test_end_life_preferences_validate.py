import sys
import os
from validator.end_life_preferences_validate import validate

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
def test_validate_end_life_preferences():
    valid_data = {
        "id": "123",
        "created_at": "2025-02-19",
        "updated_at": "2025-02-19",
        "status": True,
        "resuscitation": "Do not resuscitate",
        "condition_for_withdrawal": "Brain dead",
        "ventilator": "Yes",
        "duration_of_support": 5,
        "decision_maker": {
            "id": "456",
            "type_of_decision_maker": "Family"
        }
    }

    invalid_data = {
        "id": "",
        "status": "Active",
        "duration_of_support": "ten",
        "decision_maker": {
            "id": 789,
            "type_of_decision_maker": 22
        }
    }

    expected_errors = [
        "Field 'id' should be a non-empty string",
        "Field 'status' should be a boolean",
        "Field 'duration_of_support' should be an integer",
        "Field 'decision_maker.id' should be a string",
        "Field 'decision_maker.type_of_decision_maker' should be a string"
    ]

    assert validate(valid_data) == valid_data

    result = validate(invalid_data)
    assert "errors" in result
    assert isinstance(result["errors"], list)
    assert len(result["errors"]) > 0
    assert set(result["errors"]) == set(expected_errors)
