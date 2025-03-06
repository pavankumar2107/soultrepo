import dynamodb.dynamodb_proxy as db
from utils.response_utils import build_response
from utils.logger_factory import get_logger
import validator.security_questions_validator  as validator
logger=get_logger(__name__)

def create_security_questions(user_id: str, security_question_answers: list):
    security_question_answers = validator.validate(security_question_answers)
    logger.info("Security Question validated successfully.")
    response = db.create_security_question(user_id, security_question_answers)
    logger.info(f" created for user {user_id}: {response}")
    return build_response(response)

def validate_security_question(user_id: str, question_answer: dict):
    response = db.validate_security_question(user_id, question_answer)
    logger.info(f" created for user {user_id}: {response}")
    return build_response(response)