import json
import logging
from utils.connections_utils import get_sns_connection


# Logger setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def event(model_name, action):
    """Decorator to send an SNS notification with attributes after a successful operation."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            sns_client = get_sns_connection()
            result = func(*args, **kwargs)

            # Ensure result is a dictionary and contains 'data'
            if isinstance(result, dict) and "data" in result:
                data = result["data"]

                # Construct message
                message = json.dumps({
                    "event": f"{model_name} {action}",
                    "User_id": args[0] if model_name != "user".upper() else data["id"],  # Assuming first argument is User_id
                    "action": action,
                    "model_name": model_name,
                    "model_id":data["id"] if model_name!="END_LIFE_PREFERENCES" else args[0],  # Safely get 'id'
                })

                # Construct MessageAttributes
                att_dict = {
                    "Action": {"DataType": "String", "StringValue": action},
                    "ModelName": {"DataType": "String", "StringValue": model_name},
                }

                # Publish to SNS topic

                response = sns_client.publish(
                    TopicArn='arn:aws:sns:ap-south-1:127214196952:soult-events',
                    Message=message,
                    Subject=f'{model_name} {action}',
                    MessageAttributes=att_dict
                )
                logger.info(f"SNS Notification sent: {response}")


            return result

        return wrapper

    return decorator
