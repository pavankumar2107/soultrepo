import pytest
from unittest.mock import patch
import handler.security_questions_handler as handler

security_questions_data = [
    {"question": "What is your favorite color?", "answer": "Blue"},
]


@pytest.fixture
def mock_db():
    with patch("handler.security_questions_handler.db") as mock:
        yield mock

@pytest.fixture
def mock_validator():
    with patch("handler.security_questions_handler.validator.validate") as mock:
        yield mock

@pytest.fixture
def mock_build_response():
    with patch("handler.security_questions_handler.build_response") as mock:
        yield mock


def test_create_security_questions_success(mock_db, mock_validator, mock_build_response):
    user_id = "user123"
    mock_validator.return_value = security_questions_data
    mock_db.create_security_question.return_value = {"message": "Security questions stored successfully"}
    mock_build_response.return_value = {"statusCode": 200, "body": "Success"}
    response = handler.create_security_questions(user_id, security_questions_data)
    mock_validator.assert_called_once_with(security_questions_data)
    mock_db.create_security_question.assert_called_once_with(user_id, security_questions_data)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "Success"}

def test_validate_security_question_success(mock_db, mock_build_response):
    user_id = "user123"
    question_answer = {"question": "What is your favorite color?",
                       "answer": "Blue"}
    mock_db.validate_security_question.return_value = {"valid": True}
    mock_build_response.return_value = {"statusCode": 200, "body": "Validation Successful"}
    response = handler.validate_security_question(user_id, question_answer)
    mock_db.validate_security_question.assert_called_once_with(user_id, question_answer)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 200, "body": "Validation Successful"}


def test_validate_security_question_failure(mock_db, mock_build_response):
    user_id = "user123"
    question_answer = {"question": "What is your favorite color?", "answer": "Red"}
    mock_db.validate_security_question.return_value = {"valid": False}
    mock_build_response.return_value = {"statusCode": 400, "body": "Validation Failed"}
    response = handler.validate_security_question(user_id, question_answer)
    mock_db.validate_security_question.assert_called_once_with(user_id, question_answer)
    mock_build_response.assert_called_once()
    assert response == {"statusCode": 400, "body": "Validation Failed"}