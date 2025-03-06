from utils.utils import build_response
from utils.utils import get_logger

logger = get_logger(__name__)

import boto3
import os

REGION = 'ap-south-1'
DYNAMODB = 'dynamodb'
BUCKET_NAME = 'soult-docs'
S3_BUCKET_NAME = 'S3_BUCKET_NAME'
S3 = 's3'
COGNITO = 'cognito-idp'

def get_connection():
    return boto3.resource(DYNAMODB, region_name=REGION)

def get_s3_connection():
    return boto3.client(S3, region_name=REGION)

def get_s3_bucket():
    return os.getenv(S3_BUCKET_NAME, BUCKET_NAME)

def get_cognito_connection():
    return boto3.client(COGNITO, region_name=REGION)

def with_connection(func):
    """Decorator to handle DynamoDB connection lifecycle."""

    def wrapper(*args, **kwargs):
        dynamodb = None
        try:
            dynamodb = get_connection()
            return func(dynamodb, *args, **kwargs)
        except Exception as e:
            logger.exception(f"Error in {func.__name__}: {e}")
            return build_response(500, {"error": str(e)})
        finally:
            if dynamodb and hasattr(dynamodb, 'close'):
                dynamodb.close()

    return wrapper
