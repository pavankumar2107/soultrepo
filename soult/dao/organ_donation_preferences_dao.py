import datetime

from dao.user_dao import get_user_by_projection
from dynamodb.dynamodb_utils import get_expression, Entity
from utils.audit_log import audit_log
from dynamodb.connection import with_connection
from utils.dao_utils import build_record
from utils.models import Operation, Model
from utils.logger_factory import get_logger

logger = get_logger(__name__)
ATTRIBUTE_EXISTS="attribute_exists"

@with_connection
@audit_log(Model.ODP.value, Operation.CREATE.value)
def create(dynamodb, user_id: str, organ_donation_preference: dict):
    table = dynamodb.Table("user")
    organ_donation_preference = organ_donation_preference | build_record()
    table.update_item(
        Key={"id": user_id},
        UpdateExpression=get_expression(Entity.ODP),
        ConditionExpression=f"{ATTRIBUTE_EXISTS}(id)",
        ExpressionAttributeNames={f'#{Entity.ODP.value}': Entity.ODP.value},
        ExpressionAttributeValues={
            f":{Entity.ODP.value}": [organ_donation_preference],
            ":default": []
        },
        ReturnValues="ALL_NEW"
    )

    logger.info(
        f"Organ Donation Preference added successfully for user '{user_id}': {organ_donation_preference}")
    return organ_donation_preference, None


@with_connection
@audit_log(Model.ODP.value, Operation.UPDATE.value)
def update(dynamodb, user_id: str, organ_donation_preference_id: str, updated_data: dict):
    table = dynamodb.Table("user")
    organ_donation_preferences = get_user_by_projection(user_id, Entity.ODP.value)
    organ_donation_preference_to_update =next(filter(lambda organ_donation_preference: organ_donation_preference["id"] == organ_donation_preference_id, organ_donation_preferences), None)
    if not organ_donation_preference_to_update:
        raise ValueError(f"Organ donation preference not found with ID: {organ_donation_preference_id}")
    updated_organ_donation_preference = {**organ_donation_preference_to_update, **updated_data,
                                         "updated_at": datetime.datetime.now().isoformat()}
    old_values = organ_donation_preference_to_update
    organ_donation_preferences.remove(organ_donation_preference_to_update)
    organ_donation_preferences.append(updated_organ_donation_preference)
    table.update_item(
        Key={"id": user_id},
        UpdateExpression=f"SET #{Entity.ODP.value} = :{Entity.ODP.value}",
        ConditionExpression=f"{ATTRIBUTE_EXISTS}(id)",
        ExpressionAttributeNames={f"#{Entity.ODP.value}": Entity.ODP.value},
        ExpressionAttributeValues={
            f":{Entity.ODP.value}": organ_donation_preferences
        },
        ReturnValues="ALL_NEW"
    )
    logger.info(
        f"organ donation preference updated successfully for user '{user_id}' (ID: {organ_donation_preference_id})")
    return updated_organ_donation_preference, old_values


@with_connection
@audit_log(Model.ODP.value, Operation.DELETE.value)
def delete(dynamodb, user_id: str, organ_donation_preference_id: str):
    table = dynamodb.Table("user")
    organ_donation_preferences = get_user_by_projection(user_id, Entity.ODP.value)
    organ_donation_preference_to_delete = next(filter(lambda organ_donation_preference: organ_donation_preference["id"] == organ_donation_preference_id, organ_donation_preferences), None)
    if not organ_donation_preference_to_delete:
        raise ValueError(f"organ donation preference not found for user {user_id} ID: {organ_donation_preference_id}")
    old_values = organ_donation_preference_to_delete
    organ_donation_preferences.remove(organ_donation_preference_to_delete)
    table.update_item(
        Key={"id": user_id},
        UpdateExpression=f"SET #{Entity.ODP.value} = :{Entity.ODP.value}",
        ConditionExpression=f"{ATTRIBUTE_EXISTS}(id)",
        ExpressionAttributeNames={f"#{Entity.ODP.value}": Entity.ODP.value},
        ExpressionAttributeValues={
            f":{Entity.ODP.value}": organ_donation_preferences
        },
        ReturnValues="ALL_NEW"
    )
    logger.info(
        f"Organ donation preference deleted successfully for user '{user_id}' (ID: {organ_donation_preference_id})")
    return {"message": "Organ donation preference deleted", "user_id": user_id, "id": organ_donation_preference_id}, old_values



def find(user_id: str, organ_donation_preference_id: str):
    organ_donation_preferences = get_user_by_projection(user_id, Entity.ODP.value)
    organ_donation_preference_to_read = next(filter(lambda organ_donation_preference: organ_donation_preference["id"] == organ_donation_preference_id, organ_donation_preferences), None)
    if not organ_donation_preference_to_read:
        raise ValueError(f"Organ donation preference not found with ID: {organ_donation_preference_id}")
    return organ_donation_preference_to_read



def find_all(user_id: str):
    organ_donation_preferences = get_user_by_projection(user_id, Entity.ODP.value)
    if not organ_donation_preferences:
        raise ValueError(f"No Organ donation preference for user with ID: {user_id}")
    return organ_donation_preferences
