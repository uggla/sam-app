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
    print("json loaded data")
    print(s3clientlist)


    pprint.pprint(event)

    # Get the service resource
    sqs = boto3.resource('sqs')

    # Get the queue
    queue = sqs.get_queue_by_name(QueueName='SimpleQueue')
    #queue = sqs.get_queue_by_name(QueueName='sam-app-SimpleQueue-HQ41P3FRAYA')

    # Process messages by printing out body and optional author name
    for message in queue.receive_messages(MessageAttributeNames=['Author']):
        # Get the custom author message attribute if it was set
        author_text = ''
        if message.message_attributes is not None:
            author_name = message.message_attributes.get('Author').get('StringValue')
            if author_name:
                author_text = ' ({0})'.format(author_name)

        # Print out the body and author (if set)
        print('Hello, {0}!{1}'.format(message.body, author_text))

        # Let the queue know that the message is processed
        message.delete()


if __name__ == "__main__":
    # execute only if run as a script
    lambda_handler('truc', 'machin')
