import boto3
REGION = 'ap-south-1'
DYNAMODB = 'dynamodb'
SNS = 'sns'
SES = 'ses'

def get_connection():
    return boto3.resource(DYNAMODB, region_name=REGION)

def get_sns_connection():
    return boto3.client(SNS, REGION)

def get_ses_connection():
    return boto3.client(SES, REGION)
