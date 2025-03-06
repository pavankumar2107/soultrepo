import dynamodb.dynamodb_proxy as db
from cognito.cognito_client import create_cognito_id, validate_cognito_user
from dynamodb.connection import get_connection
from utils.dao_utils import build_record
from utils.sns_utils import event
from utils.logger_factory import get_logger
import validator.user_validator as validator
from utils.models import Model, Operation
from utils.response_utils import build_response

logger = get_logger(__name__)
@event(Model.USER.value, Operation.CREATE.value)
def create(user: dict):
    validated_user = validator.validate(user)
    if 'errors' in validated_user:
        return build_response(validated_user['errors'])
    else:
        dynamodb=get_connection()
        dynamodb.Table("user")
        user['firstname'] = user['firstname'].title()
        user['lastname'] = user['lastname'].title()
        user = user | build_record()
        user['id'] = create_cognito_id("7uoa3vrrtn8j8ockhfdhit2ean",user['phone_no'],user['mpin'])
        if not isinstance(user['id'], dict):
            response = db.create_user(user['id'], user)
            return build_response(response)
        else:
            return build_response({'message': "Invalid user id"})

# use_id is used a dummy parameter to handle for audit log
@event(Model.USER.value, Operation.DELETE.value)
def delete(user_id: str, model_id: str):
    response = db.delete_user(user_id, model_id)
    logger.info(response)
    return build_response(response)

@event(Model.USER.value, Operation.UPDATE.value)
def update(user_id: str, updated_data: dict):
    validated_user = validator.validate(updated_data)
    if 'errors' in validated_user:
        return build_response(validated_user['errors'])
    else:
        validated_user=db.update_user(user_id, validated_user)
        validated_user['firstname'] = validated_user['firstname'].title()
        validated_user['lastname'] = validated_user['lastname'].title()
        return build_response(validated_user)

def find(user_id: str):
    response = db.find_user(user_id)
    logger.info(response)
    return build_response(response)

def find_phone(phone_number: str):
    exists = db.find_phone(phone_number)
    logger.info(f"Phone number {phone_number} exists: {exists}")
    return build_response(exists)

def find_email(email: str):
    exists = db.find_email(email)
    logger.info(f"Email {email} exists: {exists}")
    return build_response(exists)

# cognito
def validate(user_id: str):
    response = validate_cognito_user(user_id)
    return build_response(response)
