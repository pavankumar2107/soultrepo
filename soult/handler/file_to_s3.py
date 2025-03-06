import base64
from dao.user_dao import user_exists
from dynamodb.connection import get_s3_connection, get_s3_bucket
from utils.response_utils import build_response

URL = 'https://soult-docs.s3.amazonaws.com/'
ARN = 'arn:aws:s3:::soult-docs/'


def upload_file_to_s3(file_name: str, user_id: str, file_content: any):
    file_decoded = base64.b64encode(file_content)
    if user_exists(user_id):
        get_s3_connection().put_object(
            Bucket=get_s3_bucket(),
            Key=file_name,
            Body=file_decoded
        )
        return build_response({
                "message": f"File {file_name} uploaded successfully",
                "file_name": file_name,
                "file_arn": f"{ARN}{file_name}",
                "file_url": f"{URL}{file_name}",
               })
    else:
        return build_response({"message": "Invalid user"})