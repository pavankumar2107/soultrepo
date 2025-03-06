from dynamodb.connection import with_connection
from dynamodb.dynamodb_utils import get_expression, Entity
from utils.dao_utils import from_attributes_to_json
from utils.utils import hash_value
from utils.logger_factory import get_logger

USER="user"
QUESTION = 'question'
ANSWER = 'answer'
MESSAGE = "message"
ERROR="error"

logger=get_logger(__name__)

@with_connection
def create(dynamodb,user_id, questions_and_answers: dict):
    table = dynamodb.Table(USER)
    security_questions = [
        {
            QUESTION: question_and_answer[QUESTION],
            ANSWER: hash_value(question_and_answer[ANSWER])
        }
        for question_and_answer in questions_and_answers
    ]
        # Store in DynamoDB
    response = table.update_item(
        Key={"id": user_id},
            UpdateExpression=get_expression(Entity.SQ),
            ExpressionAttributeNames={f'#{Entity.SQ.value}': Entity.SQ.value},
            ExpressionAttributeValues={
                f":{Entity.SQ.value}": security_questions,
                ":default": []
            },
            ReturnValues="ALL_NEW"
    )
    logger.info(f"Security question added successfully for user '{user_id}': {security_questions}")
    return from_attributes_to_json(response["Attributes"])

@with_connection
def validate(dynamodb, user_id, question_and_answer:dict):
    if not all(key in question_and_answer for key in [QUESTION, ANSWER]):
        logger.warning("Invalid input format. Expected {'question': str, 'answer': str}")
        return {ERROR: "Invalid input format"}
    selected_question = question_and_answer[QUESTION]
    user_answer = question_and_answer[ANSWER]

    table = dynamodb.Table(USER)
    response = table.get_item(Key={"id": user_id})
    if "Item" not in response or "security_questions" not in response["Item"]:
        logger.warning(f"No security questions found for user '{user_id}'")
        return {ERROR: "No security questions found."}
    security_questions = response["Item"]["security_questions"]
    matched_questions = list(filter(lambda q: q[QUESTION] == selected_question, security_questions))
    if not matched_questions:
        logger.warning(f"Selected question not found for user '{user_id}'")
        return {ERROR: "Selected question not found"}
    stored_hashed_answer = matched_questions[0][ANSWER]
    if hash_value(user_answer) == stored_hashed_answer:
        logger.info(f"Security question validated successfully for user '{user_id}'")
        return {MESSAGE: "Validation successful"}
    else:
        logger.warning(f"Incorrect answer for user '{user_id}'")
        return {ERROR: "Incorrect answer"}
