import boto3

def get_running_count():
    ec2 = boto3.resource('ec2', region_name='us-east-1')
    return len([instance for instance in ec2.instances.all() if instance.state['Name'] != 'terminated'])

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

def launch_instances(count):
    ec2 = boto3.client('ec2', region_name='us-east-1')
    instances = ec2.run_instances(MinCount = count, MaxCount = count, LaunchTemplate = {'LaunchTemplateId' : 'lt-0897a45c86878b1d7'})
    return [instance['InstanceId'] for instance in instances['Instances']]

def terminate_all_instances():
    ec2_resource = boto3.resource('ec2', region_name='us-east-1')
    ec2 = boto3.client('ec2', region_name='us-east-1')
    run_instances = [instance.id for instance in ec2_resource.instances.all() if instance.state['Name'] != 'terminated']
    #print(run_instances)
    response = ec2.terminate_instances(InstanceIds = run_instances)