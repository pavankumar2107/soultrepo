import datetime
from boto3.dynamodb.conditions import Key
from utils.audit_log import audit_log
from utils.dao_utils import from_attributes_to_json
from utils.models import Operation, Model
from dynamodb.connection import with_connection
from utils.logger_factory import get_logger


logger = get_logger(__name__)
ATTRIBUTE_EXISTS="attribute_exists"
@with_connection
@audit_log(Model.USER.value, Operation.CREATE.value)
def create(dynamodb,user_id:str, user: dict):
    table = dynamodb.Table("user")
    table.put_item(Item=user)
    logger.info(f"Item: '{user} with {user_id}' Created successfully")
    logger.info("Created user successfully")
    return user,None


@with_connection
@audit_log(Model.USER.value, Operation.DELETE.value)
# use_id is used a dummy parameter to handle for audit log
def delete(dynamodb, user_id: str, use_id: str):
    table = dynamodb.Table("user")
    user = table.get_item(Key={"id": user_id})
    old_values = user["Item"]
    table.delete_item(Key={"id": user_id})
    logger.info(f"Deleted user successfully '{user_id}' {use_id}")
    return {"Message": "User deleted", "id": user_id},old_values


@with_connection
def find(dynamodb, user_id: str):
    table = dynamodb.Table("user")
    response = table.get_item(Key={"id": user_id})
    if "Item" in response:
        return from_attributes_to_json(response["Item"]),None
    else:
        raise ValueError(f"User not found with ID: {user_id}")


@with_connection
@audit_log(Model.USER.value, Operation.UPDATE.value)
def update(dynamodb, user_id: str, updated_data: dict):
    table = dynamodb.Table("user")
    user = table.get_item(Key={"id": user_id})
    old_values = user["Item"]
    updated_data["updated_at"]= datetime.datetime.now().isoformat()
    update_expression = "SET "
    expression_attribute_names = {}
    expression_attribute_values = {}
    for key, value in updated_data.items():
        attribute_name = f"#{key}"
        expression_attribute_names[attribute_name] = key
        expression_attribute_values[f":{key}"] = value
        update_expression += f"{attribute_name} = :{key},"
    update_expression = update_expression.rstrip(", ")
    response = table.update_item(
            Key={"id": user_id},
            UpdateExpression=update_expression,
            ConditionExpression=f"{ATTRIBUTE_EXISTS}(id)",
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW"
    )
    logger.info(f"Updated user successfully '{user_id}'")
    return from_attributes_to_json(response['Attributes']), old_values

@with_connection
def user_exists(dynamodb, user_id: str) -> bool:
    table = dynamodb.Table("user")
    response = table.get_item(Key={"id": user_id})
    return "Item" in response


@with_connection
def get_user_details(dynamodb, user_id: str):
    table = dynamodb.Table("user")
    response = table.get_item(Key={"id": user_id})
    if "Item" in response:
        item = response["Item"]
        return {
            "email": item["email"],
            "firstname": item["firstname"],
            "lastname": item["lastname"]
        }
    return None

@with_connection
def get_user_by_projection(dynamodb,user_id,entity):
    table = dynamodb.Table("user")
    user = table.get_item(Key={"id": user_id}, ProjectionExpression=entity)
    user_data = user["Item"]
    return user_data.get(entity, [])

@with_connection
def find_phone(dynamodb, phone_number: str):
    table = dynamodb.Table("user")
    response = table.query(
        IndexName="phone-no-index",
        KeyConditionExpression=Key("phone_no").eq(phone_number),
        Limit=1
    )
    return len(response.get('Items', [])) > 0

@with_connection
def find_email(dynamodb, email: str):
    table = dynamodb.Table("user")
    response = table.query(
        IndexName="email-index",
        KeyConditionExpression=Key("email").eq(email),
        Limit=1
    )
    return len(response.get('Items', [])) > 0
