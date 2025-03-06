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
@audit_log(Model.NMM.value, Operation.CREATE.value)
def create(dynamodb, user_id: str, non_material_memory_data: dict):
    table=dynamodb.Table(USER)
    non_material_memory_data["memory"] = list(
        map(lambda item: {**item, **build_record()} if "id" not in item else item,
            non_material_memory_data.get("memory", []))
    )
    non_material_memory = non_material_memory_data | build_record()
    table.update_item(
            Key={"id": user_id},
            UpdateExpression=get_expression(Entity.NMM),
            ConditionExpression=f"{ATTRIBUTE_EXISTS}(id)",
            ExpressionAttributeNames={f'#{Entity.NMM.value}': Entity.NMM.value},
            ExpressionAttributeValues={
                f":{Entity.NMM.value}": [non_material_memory_data],
                ":default": []
            },
            ReturnValues="ALL_NEW"
        )
    logger.info(f"Non Material Asset added successfully for user '{user_id}': {non_material_memory_data}")
    return non_material_memory,None

@with_connection
@audit_log(Model.NMM.value, Operation.UPDATE.value)
def update(dynamodb, user_id: str, non_material_memory_id: str, updated_data: dict):
    table = dynamodb.Table(USER)
    non_material_memories = get_user_by_projection(user_id, Entity.NMM.value)
    non_material_memory_to_update = next(filter(lambda non_material_asset: non_material_asset["id"] == non_material_memory_id, non_material_memories),None)
    if not non_material_memory_to_update:
        raise ValueError(f"Non Material Memory not found with ID: {non_material_memory_id}")
    updated_non_material_asset = {**non_material_memory_to_update, **updated_data, "updated_at": datetime.datetime.now().isoformat()}
    old_values = non_material_memory_to_update
    non_material_memories.remove(non_material_memory_to_update)
    non_material_memories.append(updated_non_material_asset)
    table.update_item(
            Key={"id": user_id},
            UpdateExpression=f'SET #{Entity.NMM.value} = :{Entity.NMM.value}',
            ConditionExpression=f"{ATTRIBUTE_EXISTS}(id)",
            ExpressionAttributeNames={f'#{Entity.NMM.value}': Entity.NMM.value},
            ExpressionAttributeValues={
                f':{Entity.NMM.value}': non_material_memories
            },
            ReturnValues="ALL_NEW"
        )
    logger.info(f"Non Material Asset updated successfully for user '{user_id}' (ID: {non_material_memory_id})")
    return updated_non_material_asset,old_values

@with_connection
@audit_log(Model.NMM.value,Operation.DELETE.value)
def delete(dynamodb, user_id: str, non_material_memory_id: str):
    table = dynamodb.Table(USER)
    non_material_memories = get_user_by_projection(user_id, Entity.NMM.value)
    non_material_memory_to_delete = next((non_material_memory for non_material_memory in non_material_memories if non_material_memory["id"] == non_material_memory_id), None)
    if not non_material_memory_to_delete:
        raise ValueError(f"Non Material Memory not found with ID: {non_material_memory_id}")
    old_values=non_material_memory_to_delete
    non_material_memories.remove(non_material_memory_to_delete)
    table.update_item(
        Key={"id": user_id},
        UpdateExpression=f'SET #{Entity.NMM.value} = :{Entity.NMM.value}',
        ConditionExpression=f"{ATTRIBUTE_EXISTS}(id)",
        ExpressionAttributeNames={f'#{Entity.NMM.value}': Entity.NMM.value},
        ExpressionAttributeValues={
            f':{Entity.NMM.value}': non_material_memories
        },
        ReturnValues="ALL_NEW"
    )
    logger.info(f"Non Material Asset deleted successfully for user '{user_id}' (ID: {non_material_memory_id})")
    return {"message": "Non Material Asset deleted", "user_id": user_id, "id": non_material_memory_id},old_values

def find(user_id: str, non_material_asset_id: str) -> dict:
    non_material_memories = get_user_by_projection(user_id, Entity.NMM.value)
    if not non_material_memories:
        raise ValueError(f"Non Material Assets Not Found For User With ID '{user_id}'.")
    non_assets = next(filter(lambda non_asset: non_asset["id"] == non_material_asset_id, non_material_memories), None)
    if non_assets:
        return non_assets
    raise ValueError(f"Non Material Asset with ID '{non_material_asset_id}' not found for user '{user_id}'.")


def find_all(user_id: str) -> dict:
    non_material_memories = get_user_by_projection(user_id, Entity.NMM.value)
    if not non_material_memories:
        raise ValueError("Non Material Assets Not Found For User")
    return non_material_memories