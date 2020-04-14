#!/usr/bin/python3

import logging
import boto3
from botocore.exceptions import ClientError
import json
import pprint

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    s3_clientobj = s3.get_object(Bucket='mypfetestbucket', Key='ressources/exemple_ressource_1_S3.json')
    s3_clientdata = s3_clientobj['Body'].read().decode('utf-8')

    s3clientlist=json.loads(s3_clientdata)
    print("json loaded data from ressources/exemple_ressource_1_S3.js")
    print(s3clientlist)


    pprint.pprint(event)
    print("Event:")
    print(event)

    # Get the service resource
    sqs = boto3.resource('sqs')

    # Get the queue
    queue = sqs.get_queue_by_name(QueueName='ResultQueue')

    # Create a new message
    response = queue.send_message(MessageBody='Hello world')

    # The response is NOT a resource, but gives you a message ID and MD5
    print(response.get('MessageId'))
    print(response.get('MD5OfMessageBody'))

    body = json.loads(event["Records"][0]["body"])
    print("Body:")
    pprint.pprint(body)
    bucketName = body["Records"][0]["s3"]["bucket"]["name"]
    objectName = body["Records"][0]["s3"]["object"]["key"]
    print("bucketName: {}".format(bucketName))
    print("objectName: {}".format(objectName))

    s3_clientobj = s3.get_object(Bucket=bucketName, Key=objectName)
    s3_clientdata = s3_clientobj['Body'].read().decode('utf-8')
    print("File content: {}".format(s3_clientdata))
    response = queue.send_message(MessageBody=s3_clientdata)

if __name__ == "__main__":
    # execute only if run as a script
    event = {'Records': [{'messageId': '39933f50-5608-4f95-bb54-dd3447f8dfbb', 'receiptHandle': 'AQEBTB+UKIej5o+zLB9HcXEmtWPxILyaFWA1UNIlwuqLMenoUVZ2I1k1QA1Y/Ogy6tdKn+J+B+ZbtspqIHHMvhRiek4Ox8BA2QBohhvceU0TxD19G8FFo2d/pcf9PHqE3vRPIOdbxNzTwMhXl1ws4tnJpKo+pftK6tFab4fHP7tOa1v5RrpSvcYBzvP/ojAzaePGDryHrAP4HXCGKp0TobdnypkAO/A6SwbzExqhvXBsEqQUIHc28UNh5ak+vH9iqHRPUBx4rd2JpPRkD8uc5SuDlJbl8sjd2XObFPZxAk9XbGDG4xvyx/025eReZcn+z8i5KdKbaI4HNHCE3cC6oSxTnOFzx1fQIDyrs3CohfQN5pT517IVqrM2GSWQrHfHtj8HH9sNoYZqSoh/pMOY1Hmx+w==', 'body': '{"Records":[{"eventVersion":"2.1","eventSource":"aws:s3","awsRegion":"eu-west-3","eventTime":"2020-04-14T21:35:09.623Z","eventName":"ObjectCreated:Put","userIdentity":{"principalId":"AWS:AIDAYR7SIGKX4JQG7QX3V"},"requestParameters":{"sourceIPAddress":"185.125.227.44"},"responseElements":{"x-amz-request-id":"B7CFCE9549FA6ECE","x-amz-id-2":"M1OFxf3cjJnJq5Viamcn8JIq6+G2R/WCayfJIqiSV5DPNWxeeZWSh6D1icrl1ikZEOr8uZlYI6kdcDKE/VFDKRwuJ6LF7/3U"},"s3":{"s3SchemaVersion":"1.0","configurationId":"da69c796-2d31-486f-b7d7-1d26dbcc47f5","bucket":{"name":"mypfetestbucket","ownerIdentity":{"principalId":"A17MSC4CLQYL6C"},"arn":"arn:aws:s3:::mypfetestbucket"},"object":{"key":"essai.json","size":23,"eTag":"11a962af4e68e7c300af0efb6ac53c05","sequencer":"005E962C8DC5A63E0C"}}}]}', 'attributes': {'ApproximateReceiveCount': '9', 'SentTimestamp': '1586900110951', 'SenderId': 'AIDAI6JBEYZ27624XIP56', 'ApproximateFirstReceiveTimestamp': '1586900110951'}, 'messageAttributes': {}, 'md5OfBody': 'a5b55a6bcd2281487a3c1eb3d6532d63', 'eventSource': 'aws:sqs', 'eventSourceARN': 'arn:aws:sqs:eu-west-3:588381696687:SimpleQueue', 'awsRegion': 'eu-west-3'}]}

    lambda_handler(event, 'machin')
