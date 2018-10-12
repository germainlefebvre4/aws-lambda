import json
import boto3
from boto3.session import Session


def lambda_handler(event, context):
    API_KEY="xxxxxxxxxxxxx"
    API_PWD="xxxxxxxxxxxxx"
    
    instances = {}
    
    session = boto3.Session(aws_access_key_id=API_KEY,
                            aws_secret_access_key=API_PWD)
    
    regions = session.get_available_regions(service_name='ec2')
    
    for region_name in regions:
        ec2c = boto3.client('ec2', region_name=region_name,
                            aws_access_key_id=API_KEY,
                            aws_secret_access_key=API_PWD)
        reservs = ec2c.describe_instances().get('Reservations')
        for reserv in reservs:
            insts = reserv.get('Instances')
            if len(insts) > 0:
                instances[region_name] = []
            for inst in insts:
                inst_state = inst.get('State').get('Name')
                if inst_state not in ["shutting-down", "terminated"]:
                    inst_id = inst.get('InstanceId')
                    instances[region_name].append(inst_state+" "+inst_id)
                else:
                    inst_id = inst.get('InstanceId')
                    instances[region_name].append(inst_state+" "+inst_id)

    
    return {
        "statusCode": 200,
        "instances": instances
    }

