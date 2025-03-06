import datetime

from dao.user_dao import get_user_by_projection
from dynamodb.connection import with_connection
from dynamodb.dynamodb_utils import get_expression, Entity
from utils.audit_log import audit_log
from utils.dao_utils import build_record
from utils.models import Operation,Model
from utils.logger_factory import get_logger

logger = get_logger(__name__)
USER = "user"
ATTRIBUTE_EXISTS="attribute_exists"

@with_connection
@audit_log(Model.LO.value, Operation.CREATE.value)
def create(dynamodb, user_id: str, loved_ones: dict):
    table = dynamodb.Table(USER)
    loved_ones = loved_ones | build_record()
    table.update_item(
                Key={"id": user_id},
                UpdateExpression=get_expression(Entity.LO),
                ConditionExpression=f"{ATTRIBUTE_EXISTS}(id)",
                ExpressionAttributeNames={f'#{Entity.LO.value}': Entity.LO.value},
                ExpressionAttributeValues={
                    f":{Entity.LO.value}": [loved_ones],
                    ":default": []
                },
                ReturnValues="ALL_NEW"
        )
    logger.info(f"loved one added successfully for user '{user_id}': {loved_ones}")
    return loved_ones,None

@with_connection
@audit_log(Model.LO.value,Operation.UPDATE.value)
def update(dynamodb, user_id: str, loved_ones_id: str, updated_data: dict):
    table = dynamodb.Table(USER)
    loved_ones = get_user_by_projection(user_id,Entity.LO.value)
    loved_ones_to_update = next(filter(lambda loved_one: loved_one["id"] == loved_ones_id, loved_ones), None)
    if not loved_ones_to_update:
        raise ValueError(f"Loved One not found with ID: {loved_ones_id}")
    updated_loved_ones = {**loved_ones_to_update, **updated_data, "updated_at": datetime.datetime.now().isoformat()}
    old_values = loved_ones_to_update
    loved_ones.remove(loved_ones_to_update)
    loved_ones.append(updated_loved_ones)
    table.update_item(
            Key={"id": user_id},
            UpdateExpression=f'SET #{Entity.LO.value} = :{Entity.LO.value}',
            ConditionExpression=f"{ATTRIBUTE_EXISTS}(id)",
            ExpressionAttributeNames={f'#{Entity.LO.value}': Entity.LO.value},
            ExpressionAttributeValues={
                f":{Entity.LO.value}": loved_ones
            },
            ReturnValues="ALL_NEW"
        )
    logger.info(f"loved one updated successfully for user '{user_id}' (ID: {loved_ones_id})")
    return updated_loved_ones,old_values

@with_connection
@audit_log(Model.LO.value,Operation.DELETE.value)
def delete(dynamodb, user_id: str, loved_ones_id: str):
    table = dynamodb.Table(USER)
    loved_ones = get_user_by_projection(user_id,Entity.LO.value)
    loved_ones_to_delete = next(filter(lambda loved_one: loved_one["id"] == loved_ones_id, loved_ones), None)
    if not loved_ones_to_delete:
        raise ValueError(f"Loved One not found with ID: {loved_ones_id}")
            # Remove the loved ones
    old_values = loved_ones_to_delete
    loved_ones.remove(loved_ones_to_delete)
    table.update_item(
        Key={"id": user_id},
        UpdateExpression=f'SET #{Entity.LO.value} = :{Entity.LO.value}',
        ConditionExpression=f"{ATTRIBUTE_EXISTS}(id)",
        ExpressionAttributeNames={f'#{Entity.LO.value}': Entity.LO.value},
        ExpressionAttributeValues={
            f":{Entity.LO.value}": loved_ones
            },
            ReturnValues="ALL_NEW"
        )

    logger.info(f"loved one deleted successfully for user '{user_id}' (ID: {loved_ones_id})")
    return {"Message": "loved one deleted", "user_id": user_id, "id": loved_ones_id},old_values

def find(user_id: str, loved_ones_id: str):
    loved_ones = get_user_by_projection(user_id, Entity.LO.value)
    loved_ones_to_read = next(filter(lambda loved_one: loved_one["id"] == loved_ones_id, loved_ones), None)
    if not loved_ones_to_read:
        raise ValueError(f"Loved One not found with ID: {loved_ones_id}")
    return loved_ones_to_read


def find_all(user_id: str):
    loved_ones = get_user_by_projection(user_id,Entity.LO.value)
    if not loved_ones:
        raise ValueError("No Loved One found for user")
    else:
        return loved_ones
