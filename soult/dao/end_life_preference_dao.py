import datetime
from dynamodb.dynamodb_utils import Entity
from utils.models import Operation, Model
from utils.audit_log import audit_log
from dynamodb.connection import with_connection

from utils.logger_factory import get_logger

logger = get_logger(__name__)
ATTRIBUTE_EXISTS="attribute_exists"

@with_connection
@audit_log(Model.ELP.value, Operation.CREATE.value)
def create(dynamodb, user_id: str, end_life_preferences: dict):
    table = dynamodb.Table("user")
    end_life_preferences["created_at"]=datetime.datetime.now().isoformat()
    table.update_item(
        Key={"id": user_id},
        UpdateExpression=f"SET #{Entity.ELP.value} = :{Entity.ELP.value}",
        ConditionExpression=f"{ATTRIBUTE_EXISTS}(id)",
        ExpressionAttributeNames={f'#{Entity.ELP.value}': Entity.ELP.value},
        ExpressionAttributeValues={
            f":{Entity.ELP.value}": end_life_preferences
        },
        ReturnValues="ALL_NEW"
    )
    logger.info(f"End Life Preferences added successfully for user '{user_id}': {end_life_preferences}")
    return end_life_preferences, None


@with_connection
@audit_log(Model.ELP.value, Operation.UPDATE.value)
def update(dynamodb, user_id: str,  updated_data: dict):
    table = dynamodb.Table("user")
    user = table.get_item(Key={"id": user_id},ProjectionExpression=Entity.ELP.value)
    user_data = user["Item"]
    existing_end_life_preferences_data = user_data.get(Entity.ELP.value, {})
    updated_end_life_preference = {
        **existing_end_life_preferences_data,
        **updated_data,
        "updated_at": datetime.datetime.now().isoformat()
    }
    old_values = existing_end_life_preferences_data
    table.update_item(
        Key={"id": user_id},
        UpdateExpression=f"SET #{Entity.ELP.value} = :{Entity.ELP.value}",
        ConditionExpression=f"{ATTRIBUTE_EXISTS}(id)",
        ExpressionAttributeNames={f"#{Entity.ELP.value}": Entity.ELP.value},
        ExpressionAttributeValues={
            f":{Entity.ELP.value}": updated_end_life_preference
        },
        ReturnValues="ALL_NEW"
    )
    logger.info(f"End life preference updated successfully for user '{user_id}'")
    return updated_end_life_preference, old_values


@with_connection
@audit_log(Model.ELP.value, Operation.DELETE.value)
def delete(dynamodb, user_id: str, end_life_preferences_id: str):
    table = dynamodb.Table("user")
    user = table.get_item(Key={"id": user_id},ProjectionExpression=Entity.ELP.value)
    user_data = user["Item"]
    existing_end_life_preferences_data = user_data.get(Entity.ELP.value, {})
    old_values = existing_end_life_preferences_data
    table.update_item(
        Key={"id": user_id},
        UpdateExpression=f"REMOVE #{Entity.ELP.value}",
        ConditionExpression=f"{ATTRIBUTE_EXISTS}(id)",
        ExpressionAttributeNames={f"#{Entity.ELP.value}": Entity.ELP.value},
        ReturnValues="ALL_NEW"
    )
    logger.info(
        f"End life preference deleted successfully for user '{user_id}' {end_life_preferences_id}")
    return {"message": "End life preference deleted", "user_id": user_id}, old_values


@with_connection
def find(dynamodb, user_id: str):
    table = dynamodb.Table("user")
    user = table.get_item(Key={"id": user_id},ProjectionExpression=Entity.ELP.value)
    user_data = user["Item"]
    end_life_preferences = user_data.get(Entity.ELP.value, {})
    if not end_life_preferences:
        raise ValueError(f"End life preference not found for user ID: {user_id}")
    return end_life_preferences
