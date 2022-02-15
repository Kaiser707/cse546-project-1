import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import boto3
from utils import SQS
from utils import S3

app = Flask(__name__)
#app.config.from_pyfile('config.py')

@app.route('/')
def hello_world():
   return 'Hello world!'

@app.route('/upload', methods = ['POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      filename = secure_filename(f.filename)
      S3.upload_file(file=f, filename=filename)
      response = SQS.enqueue(filename)
      return 'Message id :' + response

# @app.route('/putInput')
# def put_input_item():
#    sqs = boto3.resource('sqs', region_name='us-east-1')
#    queue = sqs.get_queue_by_name(QueueName='cse546-input-queue')
#    response = queue.send_message(MessageBody='First Message')
#    print(response.get('MessageId'))
#    return response.get('MessageId') 

# @app.route('/fetchOutput')
# def get_output_item():
#    sqs = boto3.resource('sqs', region_name='us-east-1')
#    queue = sqs.get_queue_by_name(QueueName='cse546-input-queue')
#    for message in queue.receive_messages():
#       out = message.body
#       message.delete()
#       return out
#    return ""