import boto3

def get_queue_length():
    session = boto3.session.Session()
    sqs = session.resource('sqs', region_name='us-east-1')
    queue = sqs.get_queue_by_name(QueueName='cse546-input-queue')
    return int(queue.attributes.get('ApproximateNumberOfMessages'))

def get_out_queue_length():
    session = boto3.session.Session()
    sqs = session.resource('sqs', region_name='us-east-1')
    queue = sqs.get_queue_by_name(QueueName='cse546-output-queue')
    return int(queue.attributes.get('ApproximateNumberOfMessages'))

def enqueue(message):
    session = boto3.session.Session()
    sqs = session.resource('sqs', region_name='us-east-1')
    queue = sqs.get_queue_by_name(QueueName='cse546-input-queue')
    response = queue.send_message(MessageBody=message)
    return response.get('MessageId')

def enqueue_out(message):
    session = boto3.session.Session()
    sqs = session.resource('sqs', region_name='us-east-1')
    queue = sqs.get_queue_by_name(QueueName='cse546-output-queue')
    response = queue.send_message(MessageBody=message)
    return response.get('MessageId')

def dequeue():
    if get_queue_length() == 0:
        return
    session = boto3.session.Session()
    sqs = session.resource('sqs', region_name='us-east-1')
    queue = sqs.get_queue_by_name(QueueName='cse546-input-queue')
    #print(len(queue.receive_messages(MaxNumberOfMessages=1)))
    for message in queue.receive_messages(MaxNumberOfMessages=1):
        out = message.body
        message.delete()
        return out
    # sqs = boto3.client('sqs', region_name='us-east-1')
    # response = sqs.receive_message(QueueUrl='https://sqs.us-east-1.amazonaws.com/390958635768/cse546-input-queue',MaxNumberOfMessages=1)
    # print(response)
    # # message = response['Messages'][0]
    # # receipt_handle = message['ReceiptHandle']
    # # sqs.delete_message(QueueUrl='https://sqs.us-east-1.amazonaws.com/390958635768/cse546-input-queue', ReceiptHandle=receipt_handle)

    # # return message['Body']

def get_result_to_send(filename):
    sqs = boto3.resource('sqs', region_name='us-east-1')
    queue = sqs.get_queue_by_name(QueueName='cse546-output-queue')
    while(True):
        if get_out_queue_length() == 0:
            continue
        for message in queue.receive_messages():
            out = message.body
            if(out.split(' ')[0] == filename):
                return out

def get_messages():
    result = {}
    session = boto3.session.Session()
    sqs = session.resource('sqs', region_name='us-east-1')
    queue = sqs.get_queue_by_name(QueueName='cse546-input-queue')
    # print(queue.receive_messages(MaxNumberOfMessages=3))
    for message in queue.receive_messages(MaxNumberOfMessages=2):
        out = message.body
        result[out.split(' ')[0]] = out.split(' ')[1]
        message.delete()

    return result