import json
import os
import uuid
from botocore.exceptions import ClientError
import boto3
from norconnect.S3 import S3
from norconnect.SQS import SQS

from norconnect.constants import FilterOptions, AWSServices


class AWS:
    def __init__(self,services:list[AWSServices],region:str=os.environ.get('AWS_DEFAULT_REGION'),aws_access_key:str=os.environ.get('AWS_ACCESS_KEY_ID'),aws_secret_key:str=os.environ.get('AWS_SECRET_ACCESS_KEY'),secrets_name:str=os.environ.get('AWS_SECRET_ACCESS_KEY')):
        self.__clients={}
        self.secrets_name=secrets_name
        self.aws_access_key=aws_access_key
        self.aws_secret_key=aws_secret_key
        self.region=region
        self.sqs_list:list[SQS]=[]
        self.buckets:dict={}
        if not region and not aws_access_key and not aws_secret_key:
            raise ValueError
        self.__session= boto3.Session(aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_key,region_name=region)
        for s in services:
            self.__clients[s]=self.__create_client(s.value)

    def __create_client(self,service:str):
        return self.__session.client(service)

    def get_secrets(self,secrets_name=None):
        if self.__clients.get(AWSServices.SECRETSMANAGER):
            try:
                if not secrets_name:
                    secrets_name=self.secrets_name
                response=self.__clients.get(AWSServices.SECRETSMANAGER).get_secret_value(SecretId=secrets_name)
                secret=response['SecretString']
                return True,json.loads(secret)
            except ClientError as e:
                if e.response['Error']['Code'] == 'ResourceNotFoundException':
                        return False,"The requested secret " + secrets_name + " was not found"
                elif e.response['Error']['Code'] == 'InvalidRequestException':
                        return False,"The request was invalid due to:"+ str(e)
                elif e.response['Error']['Code'] == 'InvalidParameterException':
                        return False,"The request had invalid params:"+str(e)
                elif e.response['Error']['Code'] == 'DecryptionFailure':
                        return False,"The requested secret can't be decrypted using the provided KMS key:"+str(e)
                elif e.response['Error']['Code'] == 'InternalServiceError':
                        return False,"An error occurred on service side:"+str(e)
            except Exception as e:
                return False,"Error generated: %s" % str(e)
        else:
            return False,"The requested client does not exist."

    def publish_sns(self,body,SNS_ARN,usecaseStringValue,MessageGroupId,usecaseData_type:str='String',MessageDeduplicationId=uuid.uuid4().hex):
        if self.__clients.get(AWSServices.SNS):
            response = self.__clients.get(AWSServices.SNS).publish(
                    TargetArn=SNS_ARN,
                    Message=json.dumps(body),
                    MessageAttributes={
                        'usecase': {
                            'DataType': usecaseData_type,
                            'StringValue': usecaseStringValue
                        }
                    },
                    MessageDeduplicationId=MessageDeduplicationId,
                    MessageGroupId=MessageGroupId
                )
            return response
        else:
            return False,"The requested client does not exist."
    
    
    def create_sqs_loop(self,sqs_url,callback,name:str='Loop',sleep_time=0.2,visibility_timeout=20,wait_time_seconds=0,max_messages=10,filters:list[str]=[],filter_type:FilterOptions=FilterOptions.ANY):
        if self.__clients.get(AWSServices.SQS):
            try:
                sqs_loop=SQS(sqs_url,self.__clients[AWSServices.SQS],callback,name,sleep_time,visibility_timeout,wait_time_seconds,max_messages,filters,filter_type)
                self.sqs_list.append(sqs_loop)
                return True,None
            except Exception as e:
                return False,str(e)
        else:
            raise Exception("The requested client does not exist.")

    def run_sqs_loops(self):
        try:
            for loop in self.sqs_list:
                loop.run()
            return True,None
        except Exception as e:
            return False,str(e)

    def stop_sqs_loops(self):
        try:
            for loop in self.sqs_list:
                loop.stop()
            return True
        except Exception as e:
            return False,str(e)
    

    def create_s3_bucket(self,bucket_name:str):
        if self.__clients.get(AWSServices.S3):
            bucket=S3(bucket_name,self.__clients.get(AWSServices.S3),aws_access_key_id=self.aws_access_key,aws_secret_access_key=self.aws_secret_key,region_name=self.region)
            self.buckets[bucket_name]=bucket
            return True,self.buckets
        else:
            return False,"Client not available"

    def get_s3_buckets(self)->dict:
        return self.buckets
