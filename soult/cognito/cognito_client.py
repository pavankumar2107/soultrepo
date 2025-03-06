from botocore.exceptions import ClientError
from dynamodb.connection import get_cognito_connection

USER_POOL_ID = 'ap-south-1_b5m3URusw'
def create_cognito_id(user_id:str, username:str, mpin:str):
    try:
        response = get_cognito_connection().sign_up(
            ClientId=user_id,
            Username=username,
            Password=mpin
        )
        return response['UserSub']
    except ClientError as e:
        if e.response['Error']['Code'] == 'UsernameExistsException':
            return {"error": "User already exists"}
        else:
            return {"error": str(e)}

def validate_cognito_user(username:str):
    try:
        response = get_cognito_connection().admin_get_user(
            UserPoolId=USER_POOL_ID,
            Username=username
        )
        return response['UserAttributes']
    except ClientError as e:
        if e.response['Error']['Code'] == 'UserNotFoundException':
            return {"error": "User does not exists"}
        else:
            return {"error": str(e)}