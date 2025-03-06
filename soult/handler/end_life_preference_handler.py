import dynamodb.dynamodb_proxy as db
from utils.response_utils import build_response
from utils.models import Model, Operation
from utils.logger_factory import get_logger
import validator.end_life_preferences_validate as validator
from utils.sns_utils import event

logger = get_logger(__name__)

@event(Model.ELP.value, Operation.CREATE.value)
def create(user_id: str, end_life_preferences: dict):
    validated_data = validator.validate(end_life_preferences)
    if 'errors' in validated_data:
        return build_response(validated_data['errors'])

    else:
        response=db.create_end_life_preferences(user_id, validated_data)
        return build_response(response)

@event(Model.ELP.value, Operation.UPDATE.value)
def update(user_id: str, updated_data: dict):
    validated_data = validator.validate(updated_data)
    if 'errors' in validated_data:
        return build_response(validated_data['errors'])

    else:
        response=db.update_end_life_preferences(user_id, validated_data)
        return build_response(response)


@event(Model.ELP.value,Operation.DELETE.value)
def delete(user_id: str, end_life_preferences_id: str):
    response = db.delete_end_life_preferences(user_id, end_life_preferences_id)
    logger.info(response)
    return build_response(response)

def find(user_id: str):
    response = db.find_end_life_preferences(user_id, )
    logger.info(response)
    return build_response(response)