from enum import Enum


class AWSServices(Enum):
    SNS='sns'
    SQS='sqs'
    SECRETSMANAGER='secretsmanager'
    S3='s3'

class FilterOptions(Enum):
    ALL='all'
    ANY='any'