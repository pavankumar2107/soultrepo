import dynamodb.dynamodb_proxy as db
from utils.models import Operation, Model
from utils.response_utils import build_response
from utils.logger_factory import get_logger
import validator.non_material_memory_validator as validator
from utils.sns_utils import event

logger=get_logger(__name__)

@event(Model.NMM.value, Operation.CREATE.value)
def create(user_id: str, non_material_memory: dict):
    validated_data = validator.validate(non_material_memory)
    if 'errors' in validated_data:
        return build_response(validated_data['errors'])
    return build_response(db.create_non_material_memory(user_id, validated_data))

@event(Model.NMM.value, Operation.UPDATE.value)
def update(user_id: str, non_asset_id: str, updated_data: dict):
    validated_data = validator.validate(updated_data)
    if 'errors' in validated_data:
        return build_response(validated_data['errors'])
    return build_response(db.update_non_material_memory(user_id, non_asset_id, validated_data))

@event(Model.NMM.value, Operation.DELETE.value)
def delete(user_id: str, non_material_memory_id: str):
    response = db.delete_non_material_memory(user_id, non_material_memory_id)
    logger.info(f"Non Material Asset successfully deleted for user {user_id}: {response}")
    return build_response(response)


def find(user_id: str, non_material_memory_id: str):
    response = db.find_non_material_memory(user_id, non_material_memory_id)
    logger.info(f"Non Material Asset found for user with non_material_memory_id {non_material_memory_id}: {response}")
    return build_response(response)


def find_all(user_id: str):
    response = db.find_all_non_material_memory(user_id)
    logger.info(f"Non Material Asset found for user with user_id {user_id}: {response}")
    return build_response(response)
