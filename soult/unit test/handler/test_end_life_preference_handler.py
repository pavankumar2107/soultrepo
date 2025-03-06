import handler.end_life_preference_handler as handler
from unittest.mock import patch

# Sample dataset from the database
sample_end_life_preferences = {
    "resuscitation": "No",
    "decision_maker": {
        "type": "loved_one",
        "id": "3fbfd18f456b450bbe16d1fa83b59324"
    },
    "condition_for_withdrawal": "Brain Death",
    "duration_of_support": 5,
    "ventilator": "Yes",
}

def test_create_success():
    user_id = "69c5ed6f35a24794bf9c1d9804e8d742"
    with patch("handler.end_life_preference_handler.validator.validate") as mock_validate, \
         patch("handler.end_life_preference_handler.db.create_end_life_preferences") as mock_db, \
         patch("handler.end_life_preference_handler.build_response") as mock_build_response:
        mock_validate.return_value = sample_end_life_preferences
        mock_db.return_value = {"message": "Created Successfully", "data": sample_end_life_preferences}
        mock_build_response.return_value = {"statusCode": 200, "body": {"message": "Created Successfully", "data": sample_end_life_preferences}}
        response = handler.create(user_id, sample_end_life_preferences)
        mock_validate.assert_called_once_with(sample_end_life_preferences)
        mock_db.assert_called_once_with(user_id, sample_end_life_preferences)
        mock_build_response.assert_called_once()
        assert response == {"statusCode": 200, "body": {"message": "Created Successfully", "data": sample_end_life_preferences}}

def test_create_validation_error():
    user_id = "69c5ed6f35a24794bf9c1d9804e8d742"
    invalid_data = {}
    with patch("handler.end_life_preference_handler.validator.validate") as mock_validate, \
         patch("handler.end_life_preference_handler.build_response") as mock_build_response:
        mock_validate.return_value = {"errors": "Invalid Data"}
        mock_build_response.return_value = {"statusCode": 400, "body": "Invalid Data"}
        response = handler.create(user_id, invalid_data)
        mock_validate.assert_called_once_with(invalid_data)
        mock_build_response.assert_called_once()
        assert response == {"statusCode": 400, "body": "Invalid Data"}

def test_update_success():
    user_id = "69c5ed6f35a24794bf9c1d9804e8d742"
    updated_data = sample_end_life_preferences.copy()
    updated_data["resuscitation"] = "Yes"
    with patch("handler.end_life_preference_handler.validator.validate") as mock_validate, \
         patch("handler.end_life_preference_handler.db.update_end_life_preferences") as mock_db, \
         patch("handler.end_life_preference_handler.build_response") as mock_build_response:
        mock_validate.return_value = updated_data
        mock_db.return_value = {"message": "Updated Successfully", "data": updated_data}
        mock_build_response.return_value = {"statusCode": 200, "body": {"message": "Updated Successfully", "data": updated_data}}
        response = handler.update(user_id, updated_data)
        mock_validate.assert_called_once_with(updated_data)
        mock_db.assert_called_once_with(user_id, updated_data)
        mock_build_response.assert_called_once()
        assert response == {"statusCode": 200, "body": {"message": "Updated Successfully", "data": updated_data}}

def test_update_validation_error():
    user_id = "69c5ed6f35a24794bf9c1d9804e8d742"
    invalid_data = {}
    with patch("handler.end_life_preference_handler.validator.validate") as mock_validate, \
         patch("handler.end_life_preference_handler.build_response") as mock_build_response:
        mock_validate.return_value = {"errors": "Invalid Data"}
        mock_build_response.return_value = {"statusCode": 400, "body": "Invalid Data"}
        response = handler.update(user_id, invalid_data)
        mock_validate.assert_called_once_with(invalid_data)
        mock_build_response.assert_called_once()
        assert response == {"statusCode": 400, "body": "Invalid Data"}

def test_delete_success():
    user_id = "69c5ed6f35a24794bf9c1d9804e8d742"
    preferences_id = "elp123"
    with patch("handler.end_life_preference_handler.db.delete_end_life_preferences") as mock_db, \
         patch("handler.end_life_preference_handler.build_response") as mock_build_response:
        mock_db.return_value = {"message": "Deleted Successfully"}
        mock_build_response.return_value = {"statusCode": 200, "body": "Deleted Successfully"}
        response = handler.delete(user_id, preferences_id)
        mock_db.assert_called_once_with(user_id, preferences_id)
        mock_build_response.assert_called_once()
        assert response == {"statusCode": 200, "body": "Deleted Successfully"}

def test_find_success():
    user_id = "69c5ed6f35a24794bf9c1d9804e8d742"
    with patch("handler.end_life_preference_handler.db.find_end_life_preferences") as mock_db, \
         patch("handler.end_life_preference_handler.build_response") as mock_build_response:
        mock_db.return_value = sample_end_life_preferences
        mock_build_response.return_value = {"statusCode": 200, "body": sample_end_life_preferences}
        response = handler.find(user_id)
        mock_db.assert_called_once_with(user_id)
        mock_build_response.assert_called_once()
        assert response == {"statusCode": 200, "body": sample_end_life_preferences}
