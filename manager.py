import math
from utils import EC2, SQS
import time
#from ec2_metadata import ec2_metadata

def auto_scale():
    #que_len = SQS.get_queue_length()
    que_len = 13
    if que_len == 0:
        print('Shutting all instances')
        EC2.terminate_all_instances()
        return
    
    running_count = EC2.get_running_count()
    scaling_param = math.ceil((que_len / 5))
    
    if scaling_param > running_count:
        print('upscaling')
        upscale(min(scaling_param - running_count, 18 - running_count))

    if scaling_param < running_count:
        print('downscaling')

def upscale(count):
    if count == 0:
        return
    print('Adding ' + str(count) + " more instances.")
    instances = EC2.launch_instances(count)
    for instance in instances:
        print('Instance added with id : ' + instance)

if __name__ == '__main__':
    
    #EC2.launch_instances(count)
    #EC2.get_running_count()
    #EC2.get_instances()
    #EC2.get_instance_state()
    while(True):
        print('Checking for auto-scaling')
        auto_scale()
        time.sleep(100)