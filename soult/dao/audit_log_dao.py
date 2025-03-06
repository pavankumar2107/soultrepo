from boto3.dynamodb.conditions import Attr
from dynamodb.connection import with_connection
from utils.logger_factory import get_logger

logger = get_logger(__name__)
ATTRIBUTE_EXISTS="attribute_exists"
@with_connection
def audit(dynamodb,user_id:str, log_entry: dict):
    table = dynamodb.Table("audit")
    table.update_item(
        Key={"id": user_id},
        UpdateExpression="SET audit_logs = list_append(if_not_exists(audit_logs, :empty_list), :log_entry)",
        ExpressionAttributeValues={
            ":log_entry": [log_entry],
            ":empty_list": []
        },
        ConditionExpression=Attr("user_id").exists() | Attr("user_id").not_exists()
    )

    return {"message": "Audit log entry added successfully"}