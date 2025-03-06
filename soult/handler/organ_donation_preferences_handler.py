import dynamodb.dynamodb_proxy as db
from utils.logger_factory import get_logger
import validator.organ_donation_preferences_validator as validator
from utils.response_utils import build_response
from utils.models import Operation, Model
from utils.sns_utils import event

logger = get_logger(__name__)

@event(Model.ODP.value, Operation.CREATE.value)
def create(user_id:str, organ_donation_preference:dict):
    validated_data = validator.validate(organ_donation_preference)
    if 'errors' in validated_data:
        return build_response(validated_data['errors'])

    else:
        response=db.create_organ_donation_preference(user_id, validated_data)
        return build_response(response)

@event(Model.ODP.value, Operation.UPDATE.value)
def update(user_id:str, organ_donation_preference_id:str, updated_data:dict):
    validated_data = validator.validate(updated_data)
    if 'errors' in validated_data:
        return build_response(validated_data['errors'])

    else:
        response=db.update_organ_donation_preference(user_id, organ_donation_preference_id, validated_data)
        return build_response(response)

@event(Model.ODP.value, Operation.DELETE.value)
def delete(user_id:str, organ_donation_preference_id:str):
    response = db.delete_organ_donation_preference(user_id, organ_donation_preference_id)
    logger.info(response)
    return build_response(response)


def find(user_id:str, organ_donation_preference_id:str):
    response = db.find_organ_donation_preference(user_id, organ_donation_preference_id)
    logger.info(response)
    return build_response(response)


def find_all(user_id:str):
    response = db.find_all_organ_donation_preferences(user_id)
    logger.info(response)
    return build_response(response)
