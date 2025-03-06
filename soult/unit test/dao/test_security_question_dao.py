import pytest
from unittest.mock import MagicMock, patch
import dao.security_questions_dao as security_questions_dao

USER_ID = "123"
SECURITY_QUESTIONS = [
    {"question": "What is your pet's name?", "answer": "hashed_dog123"},
    {"question": "What is your favorite color?", "answer": "hashed_blue"}
]

VALID_ANSWER = {
    "question": "What is your pet's name?",
    "answer": "dog123"
}

INVALID_ANSWER = {
    "question": "What is your pet's name?",
    "answer": "wrong_answer"
}

@pytest.fixture
def mock_dynamodb():
    with patch("boto3.resource") as mock_boto3:
        mock_dynamodb = MagicMock()
        mock_table = MagicMock()
        mock_boto3.return_value = mock_dynamodb
        mock_dynamodb.Table.return_value = mock_table
        yield mock_table

@pytest.fixture
def mock_decorators():
    with patch("dao.security_questions_dao.with_connection", lambda func: func):
        yield

def test_create_security_questions(mock_dynamodb, mock_decorators):
    mock_dynamodb.update_item.return_value = {"Attributes": {"security_questions": SECURITY_QUESTIONS}}
    response = security_questions_dao.create(USER_ID, SECURITY_QUESTIONS)
    assert "security_questions" in response
    assert len(response["security_questions"]) == len(SECURITY_QUESTIONS)

def test_validate_correct_answer(mock_dynamodb, mock_decorators):
    mock_dynamodb.get_item.return_value = {"Item": {"security_questions": SECURITY_QUESTIONS}}
    with patch("dao.security_questions_dao.hash_value", return_value="hashed_dog123"):
        response = security_questions_dao.validate(USER_ID, VALID_ANSWER)
    assert response == {"message": "Validation successful"}

def test_validate_incorrect_answer(mock_dynamodb, mock_decorators):
    mock_dynamodb.get_item.return_value = {"Item": {"security_questions": SECURITY_QUESTIONS}}
    with patch("dao.security_questions_dao.hash_value", return_value="hashed_wrong"):
        response = security_questions_dao.validate(USER_ID, INVALID_ANSWER)
    assert response == {"error": "Incorrect answer"}

def test_validate_no_security_questions(mock_dynamodb, mock_decorators):
    mock_dynamodb.get_item.return_value = {}  # No Item found
    response = security_questions_dao.validate(USER_ID, VALID_ANSWER)
    assert response == {"error": "No security questions found."}

def test_validate_invalid_input_format(mock_dynamodb, mock_decorators):
    response = security_questions_dao.validate(USER_ID, {"question": "What is your pet's name?"})
    assert response == {"error": "Invalid input format"}

def test_validate_question_not_found(mock_dynamodb, mock_decorators):
    mock_dynamodb.get_item.return_value = {"Item": {"security_questions": SECURITY_QUESTIONS}}
    response = security_questions_dao.validate(USER_ID, {"question": "What is your school name?", "answer": "ABC School"})
    assert response == {"error": "Selected question not found"}
