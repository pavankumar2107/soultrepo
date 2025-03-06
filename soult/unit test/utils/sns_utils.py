import json
import pytest
from unittest.mock import patch, MagicMock
from utils.sns_utils import event

@pytest.fixture
def mock_sns_client():
    with patch("utils.sns_utils.get_sns_connection") as mock_sns:
        mock_client = MagicMock()
        mock_sns.return_value = mock_client
        yield mock_client

def test_event_decorator_successful_sns_publish(mock_sns_client):
    @event("USER", "CREATE")
    def mock_function(user_id):
        return {"data": {"id": user_id}}
    user_id = "12345"
    result = mock_function(user_id)
    expected_message = json.dumps({
        "event": "USER CREATE",
        "User_id": user_id,
        "action": "CREATE",
        "model_name": "USER",
        "model_id": user_id
    })
    assert result == {"data": {"id": user_id}}
    mock_sns_client.publish.assert_called_once_with(
        TopicArn='arn:aws:sns:ap-south-1:127214196952:soult-events',
        Message=expected_message,
        Subject="USER CREATE",
        MessageAttributes={
            "Action": {"DataType": "String", "StringValue": "CREATE"},
            "ModelName": {"DataType": "String", "StringValue": "USER"},
        }
    )
