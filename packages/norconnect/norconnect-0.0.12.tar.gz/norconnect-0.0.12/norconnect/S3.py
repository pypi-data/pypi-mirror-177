import asyncio
import json
import threading
import time
import traceback
from boto3 import resource




class S3:
    def __init__(self,bucket_name,client,aws_access_key_id,aws_secret_access_key,region_name):
        self.bucket_name = bucket_name
        self.client = client
        self.aws_access_key_id=aws_access_key_id
        self.aws_secret_access_key=aws_secret_access_key
        self.region_name=region_name

    async def upload_file_to_s3(self,s3_file_name, filename,ExtraArgs={'ACL': 'public-read'}):
        try:
            self.client.upload_file(filename, self.bucket_name, s3_file_name, ExtraArgs=ExtraArgs)
            return True, f"{self.bucket_name}/{s3_file_name}"
        except Exception as e:
            traceback.print_exc()
            return False,str(e)
    async def upload_file_content_to_s3(self,Key, Body, ContentType, folder,ACL='public-read'):
        try:
            s3resource= resource('s3', aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key, region_name=self.region_name)
            s3resource.Bucket(self.bucket_name).put_object(Key=f"{folder}/{Key}", Body=Body, ACL=ACL, ContentType=ContentType)
            return f"{self.bucket_name}/{folder}/{Key}"
        except Exception as e:
            traceback.print_exc()
            return False,str(e)
        finally:
            s3resource=None