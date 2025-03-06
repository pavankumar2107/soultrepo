import dynamodb.dynamodb_proxy as db
import validator.loved_ones_validator as validator
from utils.logger_factory import get_logger
from utils.response_utils import  build_response
from utils.models import Operation, Model
from utils.sns_utils import event

logger = get_logger(__name__)

@event(Model.LO.value, Operation.CREATE.value)
def create(user_id: str, loved_ones_data: dict):
    validated_data = validator.validate(
        loved_ones_data)
    print(validated_data)
    if 'errors' in validated_data:
        return build_response(validated_data['errors'])

    else:
        response=db.create_loved_ones(user_id, validated_data)
        return build_response(response)

@event(Model.LO.value, Operation.UPDATE.value)
def update(user_id: str, loved_ones_id: str, updated_data: dict):
    validated_data = validator.validate(updated_data)
    # print(validated_data)
    if 'errors' in validated_data:
        print(validated_data['errors'])
        return build_response(validated_data['errors'])

    else:
        response=db.update_loved_ones(user_id, loved_ones_id, validated_data)
        return build_response(response)

@event(Model.LO.value, Operation.DELETE.value)
def delete(userid: str, loved_ones_id: str):
    response = db.delete_loved_ones(userid, loved_ones_id)
    logger.info(response)
    return build_response(response)


def find(user_id: str, loved_ones_id: str):
    response = db.find_loved_ones(user_id, loved_ones_id)
    logger.info(response)
    return build_response(response)


def find_all(user_id: str):
    response = db.find_all_loved_ones(user_id)
    logger.info(response)
    return build_response(response)
