import boto3
import time

def get_running_count():
    ec2 = boto3.resource('ec2', region_name='us-east-1')
    return len([instance for instance in ec2.instances.all() if instance.state['Name'] == 'running' or instance.state['Name'] == 'pending'])

def get_instances():
    instanceIDs = []
    ec2 = boto3.resource('ec2', region_name='us-east-1')
    for instance in ec2.instances.all():
        instanceIDs.append(instance.id)
    return instanceIDs

def get_instance_state(instanceId):
    ec2 = boto3.resource('ec2', region_name='us-east-1')
    instance = ec2.Instance(instanceId)
    return instance.state

'''This method is helpful when the logic involes launching new instances as a part of auto-scaling'''
# def launch_instances(count):
#     ec2 = boto3.client('ec2', region_name='us-east-1')
#     instances = ec2.run_instances(MinCount = count, MaxCount = count, LaunchTemplate = {'LaunchTemplateId' : 'lt-0897a45c86878b1d7'})
#     return [instance['InstanceId'] for instance in instances['Instances']]

'''This method is helpful when the logic involes starting new instances as a part of auto-scaling'''
def start_instances(count):
    instanceIDs = get_instances()
    ec2_client = boto3.client('ec2', region_name='us-east-1')
    for instance in instanceIDs:
        if get_instance_state(instance)['Name'] == 'stopped':
            count -= 1
            run = []
            run.append(instance)
            print('Instance started with id : ' + instance)
            ec2_client.start_instances(InstanceIds=run)
            if count == 0:
                return

'''This method is helpful when the logic involes terminating all instances as a part of auto-scaling'''
# def terminate_all_instances():
#     ec2_resource = boto3.resource('ec2', region_name='us-east-1')
#     ec2 = boto3.client('ec2', region_name='us-east-1')
#     run_instances = [instance.id for instance in ec2_resource.instances.all() if instance.state['Name'] != 'terminated']
#     #print(run_instances)
#     response = ec2.terminate_instances(InstanceIds = run_instances)

'''This method is helpful when the logic involes sopping all instances as a part of auto-scaling'''
def stop_all_instances():
    if get_running_count() == 0:
        print('No instances running')
        return
    instanceIDs = get_instances()
    ec2_client = boto3.client('ec2', region_name='us-east-1')
    time.sleep(40)
    for instance in instanceIDs:
        if get_instance_state(instance)['Name'] == 'running':
            stop = []
            stop.append(instance)
            print('Instance stopped with id : ' + instance)
            ec2_client.stop_instances(InstanceIds=stop)