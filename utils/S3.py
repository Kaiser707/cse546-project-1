from urllib import response
import boto3

def upload_file(file, filename):
    session = boto3.session.Session()
    s3 = session.resource('s3')
    bucket = s3.Bucket('cse-546-input-bucket')
    try:
        bucket.upload_fileobj(file, filename)
    except:
        print('Error occured while uploading')

def download_file(filename):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('cse-546-input-bucket')    
    try:
        with open(filename, 'wb') as f:
            bucket.download_fileobj(filename, f)
    except:
        print('Error occured while downloading')

def put_result(filename, output):
    session = boto3.session.Session()
    s3 = session.resource('s3')
    object = s3.Object('cse-546-out-bucket', filename)
    response = object.put(Body=output)