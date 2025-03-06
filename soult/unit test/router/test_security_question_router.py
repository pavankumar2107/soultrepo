from fastapi.testclient import TestClient
from unittest.mock import patch
from router.security_question_router import router

client = TestClient(router)

@patch("handler.security_questions_handler.create_security_questions")
def test_create_security_questions_success(mock_create_security_questions):
    mock_create_security_questions.return_value = {"id": "123", "security_questions": []}
    response = client.post("/user/test_user/security_question/", json={"security_questions": [{"question": "What is your pet's name?", "answer": "Charlie"}]})
    assert response.status_code == 200
    assert response.json()["message"] == "Security questions added successfully"

@patch("handler.security_questions_handler.validate_security_question")
def test_validate_security_question_success(mock_validate_security_question):
    mock_validate_security_question.return_value = {"valid": True}
    response = client.post("/user/test_user/security_question/validate", json={"question": "What is your pet's name?", "answer": "Charlie"})
    assert response.status_code == 200
    assert response.json() == {"valid": True}


