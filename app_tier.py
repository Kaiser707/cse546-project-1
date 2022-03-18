# from distutils import command
# from distutils.command.clean import clean
# from fileinput import filename
from utils import SQS, S3
import subprocess

def detect_object(filename):
    print('Performing detection on ' + filename)
    #S3.download_file(filename)
    command = ["python3", "face_recognition.py"]
    execution = subprocess.run(command, stdout=subprocess.PIPE)
    output = str(execution.stdout)
    #clean_output = output.replace('b','')
    clean_output = output.replace('\n','')
    clean_output = clean_output[2:-3]
    #print(clean_output)
    # with open(filename+'.txt', 'w') as f:
    #     f.write(clean_output)
    #     f.close()
    S3.put_result(filename=filename[:-4], output=clean_output)
    SQS.enqueue_out(filename + ' ' + clean_output)
    print(clean_output)
    return

if __name__=='__main__':
    #detect_object('file')
    while(True):
        filename = SQS.dequeue()
        if filename:
            print(filename + ' going for detection')
            detect_object(filename)