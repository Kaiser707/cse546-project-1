import boto3

def get_queue_length():
    sqs = boto3.resource('sqs', region_name='us-east-1')
    queue = sqs.get_queue_by_name(QueueName='cse546-input-queue')
    return int(queue.attributes.get('ApproximateNumberOfMessages'))

def enqueue(message):
    sqs = boto3.resource('sqs', region_name='us-east-1')
    queue = sqs.get_queue_by_name(QueueName='cse546-input-queue')
    response = queue.send_message(MessageBody=message)
    return response.get('MessageId')

def enqueue_out(message):
    sqs = boto3.resource('sqs', region_name='us-east-1')
    queue = sqs.get_queue_by_name(QueueName='cse546-output-queue')
    response = queue.send_message(MessageBody=message)
    return response.get('MessageId')

def dequeue():
    if get_queue_length() == 0:
        return
    sqs = boto3.resource('sqs', region_name='us-east-1')
    queue = sqs.get_queue_by_name(QueueName='cse546-input-queue')
    for message in queue.receive_messages():
        out = message.body
        message.delete()
        return out
    return ""