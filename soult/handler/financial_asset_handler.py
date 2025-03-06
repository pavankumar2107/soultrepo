import dynamodb.dynamodb_proxy as db
from utils.sns_utils import event
from utils.models import Operation, Model
from utils.response_utils import  build_response
from utils.logger_factory import get_logger
import validator.financial_asset_validator as validator

logger=get_logger(__name__)

@event(Model.FA.value, Operation.CREATE.value)
def create(user_id: str, financial_asset_data: dict):
    financial_asset_data = validator.validate(financial_asset_data)
    if 'errors' in financial_asset_data:
        return build_response(financial_asset_data['errors'])
    else:
        return build_response(db.create_financial_asset(user_id, financial_asset_data))


@event(Model.FA.value, Operation.UPDATE.value)
def update(user_id: str, financial_asset_id: str, updated_data: dict):
    financial_asset_data = validator.validate(updated_data)
    if 'errors' in financial_asset_data:
        return build_response(financial_asset_data['errors'])
    else:
        return build_response(db.update_financial_asset(user_id, financial_asset_id, financial_asset_data))


@event(Model.FA.value,Operation.DELETE.value)
def delete(user_id: str, financial_asset_id: str):
    response = db.delete_financial_asset(user_id, financial_asset_id)
    logger.info(response)
    return build_response(response)


def find(user_id: str, financial_asset_id: str):
    response = db.find_financial_asset(user_id, financial_asset_id)
    logger.info(response)
    return build_response(response)


def find_all(user_id: str):
    response = db.find_all_financial_asset(user_id)
    logger.info(response)
    return build_response(response)
