import time
from norconnect.classes import AWS
from norconnect.constants import AWSServices


def start_testing():

    sqs_url='https://sqs.ap-southeast-1.amazonaws.com/858460980823/amb-detour-location-stage.fifo'

    saws=AWS(services=[AWSServices.SQS],region="ap-southeast-1",aws_access_key="AKIA4PYCDAZLUHJILK7F",aws_secret_key="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",secrets_name='stage/subscription_ms')


    def print_data(data):
        print(data)
        return True


    saws.create_sqs_loop(sqs_url=sqs_url,callback=print_data,name='Print_Loop')
    saws.run_sqs_loops()

