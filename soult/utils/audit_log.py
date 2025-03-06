import datetime
import functools
import logging

from dao import audit_log_dao
from utils.models import Operation, Model
from utils.utils import generate_uuid

AUDIT ="audit"

# Logger setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def audit_log(model: str, operation: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Entering wrapper with args={args}, kwargs={kwargs}")
            user_id = args[1]
            if (operation == Operation.UPDATE.value and model in {Model.USER.value,Model.ELP.value}) or operation == Operation.CREATE.value:
                new_values = args[2]
                model_id = None
            else:
                model_id = args[2]
                new_values = args[3] if operation == Operation.UPDATE.value else None
            result, old_values = func(*args, **kwargs)
            logger.info(f"Function {func.__name__} result: {result}")
            # Handle Create case (Assign new model_id)
            if all([operation == Operation.CREATE.value, isinstance(result, dict), 'id' in result]):
                model_id = result['id']
                new_values = new_values | result
            log_entry = {
                "id": generate_uuid(),
                "user_id": user_id,
                "model": model,
                "model_id": model_id or user_id,
                "old_values": old_values,
                "new_values": new_values | {'id': model_id or user_id} if operation != Operation.DELETE.value else None,
                "operation": operation,
                "created_at": datetime.datetime.now().isoformat(),
            }
            audit_log_dao.audit(user_id, log_entry)
            logger.info("Audit log entry created successfully.")
            return result

        return wrapper

    return decorator
