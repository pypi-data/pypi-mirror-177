import asyncio
import json
import threading
import time
import traceback

from norconnect.constants import FilterOptions


class SQS:
    def __init__(self,sqs_url,client,callback,name:str='Loop',sleep_time=0.2,visibility_timeout=20,wait_time_seconds=0,max_messages=10,filters:list[str]=[],filter_type:FilterOptions=FilterOptions.ANY):
        self.sqs_url = sqs_url
        self.client = client
        self.visibility_timeout = visibility_timeout
        self.callback = callback
        self.name = name
        self.sleep_time = sleep_time
        self.wait_time_seconds= wait_time_seconds
        self.max_messages = max_messages
        self.filters = filters
        self.filter_type=filter_type

    def run(self):
        self.thread = threading.Thread(target=self.__loop, daemon=True).start()
        
    def __loop(self):
        self.EVENT_LOOP = asyncio.new_event_loop()
        print(f'{self.name} loop started {self.EVENT_LOOP}')
        self.EVENT_LOOP.run_until_complete(self.__read_sqs())

    def __read_sqs(self):
        while True:
            time.sleep(self.sleep_time)
            response = self.client.receive_message(
                QueueUrl=self.sqs_url,
                AttributeNames=[
                    'SentTimestamp'
                ],
                MaxNumberOfMessages=self.max_messages,
                MessageAttributeNames=[
                    'All'
                ],
                VisibilityTimeout=self.visibility_timeout,
                WaitTimeSeconds=self.wait_time_seconds
            )
            messages = response.get("Messages")
            if messages is not None:
                for message in messages:
                    try:
                        message_body = message["Body"]
                        # message_body = json.loads(message_body)
                        data = json.loads(message_body)
                        receipt_handler = message.get('ReceiptHandle')
                        is_valid=self.__is_filtred(data)
                        if is_valid:
                            response=self.callback(data)
                            if response==None:
                                raise Exception("Return cannot be none")
                            else:
                                if response:
                                    self.delete_message(receipt_handler=receipt_handler)
                        else:
                            self.delete_message(receipt_handler=receipt_handler)
                    except Exception as e:
                        traceback.print_exc()

    def delete_message(self,receipt_handler):
        if receipt_handler is not None:
            response = self.client.delete_message(
                QueueUrl=self.sqs_url,
                ReceiptHandle=receipt_handler,
                )
    
    
    def stop(self):
        self.EVENT_LOOP.call_soon_threadsafe(self.EVENT_LOOP.stop)
        print(f'{self.name} loop Stopping {self.EVENT_LOOP}')

    def __is_filtred(self,data):
        is_valid=True
        if len(self.filters)==0:
            return is_valid
        else:
            if self.filter_type==FilterOptions.ALL:
                for filter in self.filters:
                    is_valid=filter in data.keys()
                    if not is_valid:
                        return False
            elif self.filter_type==FilterOptions.ANY:
                for filter in self.filters:
                    is_valid=filter in data.keys()
                    if is_valid:
                        return True