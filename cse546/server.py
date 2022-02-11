from flask import Flask
import boto3
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/first')
def print_text():
    return 'Second'

@app.route('/putInput')
def put_input_item():
    return "" 

@app.route('/fetchOutput')
def get_output_item():
    return ""


