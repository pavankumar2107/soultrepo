import unittest
import json
from unittest.mock import patch
from handler.user_handler import find  # Replace 'your_module' with the name of the module where `find` is defined

class UserHandlerTest(unittest.TestCase):
    @patch("handler.user_handler.table")  # Mock the `table` resource
    @patch("handler.user_handler.logger")  # Mock the logger
    def test_find_user_found(self, mock_logger, mock_table):
        # Mock the DynamoDB get_item response for a found user
        mock_table.get_item.return_value = {"Item": {"id": "123", "name": "John Doe"}}

        # Call the function with a test ID
        response = find("123")

        # Verify the response
        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(json.loads(response["body"])["id"], "123")
        self.assertEqual(json.loads(response["body"])["name"], "John Doe")

        # Ensure logger wasn't called for exceptions
        mock_logger.exception.assert_not_called()

    @patch("handler.user_handler.table")
    @patch("handler.user_handler.logger")
    def test_find_user_not_found(self, mock_logger, mock_table):
        # Mock the DynamoDB get_item response for a missing user
        mock_table.get_item.return_value = {}

        # Call the function with a test ID
        response = find("999")

        # Verify the response
        self.assertEqual(response["statusCode"], 404)
        self.assertEqual(json.loads(response["body"])["message"], "User not found")

        # Ensure logger wasn't called for exceptions
        mock_logger.exception.assert_not_called()

    @patch("handler.user_handler.table")
    @patch("handler.user_handler.logger")
    def test_find_exception(self, mock_logger, mock_table):
        # Simulate an exception being raised during get_item
        mock_table.get_item.side_effect = Exception("Database error")

        # Call the function with a test ID
        response = find("error-id")

        # Verify the response
        self.assertEqual(response["statusCode"], 500)
        self.assertEqual(json.loads(response["body"])["error"], "Database error")

        # Ensure logger.exception was called
        mock_logger.exception.assert_called_with("Error: user find 'error-id'")

