from flask import Flask
from os import environ, path
import boto3
app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/first')
def print_text():
    return 'Second'

@app.route('/putInput')
def put_input_item():
    sqs = boto3.resource('sqs', aws_access_key_id = app.config['AWS_ACCESS_KEY'], aws_secret_access_key = app.config['AWS_SECRET_ACCESS_KEY'], region_name='us-east-1')
    queue = sqs.get_queue_by_name(QueueName='cse546-input-queue')
    response = queue.send_message(MessageBody='First Message')
    print(response.get('MessageId'))
    return response.get('MessageId') 

@app.route('/fetchOutput')
def get_output_item():
    sqs = boto3.resource('sqs', aws_access_key_id = app.config['AWS_ACCESS_KEY'], aws_secret_access_key = app.config['AWS_SECRET_ACCESS_KEY'], region_name='us-east-1')
    queue = sqs.get_queue_by_name(QueueName='cse546-input-queue')
    for message in queue.receive_messages():
        return message.body
    return ""


