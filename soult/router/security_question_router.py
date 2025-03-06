from fastapi import APIRouter, HTTPException, Request
import handler.security_questions_handler as security_question_handler

router = APIRouter(prefix="/user/{user_id}/security_question", tags=['security_question'])

@router.post("/")
async def create_security_questions(user_id: str, request: Request):
    body = await request.json()
    if not isinstance(body, dict) or "security_questions" not in body:
        return HTTPException(status_code=400, detail="Invalid request format. Expected a 'security_questions' key.")
    security_questions = body["security_questions"]
    if not isinstance(security_questions, list):
        return HTTPException(status_code=400, detail="'security_questions' must be a list.")
    formatted_questions = [
        {"question": item["question"], "answer": item["answer"]}
        for item in security_questions
        if isinstance(item, dict) and "question" in item and "answer" in item
    ]
    if len(formatted_questions) != len(security_questions):
        return HTTPException(status_code=400, detail="Each security question must have 'question' and 'answer' keys.")
    response = security_question_handler.create_security_questions(user_id, formatted_questions)
    return {"message": "Security questions added successfully", "data": response}


@router.post("/validate")
async def validate_security_question(user_id: str, request : Request):
    body = await request.json()
    response = security_question_handler.validate_security_question(user_id, body)
    if response:
        return response
    raise HTTPException(status_code=400, detail="Security question validation failed")
