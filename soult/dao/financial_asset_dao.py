import datetime
from dao.user_dao import get_user_by_projection
from dynamodb.connection import with_connection
from dynamodb.dynamodb_utils import get_expression, Entity
from utils.audit_log import audit_log
from utils.dao_utils import build_record
from utils.models import Operation,Model
from utils.logger_factory import get_logger

USER = "user"
ATTRIBUTE_EXISTS="attribute_exists"

logger=get_logger(__name__)

@with_connection
@audit_log(Model.FA.value, Operation.CREATE.value)
def create(dynamodb, user_id: str, financial_asset_data: dict):
    table = dynamodb.Table(USER)
    financial_asset = financial_asset_data | build_record()
    table.update_item(
        Key={"id": user_id},
        UpdateExpression=get_expression(Entity.FA),
        ConditionExpression=f"{ATTRIBUTE_EXISTS}(id)",
        ExpressionAttributeNames={f'#{Entity.FA.value}': Entity.FA.value},
        ExpressionAttributeValues={
            f":{Entity.FA.value}": [financial_asset],
            ":default": []
        },
        ReturnValues="ALL_NEW"
    )
    logger.info(f"Asset added successfully for user '{user_id}': {financial_asset_data}")
    return financial_asset, None


@with_connection
@audit_log(Model.FA.value, Operation.UPDATE.value)
def update(dynamodb, user_id: str, financial_asset_id: str, new_values: dict):
    table = dynamodb.Table(USER)
    assets = get_user_by_projection(user_id, Entity.FA.value)
    financial_asset_to_update = next(
        filter(lambda asset: asset["id"] == financial_asset_id, assets), None
    )
    if not financial_asset_to_update:
        raise ValueError(f"Financial asset not found with ID: {financial_asset_id}")
    old_values = financial_asset_to_update
    updated_financial_asset = {
        **financial_asset_to_update,
        **new_values,
        "updated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    assets = [asset if asset["id"] != financial_asset_id else updated_financial_asset for asset in assets]
    table.update_item(
        Key={"id": user_id},
        UpdateExpression=f'SET #{Entity.FA.value} = :{Entity.FA.value}',
        ConditionExpression=f"{ATTRIBUTE_EXISTS}(id)",
        ExpressionAttributeNames={f'#{Entity.FA.value}': Entity.FA.value},
        ExpressionAttributeValues={
            f':{Entity.FA.value}': assets
        },
        ReturnValues="ALL_NEW"
    )
    logger.info(f"Asset updated successfully for user '{user_id}' (ID: {financial_asset_id})")
    return updated_financial_asset, old_values

@with_connection
@audit_log(Model.FA.value,Operation.DELETE.value)
def delete(dynamodb, user_id: str, financial_asset_id: str):
    table = dynamodb.Table(USER)
    assets = get_user_by_projection(user_id,Entity.FA.value)
    asset_to_delete = next((asset for asset in assets if asset["id"] == financial_asset_id), None)
    if not asset_to_delete:
        raise ValueError(f"financial asset not found with ID: {financial_asset_id}")
    old_values = asset_to_delete
    assets.remove(asset_to_delete)
    table.update_item(
        Key={"id": user_id},
        UpdateExpression=f'SET #{Entity.FA.value} = :{Entity.FA.value}',
        ConditionExpression=f"{ATTRIBUTE_EXISTS}(id)",
        ExpressionAttributeNames={f'#{Entity.FA.value}': Entity.FA.value},
        ExpressionAttributeValues={
            f":{Entity.FA.value}": assets
        },
        ReturnValues="ALL_NEW"
        )

    logger.info(f"Asset deleted successfully for user '{user_id}' (ID: {financial_asset_id})")
    return {"message": "Financial Asset deleted", "user_id": user_id, "id": financial_asset_id}, old_values


def find(user_id: str, financial_asset_id: str) -> dict:
    assets = get_user_by_projection(user_id,Entity.FA.value)
    if not assets:
        raise ValueError(f"No assets found for user with ID '{user_id}'.")
    assets = next(filter(lambda asset: asset["id"] == financial_asset_id, assets), None)
    if assets:
        return assets
    raise ValueError(f"Asset with ID '{financial_asset_id}' not found for user '{user_id}'.")


def find_all(user_id: str) -> dict:
    assets = get_user_by_projection(user_id,Entity.FA.value)
    if not assets:
        raise ValueError ("No Financial Asset found for user.")
    return assets

