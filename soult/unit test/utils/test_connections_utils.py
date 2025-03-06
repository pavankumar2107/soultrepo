from unittest.mock import patch
from utils.connections_utils import get_connection, get_sns_connection, \
    get_ses_connection

REGION = 'ap-south-1'
DYNAMODB = 'dynamodb'
SNS = 'sns'
SES = 'ses'


@patch("boto3.resource")
def test_get_connection(mock_boto_resource):
    mock_dynamodb = mock_boto_resource.return_value
    connection = get_connection()
    mock_boto_resource.assert_called_once_with(DYNAMODB, region_name=REGION)
    assert connection == mock_dynamodb


@patch("boto3.client")
def test_get_sns_connection(mock_boto_client):
    mock_sns = mock_boto_client.return_value
    connection = get_sns_connection()
    mock_boto_client.assert_called_once_with(SNS, REGION)
    assert connection == mock_sns


@patch("boto3.client")
def test_get_ses_connection(mock_boto_client):
    mock_ses = mock_boto_client.return_value
    connection = get_ses_connection()
    mock_boto_client.assert_called_once_with(SES, REGION)
    assert connection == mock_ses
